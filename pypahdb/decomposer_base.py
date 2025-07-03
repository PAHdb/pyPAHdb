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
import os
import pickle
from functools import cached_property, partial
from urllib.request import urlretrieve

import importlib_resources
import numpy as np
from astropy import units as u
from fnnls import fnnls
from specutils import Spectrum1D
from tqdm import tqdm

SMALL_SIZE = 50
MEDIUM_SIZE = 70


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
    return m.dot(w * (p > MEDIUM_SIZE).astype(float))


def _decomposer_medium(w, m=None, p=None):
    """Do the actual large decomposition in multiprocessing."""
    return m.dot(w * ((p > SMALL_SIZE) & (p <= MEDIUM_SIZE)).astype(float))


def _decomposer_small(w, m=None, p=None):
    """Do the small decomposition in multiprocessing."""
    return m.dot(w * (p <= 50).astype(float))


def _decomposer_fit(w, m=None):
    """Do the matrix manipulation to obtain the total fit in
    multiprocessing."""
    return m.dot(w)


def _decomposer_interp(fp, x=None, xp=None):
    """Do the grid interpolation in multiprocessing."""
    return np.interp(x, xp, fp)


def _decomposer_nnls(y, m=None):
    """Do the NNLS in multiprocessing."""
    return fnnls(m, y)


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
        self._mask = np.sum(pool_shape, axis=0) > 0.0
        if np.all(self._mask is False):
            print("spectral data is all zeros.")
            return None

        # Download the precomputed data if not present
        remote_pkl = "https://www.astrochemistry.org/pahdb/pypahdb/pickle.php"
        if os.getenv("GITHUB_ACTIONS") == "true":
            remote_pkl += "?github_actions=true"
        local_pkl = importlib_resources.files("pypahdb") / "resources/precomputed.pkl"
        if not os.path.isfile(local_pkl):

            def hook(t):
                last_b = [0]

                def inner(b=1, bsize=1, tsize=None):
                    if tsize is not None:
                        t.total = tsize
                    t.update((b - last_b[0]) * bsize)
                    last_b[0] = b

                return inner

            print("downloading pre-computed matrix")
            with tqdm(
                unit="B",
                unit_scale=True,
                leave=True,
                miniters=1,
            ) as t:
                urlretrieve(
                    remote_pkl, filename=local_pkl, reporthook=hook(t), data=None
                )

        with open(local_pkl, "rb") as f:
            self._precomputed = pickle.load(f, encoding="latin1")

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

        # Copy and normalize the matrix.
        m = self._matrix.copy()
        m_scl = m.max()
        m /= m_scl

        # Normalize spectral input.
        b_scl = np.max(pool_shape, axis=0).value
        np.divide(pool_shape, b_scl[None, :], out=pool_shape, where=self._mask)

        # Setup the fitter.
        decomposer_nnls = partial(_decomposer_nnls, m=m)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

        # Perform the fit.
        weights, _ = list(zip(*pool.map(decomposer_nnls, pool_shape[:, self._mask].T)))
        pool.close()
        pool.join()

        # Scale weights back.
        weights = np.array(weights)
        weights /= m_scl / b_scl[self._mask, None]

        # Set weights.
        self._weights = np.zeros((pool_shape.shape[1], self._matrix.shape[1]))
        self._weights[self._mask] = weights

        # Reshape results.
        new_shape = ordinate.shape[1:] + (self._matrix.shape[1],)
        self._weights = np.transpose(np.reshape(self._weights, new_shape), (2, 0, 1))

    @cached_property
    def fit(self):
        """Return the fit.

        Returns:
            quantity.Quantity: The fit.
        """

        decomposer_fit = partial(_decomposer_fit, m=self._matrix)

        # Create multiprocessing pool.
        n_cpus = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=n_cpus - 1)

        # Convenience defintions.
        ordinate = self.spectrum.flux.T
        wt_elements_yz = self._weights.shape[1] * self._weights.shape[2]
        wt_shape = np.reshape(self._weights, (self._weights.shape[0], wt_elements_yz))

        # Perform the fit.
        yfit = np.zeros((wt_elements_yz, ordinate.shape[0]))
        yfit[self._mask, :] = np.array(
            pool.map(decomposer_fit, wt_shape[:, self._mask].T)
        )
        pool.close()
        pool.join()

        # Reshape results.
        new_shape = ordinate.shape[1:] + (ordinate.shape[0],)
        yfit = np.transpose(np.reshape(yfit, new_shape), (2, 0, 1))

        # Set units.
        yfit *= self.spectrum.flux.unit

        return yfit

    @cached_property
    def error(self):
        """Return the error as ∫|residual|dν / ∫observation dν.

        Returns:
            quantity.Quantity: The fit error.
        """

        # Convert units of spectral_axis to wavenumber.
        abscissa = self.spectrum.spectral_axis.to(
            1.0 / u.cm, equivalencies=u.spectral()
        )

        # Convenience definition.
        ordinate = self.spectrum.flux.T

        # Use Trapezium rule to integrate the absolute of the residual
        # and the observations.
        abs_residual = np.trapz(np.abs(self.fit - ordinate), x=abscissa, axis=0)

        total = np.trapz(ordinate, x=abscissa, axis=0)

        # Initialize result to NaN.
        yerror = np.empty(ordinate.shape[1:])
        yerror.fill(np.nan)

        # Avoid division by -zero-.
        nonzero = np.nonzero(total)

        # Calculate the error.
        yerror[nonzero] = abs_residual[nonzero] / total[nonzero]

        # Set units.
        yerror *= u.dimensionless_unscaled

        return yerror

    @cached_property
    def charge_fractions(self):
        """Return the charge fraction.

        Returns:
            dict: Fraction of neutral,
            cation and anion PAHs from fit.
        """

        # Compute ionized fraction.
        charge_matrix = self._precomputed["properties"]["charge"]
        neutrals = (charge_matrix == 0).astype(float)[:, None, None]
        cations = (charge_matrix > 0).astype(float)[:, None, None]
        anions = (charge_matrix < 0).astype(float)[:, None, None]
        neutral_fraction = np.sum(self._weights * neutrals, axis=0)
        cation_fraction = np.sum(self._weights * cations, axis=0)
        anion_fraction = np.sum(self._weights * anions, axis=0)
        neutral_fraction *= u.dimensionless_unscaled
        cation_fraction *= u.dimensionless_unscaled
        anion_fraction *= u.dimensionless_unscaled

        charge_sum = neutral_fraction + cation_fraction + anion_fraction
        nonzero = np.nonzero(charge_sum)

        neutral_fraction[nonzero] /= charge_sum[nonzero]
        cation_fraction[nonzero] /= charge_sum[nonzero]
        anion_fraction[nonzero] /= charge_sum[nonzero]

        # Make dictionary of charge fractions.
        charge_fractions = {
            "neutral": neutral_fraction,
            "cation": cation_fraction,
            "anion": anion_fraction,
        }

        return charge_fractions

    @cached_property
    def nc(self):
        """Return the average number of carbon atoms.

        Returns:
            quantity.Quantity: Average number of carbon atoms
        """

        # Compute average number of carbon atoms.
        nc = np.zeros(self._weights.shape[1:])
        size_array = self._precomputed["properties"]["size"]
        size = size_array.astype(float)[:, None, None]
        nc_sum = np.sum(self._weights, axis=0)
        np.divide(
            np.sum(self._weights * size, axis=0),
            nc_sum,
            out=nc,
            where=nc_sum != 0,
        )
        nc *= u.dimensionless_unscaled

        return nc

    @cached_property
    def size_fractions(self):
        """Return the size fraction.

        Returns:
           dict: Size fractions from fit.
        """

        # Compute large fraction.
        size_matrix = self._precomputed["properties"]["size"]
        large = (size_matrix > MEDIUM_SIZE).astype(float)[:, None, None]
        large_fraction = np.sum(self._weights * large, axis=0)
        large_fraction *= u.dimensionless_unscaled

        # Compute medium fraction between 50 and 70.
        medium = ((size_matrix > SMALL_SIZE) & (size_matrix <= MEDIUM_SIZE)).astype(
            float
        )[:, None, None]
        medium_fraction = np.sum(self._weights * medium, axis=0)
        medium_fraction *= u.dimensionless_unscaled

        # Compute small fraction between 20 and 50.
        small = (size_matrix <= SMALL_SIZE).astype(float)[:, None, None]
        small_fraction = np.sum(self._weights * small, axis=0)
        small_fraction *= u.dimensionless_unscaled

        size_sum = large_fraction + medium_fraction + small_fraction
        nonzero = np.nonzero(size_sum)

        # Update the size fractions.
        large_fraction[nonzero] /= size_sum[nonzero]
        medium_fraction[nonzero] /= size_sum[nonzero]
        small_fraction[nonzero] /= size_sum[nonzero]

        # Make dictionary of size fractions.
        size_fractions = {
            "large": large_fraction,
            "medium": medium_fraction,
            "small": small_fraction,
        }

        return size_fractions

    @cached_property
    def charge(self):
        """Return the spectral charge breakdown from fit.

        Returns:
            dict: Dictionary with keys
            'anion', 'neutral' and 'cation'.
        """

        # TODO: Should self._charge be a Spectrum1D-object?

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
        charge = {
            charge: np.zeros((wt_shape_yz, ordinate.shape[0]))
            for charge in mappings.keys()
        }
        for c, func in mappings.items():
            charge[c][self._mask, :] = np.array(
                pool.map(func, new_dims[:, self._mask].T)
            )
        pool.close()
        pool.join()

        # Reshape results and set units.
        interior = ordinate.shape[1:] + (ordinate.shape[0],)
        for c, spectrum in charge.items():
            charge[c] = (
                np.transpose(np.reshape(spectrum, interior), (2, 0, 1))
                * self.spectrum.flux.unit
            )

        return charge

    @cached_property
    def size(self):
        """Return the spectral size breakdown from fit.

        Returns:
            dict: Dictionary with keys
            'large', 'medium', 'small'.
        """

        # TODO: Should self._size be a Spectrum1D-object?

        decomposer_large = partial(
            _decomposer_large,
            m=self._matrix,
            p=self._precomputed["properties"]["size"],
        )
        decomposer_medium = partial(
            _decomposer_medium,
            m=self._matrix,
            p=self._precomputed["properties"]["size"],
        )
        decomposer_small = partial(
            _decomposer_small,
            m=self._matrix,
            p=self._precomputed["properties"]["size"],
        )

        # Convenience definitions.
        wt_shape_yz = self._weights.shape[1] * self._weights.shape[2]
        new_dims = np.reshape(self._weights, (self._weights.shape[0], wt_shape_yz))
        ordinate = self.spectrum.flux.T
        mappings = {
            "small": decomposer_small,
            "medium": decomposer_medium,
            "large": decomposer_large,
        }

        # Map the size arrays.
        size = {
            size: np.zeros((wt_shape_yz, ordinate.shape[0])) for size in mappings.keys()
        }

        # Create multiprocessing pool.
        n_cpus = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=n_cpus - 1)

        for s, func in mappings.items():
            size[s][self._mask, :] = np.array(pool.map(func, new_dims[:, self._mask].T))
        pool.close()
        pool.join()

        # Reshape results and set units.
        interior = ordinate.shape[1:] + (ordinate.shape[0],)
        for s, spectrum in size.items():
            size[s] = (
                np.transpose(np.reshape(spectrum, interior), (2, 0, 1))
                * self.spectrum.flux.unit
            )

        return size

    @cached_property
    def mask(self):
        """Return the computed mask."""
        return self._mask.reshape(self._weights.shape[1:])
