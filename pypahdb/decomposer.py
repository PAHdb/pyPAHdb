#!/usr/bin/env python
# decomposer.py

"""decomposer.py: Using a precomputed matrix of theoretically calculated
PAH emission spectra, an input spectrum is fitted and decomposed into
contributions from PAH subclasses using a nnls-approach.

This file is part of pypahdb - see the module docs for more
information.
"""

from os import path

import copy
import sys
import platform
import multiprocessing
import pickle

from functools import partial
from scipy import optimize

import numpy as np

def _decomposer_anion(w, m=None, p=None):
   """Do the actual anion decomposition for multiprocessing"""
   return  m.dot(w * (p < 0).astype(float))

def _decomposer_neutral(w, m=None, p=None):
   """Do the actual neutral decomposition for multiprocessing"""
   return  m.dot(w * (p ==  0).astype(float))

def _decomposer_cation(w, m=None, p=None):
   """Do the actual cation decomposition for multiprocessing"""
   return  m.dot(w * (p > 0).astype(float))

def _decomposer_large(w, m=None, p=None):
   """Do the actual large decomposition for multiprocessing"""
   return  m.dot(w * (p > 40).astype(float))

def _decomposer_small(w, m=None, p=None):
   """Do the actual small decomposition for multiprocessing"""
   return  m.dot(w * (p <= 40).astype(float))

def _decomposer_fit(w, m=None):
    """Do the actual matrix manipulation for multiprocessing"""
    return m.dot(w)

def _decomposer_interp(fp, x=None, xp=None):
    """Do the actual interpolation for multiprocessing"""
    return np.interp(x, xp, fp)

def _decomposer_nnls(y, m=None):
    """Do the actual nnls for multiprocessing"""
    return optimize.nnls(m, y)

class decomposer(object):
    """Fits and decomposes a spectrum.

    Attributes:
       spectrum: The spectrum to fit and decompose.
    """
    def __init__(self, spectrum):
        """
        Construct a decomposer object.

        :param spectrum: The spectrum to fit and decompose
        :return: returns None
        """

        self._yfit = None
        self._ionized_fraction = None
        self._large_fraction = None
        self._charge = None
        self._size = None

        # Make a deep copy in case spectrum gets altered outside self
        self.spectrum = copy.deepcopy(spectrum)

        # Convert units of spectrum to wavenumber and flux density
        self.spectrum.convertunitsto(aunits='wavenumbers', ounits='flux density')

        # Retrieve the precomputed data
        # Raise error if file is not found?
        with open(path.join(path.abspath(path.dirname(__file__)), 'data/precomputed.pkl'), 'rb') as f:
            if sys.version_info[0] == 2:
                self._precomputed = pickle.load(f)
            elif sys.version_info[0] == 3:
                self._precomputed = pickle.load(f, encoding='latin1')


        # Deal with having no map; have a threshold when to do in for loop?
        # Linearly interpolate the precomputed spectra onto the
        # frequency grid of the input spectrum
        decomposer_interp = partial(_decomposer_interp, x=self.spectrum.abscissa, xp=self._precomputed['abscissa'])
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        self._matrix = pool.map(decomposer_interp, self._precomputed['matrix'].T)
        pool.close()
        pool.join()
        self._matrix = np.array(self._matrix).T

        # Perform the fit
        decomposer_nnls = partial(_decomposer_nnls, m=self._matrix)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        yfit = pool.map(decomposer_nnls, np.reshape(self.spectrum.ordinate, (self.spectrum.ordinate.shape[0], self.spectrum.ordinate.shape[1] * self.spectrum.ordinate.shape[2])).T)
        pool.close()
        pool.join()
        self._weights, self.norm = list(zip(*yfit))
        self._weights = np.transpose(np.reshape(self._weights, (self.spectrum.ordinate.shape[1:] + (self._matrix.shape[1],))), (2,0,1))
        self.norm = np.reshape(self.norm, (self.spectrum.ordinate.shape[2], self.spectrum.ordinate.shape[1])).T

    def _fit(self):
        """
        Return the fit.

        :return: returns array
        """

        # Lazy Instantiation
        if self._yfit is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                decomposer_fit = partial(_decomposer_fit, m=self._matrix)
                pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
                self._yfit = pool.map(decomposer_fit, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                pool.close()
                pool.join()
                self._yfit = np.transpose(np.reshape(self._yfit, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1))
            else:
                self._yfit = np.zeros(self.spectrum.ordinate.shape)
                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):
                        self._yfit[:,i,j] = self._matrix.dot(self._weights[:,i,j])
        return self._yfit

    def _get_ionized_fraction(self):
        """
        Return the ionized fraction.

        :return: returns array
        """

        # Lazy Instantiation
        if self._ionized_fraction is None:
            self._ionized_fraction = np.sum(self._weights * (self._precomputed['properties']['charge'] > 0).astype(float)[:, None, None], axis=0)
            self._ionized_fraction /= self._ionized_fraction + np.sum(self._weights * (self._precomputed['properties']['charge'] == 0).astype(float)[:, None, None], axis=0)
        return self._ionized_fraction

    def _get_large_fraction(self):
        """
        Return the large fraction.

        :return: returns array
        """

        # Lazy Instantiation
        if self._large_fraction is None:
            self._large_fraction = np.sum(self._weights * (self._precomputed['properties']['size'] > 40).astype(float)[:, None, None], axis=0)
            self._large_fraction /= self._large_fraction + np.sum(self._weights * (self._precomputed['properties']['size'] <= 40).astype(float)[:, None, None], axis=0)
        return self._large_fraction

    def _get_charge(self):
        """Return the spectral charge breakdown.

        :return: returns associative array with keys 'anion', 'neutral' and 'cation'
        """

        # Lazy Instantiation
        if self._charge is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                print platform.system()
                decomposer_anion = partial(_decomposer_anion, m=self._matrix, p=self._precomputed['properties']['charge'])
                decomposer_neutral = partial(_decomposer_neutral, m=self._matrix, p=self._precomputed['properties']['charge'])
                decomposer_cation = partial(_decomposer_cation, m=self._matrix, p=self._precomputed['properties']['charge'])
                pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
                anion = pool.map(decomposer_anion, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                neutral = pool.map(decomposer_neutral, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                cation = pool.map(decomposer_cation, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                pool.close()
                pool.join()
                self._charge = {'anion': np.transpose(np.reshape(anion, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1)),
                                'neutral': np.transpose(np.reshape(neutral, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1)),
                                'cation': np.transpose(np.reshape(cation, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1))}
            else:
                self._charge = {'anion': np.zeros(self.spectrum.ordinate.shape),
                                'neutral': np.zeros(self.spectrum.ordinate.shape),
                                'cation': np.zeros(self.spectrum.ordinate.shape)}
                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):
                        self._charge['anion'][:,i,j] = self._matrix.dot(self._weights[:,i,j] * (self._precomputed['properties']['charge'] < 0).astype(float))
                        self._charge['neutral'][:,i,j] = self._matrix.dot(self._weights[:,i,j] * (self._precomputed['properties']['charge'] == 0).astype(float))
                        self._charge['cation'][:,i,j] = self._matrix.dot(self._weights[:,i,j] * (self._precomputed['properties']['charge'] > 0).astype(float))

        return self._charge

    def _get_size(self):
        """Return the spectral size breakdown.

        :return: returns associative array with keys 'large' and 'small'
        """

        # Lazy Instantiation
        if self._size is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            if platform.system() != "Darwin":
                print platform.system()
                decomposer_large = partial(_decomposer_large, m=self._matrix, p=self._precomputed['properties']['size'])
                decomposer_small = partial(_decomposer_small, m=self._matrix, p=self._precomputed['properties']['size'])
                pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
                large = pool.map(decomposer_large, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                small = pool.map(decomposer_small, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
                pool.close()
                pool.join()
                self._charge = {'large': np.transpose(np.reshape(large, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1)),
                                'small': np.transpose(np.reshape(small, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1))}
            else:
                self._size = {'large': np.zeros(self.spectrum.ordinate.shape),
                              'small': np.zeros(self.spectrum.ordinate.shape)}
                for i in range(self.spectrum.ordinate.shape[1]):
                    for j in range(self.spectrum.ordinate.shape[2]):
                        self._size['large'][:,i,j] = self._matrix.dot(self._weights[:,i,j] * (self._precomputed['properties']['size'] > 40).astype(float))
                        self._size['small'][:,i,j] = self._matrix.dot(self._weights[:,i,j] * (self._precomputed['properties']['size'] <= 40).astype(float))

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
