#!/usr/bin/env python3
"""
decomposer_base.py

Using a precomputed matrix of theoretically calculated
PAH emission spectra, an input spectrum is fitted and decomposed into
contributing PAH subclasses using a NNLS-approach.

This file is part of pypahdb - see the module docs for more
information.
"""

import multiprocessing
import pickle
import platform
import pkg_resources
from functools import partial
from astropy import units as u
from specutils import Spectrum1D

import numpy as np
from scipy import optimize


def _decomposer_anion(w, m=None, p=None):
    """Do the actual anion decomposition for multiprocessing"""
    return m.dot(w * (p < 0).astype(float))


def _decomposer_neutral(w, m=None, p=None):
    """Do the actual neutral decomposition for multiprocessing"""
    return m.dot(w * (p == 0).astype(float))


def _decomposer_cation(w, m=None, p=None):
    """Do the actual cation decomposition for multiprocessing"""
    return m.dot(w * (p > 0).astype(float))


def _decomposer_large(w, m=None, p=None):
    """Do the actual large decomposition for multiprocessing"""
    return m.dot(w * (p > 40).astype(float))


def _decomposer_small(w, m=None, p=None):
    """Do the actual small decomposition for multiprocessing"""
    return m.dot(w * (p <= 40).astype(float))


def _decomposer_fit(w, m=None):
    """Do the actual matrix manipulation for multiprocessing"""
    return m.dot(w)


def _decomposer_interp(fp, x=None, xp=None):
    """Do the actual interpolation for multiprocessing"""
    return np.interp(x, xp, fp)


def _decomposer_nnls(y, m=None):
    """Do the actual nnls for multiprocessing"""
    return optimize.nnls(m, y)


class DecomposerBase(object):
    """Fits and decomposes a spectrum.

    Attributes:
       spectrum: A spectrum to fit and decompose.
    """

    def __init__(self, spectrum):
        """Construct a decomposer object.

        Args:
            spectrum (specutil.Spectrum1D): The spectrum to fit and decompose.
        """
        self._yfit = None
        self._ionized_fraction = None
        self._large_fraction = None
        self._charge = None
        self._size = None

        # Check if spectrum is a Spectrum1D
        if not isinstance(spectrum, Spectrum1D):
            print("spectrum is not a specutils.Spectrum1D")
            return None

        self.spectrum = spectrum

        # Convert units of spectrum to wavenumber and flux (density)
        abscissa = self.spectrum.spectral_axis.to(1.0 / u.cm,
                                                  equivalencies=u.spectral())
        try:
            ordinate = self.spectrum.flux.to(u.Unit("MJy/sr"),
                                             equivalencies=u.spectral()).T
        except u.UnitConversionError:
            ordinate = self.spectrum.flux.to(u.Unit("Jy"),
                                             equivalencies=u.spectral()).T
            pass

        # Retrieve the precomputed data
        # Raise error if file is not found
        file_name = 'resources/precomputed.pkl'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)
        with open(file_path, 'rb') as f:
            try:
                self._precomputed = pickle.load(f, encoding='latin1')
            except Exception as e:
                print('Python 3 is required for pypahdb.')
                raise(e)

        # Deal with having no map; have a threshold when to do in for loop?

        # Linearly interpolate the precomputed spectra onto the
        # frequency grid of the input spectrum
        decomposer_interp = partial(_decomposer_interp,
                                    x=abscissa,
                                    xp=self._precomputed['abscissa'] / u.cm)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        self._matrix = pool.map(decomposer_interp,
                                self._precomputed['matrix'].T)
        pool.close()
        pool.join()
        self._matrix = np.array(self._matrix).T

        # Perform the fit
        decomposer_nnls = partial(_decomposer_nnls, m=self._matrix)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

        # For clarity, define a few quantities.
        n_elements_yz = ordinate.shape[1] * ordinate.shape[2]
        pool_shape = np.reshape(ordinate, (ordinate.shape[0], n_elements_yz))

        # Perform the fit.
        yfit = pool.map(decomposer_nnls, pool_shape.T)
        pool.close()
        pool.join()

        # Determine the weights and norm.
        new_shape = (ordinate.shape[1:] + (self._matrix.shape[1],))
        self._weights, self.norm = list(zip(*yfit))
        self._weights = \
            np.transpose(np.reshape(self._weights, new_shape), (2, 0, 1))
        self.norm = np.reshape(self.norm,
                               (ordinate.shape[2],
                                ordinate.shape[1])).T
        self.norm *= u.dimensionless_unscaled

    def _fit(self):
        """Return the fit.

        Returns:
            self._yfit (quantity.Quantity): PAHdb total fit.
        """

        # Lazy Instantiation
        if self._yfit is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_fit = partial(_decomposer_fit, m=self._matrix)
                n_cpus = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=n_cpus - 1)

                # Convenience defintions.
                ordinate = self.spectrum.flux.T
                wt_elements_yz = \
                    self._weights.shape[1] * self._weights.shape[2]
                wt_shape = np.reshape(self._weights,
                                      (self._weights.shape[0], wt_elements_yz))

                # Perform fit.
                self._yfit = pool.map(decomposer_fit, wt_shape.T)
                pool.close()
                pool.join()

                # Reshape the results.
                new_shape = (ordinate.shape[1:] + (ordinate.shape[0],))
                self._yfit = \
                    np.transpose(np.reshape(self._yfit, new_shape), (2, 0, 1))

            else:
                ordinate = self.spectrum.flux.T
                self._yfit = np.zeros(ordinate.shape)
                for i in range(ordinate.shape[1]):
                    for j in range(ordinate.shape[2]):
                        self._yfit[:, i, j] = \
                            self._matrix.dot(self._weights[:, i, j])

            # Set the units
            self._yfit *= self.spectrum.flux.unit

        return self._yfit

    def _get_ionized_fraction(self):
        """Return the ionized fraction.

        Returns:
            self._ionized_fraction (quantity.Quantity): Ion fraction of fit.
        """

        # Lazy Instantiation
        if self._ionized_fraction is None:

            # Compute ionized fraction.
            charge_matrix = self._precomputed['properties']['charge']
            ions = (charge_matrix > 0).astype(float)[:, None, None]
            self._ionized_fraction = np.sum(self._weights * ions, axis=0)
            self._ionized_fraction *= u.dimensionless_unscaled

            nonzero = np.nonzero(self._ionized_fraction)

            # Update ionized fraction.
            neutrals = (charge_matrix == 0).astype(float)[:, None, None]
            neutrals_wt = (np.sum(self._weights * neutrals, axis=0))[nonzero]
            self._ionized_fraction[nonzero] /= \
                self._ionized_fraction[nonzero] + neutrals_wt

        return self._ionized_fraction

    def _get_large_fraction(self):
        """Return the large fraction.

        Returns:
            self._large_fraction (quantity.Quantity): Large fraction of fit.
        """

        # Lazy Instantiation
        if self._large_fraction is None:

            # Compute large fraction.
            size_matrix = self._precomputed['properties']['size']
            large = (size_matrix > 40).astype(float)[:, None, None]
            self._large_fraction = np.sum(self._weights * large, axis=0)
            self._large_fraction *= u.dimensionless_unscaled

            nonzero = np.nonzero(self._large_fraction)

            # Update the large fraction.
            small = (size_matrix <= 40).astype(float)[:, None, None]
            small_wt = (np.sum(self._weights * small, axis=0))[nonzero]
            self._large_fraction[nonzero] /= \
                self._large_fraction[nonzero] + small_wt

        return self._large_fraction

    def _get_charge(self):
        """Return the spectral charge breakdown.

        Returns:
            self._charge (dictionary): Associative array with keys
                'anion', 'neutral' and 'cation'

        Todo:
            self._charge should be a Spectrum1D-object
        """

        # Lazy Instantiation
        if self._charge is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_anion = \
                    partial(_decomposer_anion, m=self._matrix,
                            p=self._precomputed['properties']['charge'])
                decomposer_neutral = \
                    partial(_decomposer_neutral, m=self._matrix,
                            p=self._precomputed['properties']['charge'])
                decomposer_cation = \
                    partial(_decomposer_cation, m=self._matrix,
                            p=self._precomputed['properties']['charge'])

                n_cpus = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=n_cpus - 1)

                # Conveniences for below.
                wt_shape_yz = self._weights.shape[1] * self._weights.shape[2]
                new_dims = np.reshape(self._weights,
                                      (self._weights.shape[0], wt_shape_yz))

                # Map the charge arrays.
                anion = pool.map(decomposer_anion, new_dims.T)
                neutral = pool.map(decomposer_neutral, new_dims.T)
                cation = pool.map(decomposer_cation, new_dims.T)

                pool.close()
                pool.join()

                # Reshape the charge arrays.
                ordinate = self.spectrum.flux.T
                interior = (ordinate.shape[1:] +
                            (ordinate.shape[0],))
                new_anion = \
                    np.transpose(np.reshape(anion, interior), (2, 0, 1))
                new_neut = \
                    np.transpose(np.reshape(neutral, interior), (2, 0, 1))
                new_cat = \
                    np.transpose(np.reshape(cation, interior), (2, 0, 1))

                self._charge = {'anion': new_anion,
                                'neutral': new_neut,
                                'cation': new_cat}

            else:
                ordinate = self.spectrum.flux.T
                self._charge = {'anion': np.zeros(ordinate.shape),
                                'neutral': np.zeros(ordinate.shape),
                                'cation': np.zeros(ordinate.shape)}

                charge_matrix = self._precomputed['properties']['charge']

                for i in range(ordinate.shape[1]):
                    for j in range(ordinate.shape[2]):

                        # Charge weights.
                        wt_anion = self._weights[:, i, j] * \
                            (charge_matrix < 0).astype(float)
                        wt_neut = self._weights[:, i, j] * \
                            (charge_matrix == 0).astype(float)
                        wt_cat = self._weights[:, i, j] * \
                            (charge_matrix > 0).astype(float)

                        # Compute dot product.
                        dot_wt_anion = self._matrix.dot(wt_anion)
                        dot_wt_neut = self._matrix.dot(wt_neut)
                        dot_wt_cat = self._matrix.dot(wt_cat)

                        # Fill arrays.
                        self._charge['anion'][:, i, j] = dot_wt_anion
                        self._charge['neutral'][:, i, j] = dot_wt_neut
                        self._charge['cation'][:, i, j] = dot_wt_cat

            # Set the units
            self._charge['anion'] *= self.spectrum.flux.unit
            self._charge['neutral'] *= self.spectrum.flux.unit
            self._charge['cation'] *= self.spectrum.flux.unit

        return self._charge

    def _get_size(self):
        """Return the spectral size breakdown.

        Returns:
            self._size (dictionary): Associative array with keys
                'large', 'small'

        Todo:
            self._charge should be a Spectrum1D-object
        """

        # Lazy Instantiation
        if self._size is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_large = \
                    partial(_decomposer_large, m=self._matrix,
                            p=self._precomputed['properties']['size'])
                decomposer_small = \
                    partial(_decomposer_small, m=self._matrix,
                            p=self._precomputed['properties']['size'])

                # Create pool.
                n_cpus = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=n_cpus - 1)

                # Using weights, map for large, small PAHs.
                wt_shape_yz = self._weights.shape[1] * self._weights.shape[2]
                new_shape = np.reshape(self._weights,
                                       (self._weights.shape[0], wt_shape_yz))
                large = pool.map(decomposer_large, new_shape.T)
                small = pool.map(decomposer_small, new_shape.T)
                pool.close()
                pool.join()

                # Reshape the outputs.
                ordinate = self.spectrum.flux.T
                ord_shape_yz = (ordinate.shape[1:] + (ordinate.shape[0],))
                new_large = \
                    np.transpose(np.reshape(large, ord_shape_yz), (2, 0, 1))
                new_small = \
                    np.transpose(np.reshape(small, ord_shape_yz), (2, 0, 1))

                self._size = {'large': new_large,
                              'small': new_small}

            else:
                ordinate = self.spectrum.flux.T
                self._size = {'large': np.zeros(ordinate.shape),
                              'small': np.zeros(ordinate.shape)}

                size_matrix = self._precomputed['properties']['size']

                for i in range(ordinate.shape[1]):
                    for j in range(ordinate.shape[2]):

                        large_wt = self._weights[:, i, j] * \
                            (size_matrix > 40).astype(float)
                        small_wt = self._weights[:, i, j] * \
                            (size_matrix <= 40).astype(float)

                        large_amount = self._matrix.dot(large_wt)
                        small_amount = self._matrix.dot(small_wt)

                        self._size['large'][:, i, j] = large_amount
                        self._size['small'][:, i, j] = small_amount

            # Set the units
            self._size['large'] *= self.spectrum.flux.unit
            self._size['small'] *= self.spectrum.flux.unit

        return self._size

    # Make fit a property for easy access
    fit = property(_fit)

    # Make ionized_fraction a property for easy access
    ionized_fraction = property(_get_ionized_fraction)

    # Make large_fraction a property for easy access
    large_fraction = property(_get_large_fraction)

    # Make charge a property for easy access
    charge = property(_get_charge)

    # Make size a property for easy access
    size = property(_get_size)
