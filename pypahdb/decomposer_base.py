#!/usr/bin/env python3
"""
decomposer_base.py

Using a precomputed matrix of theoretically calculated
PAH emission spectra, an input spectrum is fitted and decomposed into
contributing PAH subclasses using a non-negative least-squares (NNLS)
approach.

This file is part of pypahdb - see the module docs for more
information.
"""

import multiprocessing
import pickle
from functools import partial

import numpy as np
import pkg_resources
from astropy import units as u
from scipy import optimize
from specutils import Spectrum1D


def _decomposer_anion(w, m=None, p=None):
    """Do the anion decomposition in multiprocessing."""
    return m.dot(w * (p < 0).astype(float))


def _decomposer_neutral(w, m=None, p=None):
    """Do the neutral decomposition in multiprocessing."""
    return m.dot(w * (p == 0).astype(float))


def _decomposer_cation(w, m=None, p=None):
    """Do the cation decomposition in multiprocessing."""
    return m.dot(w * (p > 0).astype(float))


def _decomposer_large(w, m=None, p=None):
    """Do the actual large decomposition in multiprocessing."""
    return m.dot(w * (p > 40).astype(float))


def _decomposer_small(w, m=None, p=None):
    """Do the small decomposition in multiprocessing."""
    return m.dot(w * (p <= 40).astype(float))


def _decomposer_fit(w, m=None):
    """Do the matrix manipulation to obtain the total fit in
    multiprocessing."""
    return m.dot(w)


def _decomposer_interp(fp, x=None, xp=None):
    """Do the grid interpolation in multiprocessing."""
    return np.interp(x, xp, fp)


def _decomposer_nnls(y, m=None):
    """Do the NNLS in multiprocessing."""
    return optimize.nnls(m, y)


class DecomposerBase(object):
    """Fit and decompose spectrum.

    Attributes:
       spectrum: A spectrum to fit and decompose.
    """

    def __init__(self, spectrum):
        """Construct a decomposer object.

        Args:
            spectrum (specutil.Spectrum1D): The spectrum to fit and decompose.
        """

        self._mask = None
        self._yfit = None
        self._yerror = None
        self._ionized_fraction = None
        self._large_fraction = None
        self._charge = None
        self._size = None

        # Check if spectrum is a Spectrum1D.
        if not isinstance(spectrum, Spectrum1D):
            print("spectrum is not a specutils.Spectrum1D")
            return None

        self.spectrum = spectrum

        # Convert units of spectrum to wavenumber and flux (density).
        abscissa = self.spectrum.spectral_axis.to(
            1.0 / u.cm, equivalencies=u.spectral()
        )
        try:
            ordinate = self.spectrum.flux.to(
                u.Unit("MJy/sr"), equivalencies=u.spectral()
            ).T
        except u.UnitConversionError:
            ordinate = self.spectrum.flux.to(u.Unit("Jy"), equivalencies=u.spectral()).T
            pass

        # For clarity, define a few quantities.
        n_elements_yz = ordinate.shape[1] * ordinate.shape[2]
        pool_shape = np.reshape(ordinate, (ordinate.shape[0], n_elements_yz))

        # Avoid fitting -zero- spectra.
        self._mask = np.where(np.sum(pool_shape, axis=0) > 0.0)[0]
        if self._mask.size == 0:
            print("spectral data is all zeros.")
            return None

        # Retrieve the precomputed data and raise error if file is
        # not found.
        file_name = "resources/precomputed.pkl"
        file_path = pkg_resources.resource_filename("pypahdb", file_name)
        with open(file_path, "rb") as f:
            try:
                self._precomputed = pickle.load(f, encoding="latin1")
            except Exception as e:
                print("Python 3 is required for pypahdb.")
                raise (e)

        # Linearly interpolate the precomputed spectra onto the
        # frequency grid of the input spectrum.
        decomposer_interp = partial(
            _decomposer_interp, x=abscissa, xp=self._precomputed["abscissa"] / u.cm
        )

        # Create multiprocessing pool.
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        self._matrix = pool.map(decomposer_interp, self._precomputed["matrix"].T)
        pool.close()
        pool.join()
        self._matrix = np.array(self._matrix).T

        # Setup the fitter.
        decomposer_nnls = partial(_decomposer_nnls, m=self._matrix)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

        # Perform the fit.
        weights, _ = list(zip(*pool.map(decomposer_nnls, pool_shape[:, self._mask].T)))
        pool.close()
        pool.join()

        # Set weights.
        self._weights = np.zeros((pool_shape.shape[1], self._matrix.shape[1]))
        self._weights[self._mask] = np.array(weights)

        # Reshape results.
        new_shape = ordinate.shape[1:] + (self._matrix.shape[1],)
        self._weights = np.transpose(np.reshape(self._weights, new_shape), (2, 0, 1))

    def _fit(self):
        """Return the fit.

        Returns:
            self._yfit (quantity.Quantity): The fit.
        """

        # Lazy Instantiation.
        if self._yfit is None:

            decomposer_fit = partial(_decomposer_fit, m=self._matrix)

            # Create multiprocessing pool.
            n_cpus = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=n_cpus - 1)

            # Convenience defintions.
            ordinate = self.spectrum.flux.T
            wt_elements_yz = self._weights.shape[1] * self._weights.shape[2]
            wt_shape = np.reshape(
                self._weights, (self._weights.shape[0], wt_elements_yz)
            )

            # Perform the fit.
            self._yfit = np.zeros((wt_elements_yz, ordinate.shape[0]))
            self._yfit[self._mask, :] = np.array(
                pool.map(decomposer_fit, wt_shape[:, self._mask].T)
            )
            pool.close()
            pool.join()

            # Reshape results.
            new_shape = ordinate.shape[1:] + (ordinate.shape[0],)
            self._yfit = np.transpose(np.reshape(self._yfit, new_shape), (2, 0, 1))

            # Set units.
            self._yfit *= self.spectrum.flux.unit

        return self._yfit

    def _error(self):
        """Return the error as ∫|residual|dν / ∫observation dν.

        Returns:
            self._yerror (quantity.Quantity): The fit error.
        """

        # Lazy Instantiation.
        if self._yerror is None:

            # Convert units of spectral_axis to wavenumber.
            abscissa = self.spectrum.spectral_axis.to(
                1.0 / u.cm, equivalencies=u.spectral()
            )

            # Convenience defintion.
            ordinate = self.spectrum.flux.T

            # Use Trapezium rule to integrate the absolute of the residual
            # and the observations.
            abs_residual = np.trapz(np.abs(self.fit - ordinate), x=abscissa, axis=0)

            total = np.trapz(ordinate, x=abscissa, axis=0)

            # Initialize result to NaN.
            self._yerror = np.empty(ordinate.shape[1:])
            self._yerror.fill(np.nan)

            # Avoid division by -zero-.
            nonzero = np.nonzero(total)

            # Calculate the error.
            self._yerror[nonzero] = abs_residual[nonzero] / total[nonzero]

            # Set units.
            self._yerror *= u.dimensionless_unscaled

        return self._yerror

    def _get_ionized_fraction(self):
        """Return the ionized fraction.

        Returns:
            self._ionized_fraction (quantity.Quantity): Ionized fraction from
            fit.
        """

        # Lazy Instantiation.
        if self._ionized_fraction is None:

            # Compute ionized fraction.
            charge_matrix = self._precomputed["properties"]["charge"]
            ions = (charge_matrix > 0).astype(float)[:, None, None]
            self._ionized_fraction = np.sum(self._weights * ions, axis=0)
            self._ionized_fraction *= u.dimensionless_unscaled

            nonzero = np.nonzero(self._ionized_fraction)

            # Update ionized fraction.
            neutrals = (charge_matrix == 0).astype(float)[:, None, None]
            neutrals_wt = (np.sum(self._weights * neutrals, axis=0))[nonzero]
            self._ionized_fraction[nonzero] /= (
                self._ionized_fraction[nonzero] + neutrals_wt
            )

        return self._ionized_fraction

    def _get_large_fraction(self):
        """Return the large fraction.

        Returns:
            self._large_fraction (quantity.Quantity): Large fraction from fit.
        """

        # Lazy Instantiation.
        if self._large_fraction is None:

            # Compute large fraction.
            size_matrix = self._precomputed["properties"]["size"]
            large = (size_matrix > 40).astype(float)[:, None, None]
            self._large_fraction = np.sum(self._weights * large, axis=0)
            self._large_fraction *= u.dimensionless_unscaled

            nonzero = np.nonzero(self._large_fraction)

            # Update the large fraction.
            small = (size_matrix <= 40).astype(float)[:, None, None]
            small_wt = (np.sum(self._weights * small, axis=0))[nonzero]
            self._large_fraction[nonzero] /= self._large_fraction[nonzero] + small_wt

        return self._large_fraction

    def _get_charge(self):
        """Return the spectral charge breakdown from fit.

        Returns:
            self._charge (dictionary): Dictionary with keys
            'anion', 'neutral' and 'cation'.
        """

        # TODO: Should self._charge be a Spectrum1D-object?

        # Lazy Instantiation.
        if self._charge is None:

            decomposer_anion = partial(
                _decomposer_anion,
                m=self._matrix,
                p=self._precomputed["properties"]["charge"],
            )
            decomposer_neutral = partial(
                _decomposer_neutral,
                m=self._matrix,
                p=self._precomputed["properties"]["charge"],
            )
            decomposer_cation = partial(
                _decomposer_cation,
                m=self._matrix,
                p=self._precomputed["properties"]["charge"],
            )

            # Create multiprocessing pool.
            n_cpus = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=n_cpus - 1)

            # Convenience definitions.
            wt_shape_yz = self._weights.shape[1] * self._weights.shape[2]
            new_dims = np.reshape(self._weights, (self._weights.shape[0], wt_shape_yz))
            ordinate = self.spectrum.flux.T
            mappings = {
                "anion": decomposer_anion,
                "neutral": decomposer_neutral,
                "cation": decomposer_cation,
            }

            # Map the charge arrays.
            self._charge = {
                charge: np.zeros((wt_shape_yz, ordinate.shape[0]))
                for charge in mappings.keys()
            }
            for charge, func in mappings.items():
                self._charge[charge][self._mask, :] = np.array(
                    pool.map(func, new_dims[:, self._mask].T)
                )
            pool.close()
            pool.join()

            # Reshape results and set units.
            interior = ordinate.shape[1:] + (ordinate.shape[0],)
            for charge, spectrum in self._charge.items():
                self._charge[charge] = (
                    np.transpose(np.reshape(spectrum, interior), (2, 0, 1))
                    * self.spectrum.flux.unit
                )

        return self._charge

    def _get_size(self):
        """Return the spectral size breakdown from fit.

        Returns:
            self._size (dictionary): Dictionary with keys
            'large', 'small'.
        """

        # TODO: Should self._size be a Spectrum1D-object?

        # Lazy Instantiation.
        if self._size is None:
            decomposer_large = partial(
                _decomposer_large,
                m=self._matrix,
                p=self._precomputed["properties"]["size"],
            )
            decomposer_small = partial(
                _decomposer_small,
                m=self._matrix,
                p=self._precomputed["properties"]["size"],
            )

            # Create multiprocessing pool.
            n_cpus = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=n_cpus - 1)

            # Convenience definitions.
            wt_shape_yz = self._weights.shape[1] * self._weights.shape[2]
            new_dims = np.reshape(self._weights, (self._weights.shape[0], wt_shape_yz))
            ordinate = self.spectrum.flux.T
            mappings = {
                "small": decomposer_small,
                "large": decomposer_large,
            }

            # Map the size arrays.
            self._size = {
                size: np.zeros((wt_shape_yz, ordinate.shape[0]))
                for size in mappings.keys()
            }
            for size, func in mappings.items():
                self._size[size][self._mask, :] = np.array(
                    pool.map(func, new_dims[:, self._mask].T)
                )
            pool.close()
            pool.join()

            # Reshape results and set units.
            interior = ordinate.shape[1:] + (ordinate.shape[0],)
            for size, spectrum in self._size.items():
                self._size[size] = (
                    np.transpose(np.reshape(spectrum, interior), (2, 0, 1))
                    * self.spectrum.flux.unit
                )

        return self._size

    # Make fit a property.
    fit = property(_fit)

    # Make error a property.
    error = property(_error)

    # Make ionized_fraction a property.
    ionized_fraction = property(_get_ionized_fraction)

    # Make large_fraction a property.
    large_fraction = property(_get_large_fraction)

    # Make charge a property.
    charge = property(_get_charge)

    # Make size a property for.
    size = property(_get_size)
