#!/usr/bin/env python3
"""
decomposer_base.py

Using a precomputed matrix of theoretically calculated
PAH emission spectra, an input spectrum is fitted and decomposed into
contributions from PAH subclasses using a nnls-approach.

This file is part of pypahdb - see the module docs for more
information.
"""

import copy
import multiprocessing
import numpy as np
import pickle
import platform
import pkg_resources
import sys

from functools import partial
from scipy import optimize


class DecomposerBase(object):
    """Fits and decomposes a spectrum.

    Attributes:
       spectrum: The spectrum to fit and decompose.
    """

    def __init__(self, spectrum):
        """Construct a decomposer object.

        Args:
            spectrum (object): The spectrum to fit and decompose
        """
        self._yfit = None
        self._ionized_fraction = None
        self._large_fraction = None
        self._charge = None
        self._size = None

        # Make a deep copy in case spectrum gets altered outside self
        self.spectrum = copy.deepcopy(spectrum)

        # Convert units of spectrum to wavenumber and flux density
        self.spectrum.convertunitsto(aunits='wavenumbers',
                                     ounits='flux density')

        # Retrieve the precomputed data
        # Raise error if file is not found?
        file_name = 'data/precomputed.pkl'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)
        with open(file_path, 'rb') as f:
            if sys.version_info[0] == 2:
                self._precomputed = pickle.load(f)
            elif sys.version_info[0] == 3:
                self._precomputed = pickle.load(f, encoding='latin1')

        # Deal with having no map; have a threshold when to do in for loop?

        # Linearly interpolate the precomputed spectra onto the
        # frequency grid of the input spectrum
        decomposer_interp = partial(self._decomposer_interp,
                                    x=self.spectrum.abscissa,
                                    xp=self._precomputed['abscissa'])
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        self._matrix = pool.map(decomposer_interp,
                                self._precomputed['matrix'].T)
        pool.close()
        pool.join()
        self._matrix = np.array(self._matrix).T

        # Perform the fit
        decomposer_nnls = partial(self._decomposer_nnls, m=self._matrix)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

        # For clarity, define a few quantities.
        ordd = self.spectrum.ordinate
        n_elements_yz = ordd.shape[1] * ordd.shape[2]
        pool_shape = np.reshape(ordd, (ordd.shape[0], n_elements_yz))

        # Perform the fit.
        yfit = pool.map(decomposer_nnls, pool_shape.T)
        pool.close()
        pool.join()

        # Determine the weights and norm.
        new_shape = (ordd.shape[1:] + (self._matrix.shape[1],))
        self._weights, self.norm = list(zip(*yfit))
        self._weights = \
            np.transpose(np.reshape(self._weights, new_shape), (2, 0, 1))
        self.norm = np.reshape(self.norm, (ordd.shape[2], ordd.shape[1])).T

    def _decomposer_anion(self, w, m=None, p=None):
        """Do the actual anion decomposition for multiprocessing"""
        return m.dot(w * (p < 0).astype(float))

    def _decomposer_neutral(self, w, m=None, p=None):
        """Do the actual neutral decomposition for multiprocessing"""
        return m.dot(w * (p == 0).astype(float))

    def _decomposer_cation(self, w, m=None, p=None):
        """Do the actual cation decomposition for multiprocessing"""
        return m.dot(w * (p > 0).astype(float))

    def _decomposer_large(self, w, m=None, p=None):
        """Do the actual large decomposition for multiprocessing"""
        return m.dot(w * (p > 40).astype(float))

    def _decomposer_small(self, w, m=None, p=None):
        """Do the actual small decomposition for multiprocessing"""
        return m.dot(w * (p <= 40).astype(float))

    def _decomposer_fit(self, w, m=None):
        """Do the actual matrix manipulation for multiprocessing"""
        return m.dot(w)

    def _decomposer_interp(self, fp, x=None, xp=None):
        """Do the actual interpolation for multiprocessing"""
        return np.interp(x, xp, fp)

    def _decomposer_nnls(self, y, m=None):
        """Do the actual nnls for multiprocessing"""
        return optimize.nnls(m, y)

    def _fit(self):
        """Return the fit.

        Returns:
            self._yfit (ndarray): PAHdb total fit.
        """

        # Lazy Instantiation
        if self._yfit is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_fit = partial(self._decomposer_fit, m=self._matrix)
                n_cpus = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=n_cpus - 1)

                # Convenience defintions.
                ordd = self.spectrum.ordinate
                wt_elements_yz = \
                    self._weights.shape[1] * self._weights.shape[2]
                wt_shape = np.reshape(self._weights,
                                      (self._weights.shape[0], wt_elements_yz))

                # Perform fit.
                self._yfit = pool.map(decomposer_fit, wt_shape.T)
                pool.close()
                pool.join()

                # Reshape the results.
                new_shape = (ordd.shape[1:] + (ordd.shape[0],))
                self._yfit = \
                    np.transpose(np.reshape(self._yfit, new_shape), (2, 0, 1))

            else:
                self._yfit = np.zeros(self.spectrum.ordinate.shape)
                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):
                        self._yfit[:, i, j] = \
                            self._matrix.dot(self._weights[:, i, j])
        return self._yfit

    def _get_ionized_fraction(self):
        """Return the ionized fraction.

        Returns:
            self._ionized_fraction (ndarray): Ion fraction of fit.
        """

        # Lazy Instantiation
        if self._ionized_fraction is None:

            # Compute ionized fraction.
            charge_matrix = self._precomputed['properties']['charge']
            ions = (charge_matrix > 0).astype(float)[:, None, None]
            self._ionized_fraction = np.sum(self._weights * ions, axis=0)

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
            self._large_fraction (ndarray): Large fraction of fit.
        """

        # Lazy Instantiation
        if self._large_fraction is None:

            # Compute large fraction.
            size_matrix = self._precomputed['properties']['size']
            large = (size_matrix > 40).astype(float)[:, None, None]
            self._large_fraction = np.sum(self._weights * large, axis=0)

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
            self._charge (ndarray): Associative array with keys
                'anion', 'neutral' and 'cation'
        """

        # Lazy Instantiation
        if self._charge is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_anion = \
                    partial(self._decomposer_anion, m=self._matrix,
                            p=self._precomputed['properties']['charge'])
                decomposer_neutral = \
                    partial(self._decomposer_neutral, m=self._matrix,
                            p=self._precomputed['properties']['charge'])
                decomposer_cation = \
                    partial(self._decomposer_cation, m=self._matrix,
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
                interior = (self.spectrum.ordinate.shape[1:] +
                            (self.spectrum.ordinate.shape[0],))
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
                ord_shape = self.spectrum.ordinate.shape
                self._charge = {'anion': np.zeros(ord_shape),
                                'neutral': np.zeros(ord_shape),
                                'cation': np.zeros(ord_shape)}

                charge_matrix = self._precomputed['properties']['charge']

                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):

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

        return self._charge

    def _get_size(self):
        """Return the spectral size breakdown.

        Returns:
            self._size (ndarray): Associative array with keys
                'large', 'small'
        """

        # Lazy Instantiation
        if self._size is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_large = \
                    partial(self._decomposer_large, m=self._matrix,
                            p=self._precomputed['properties']['size'])
                decomposer_small = \
                    partial(self._decomposer_small, m=self._matrix,
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
                ordd = self.spectrum.ordinate
                ord_shape_yz = (ordd.shape[1:] + (ordd.shape[0],))
                new_large = \
                    np.transpose(np.reshape(large, ord_shape_yz), (2, 0, 1))
                new_small = \
                    np.transpose(np.reshape(small, ord_shape_yz), (2, 0, 1))

                self._size = {'large': new_large,
                              'small': new_small}

            else:
                self._size = {'large': np.zeros(self.spectrum.ordinate.shape),
                              'small': np.zeros(self.spectrum.ordinate.shape)}
                size_matrix = self._precomputed['properties']['size']

                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):

                        large_wt = self._weights[:, i, j] * \
                            (size_matrix > 40).astype(float)
                        small_wt = self._weights[:, i, j] * \
                            (size_matrix <= 40).astype(float)

                        large_amount = self._matrix.dot(large_wt)
                        small_amount = self._matrix.dot(small_wt)

                        self._size['large'][:, i, j] = large_amount
                        self._size['small'][:, i, j] = small_amount

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
