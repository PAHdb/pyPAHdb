#!/usr/bin/env python
# decomposer.py

"""
decomposer.py: Using a precomputed matrix of theoretically
calculated PAH emission spectra a spectrum is decomposed into
contribution PAH subclasses using a nnls-approach.

This file is part of pypahdb - see the module docs for more
information.
"""

from os import path
import copy
import multiprocessing
import sys

import numpy as np
from functools import partial
from scipy import optimize
# try:
#     import cPickle as pickle
# except ImportError:
import pickle

#from pdb import set_trace as st

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
    """Decomposes a spectrum with PAHdb.

    Attributes:
       spectrum: The decomposed spectrum.
    """
    def __init__(self, spectrum):
        """
        Construct a decomposer object.

        :param spectrum: The spectrum to decompose
        :return: returns nothing
        """

        self._yfit = None
        self._ionized_fraction = None
        self._large_fraction = None

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
        # frequency grid of the spectrum
        decomposer_interp = partial(_decomposer_interp, x=self.spectrum.abscissa, xp=self._precomputed['abscissa'])
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        self._matrix = pool.map(decomposer_interp, self._precomputed['matrix'].T)
        pool.close()
        pool.join()
        self._matrix = np.array(self._matrix).T
        #for i in range(self._precomputed['matrix'].shape[1]):
        #    self._matrix[:,i] = np.interp(self.spectrum.abscissa, self._precomputed['abscissa'], self._precomputed['matrix'][:,i])

        # Perform the fit
        decomposer_nnls = partial(_decomposer_nnls, m=self._matrix)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        yfit = pool.map(decomposer_nnls, np.reshape(self.spectrum.ordinate, (self.spectrum.ordinate.shape[0], self.spectrum.ordinate.shape[1] * self.spectrum.ordinate.shape[2])).T)
        pool.close()
        pool.join()
        self._weights, self.norm = list(zip(*yfit))
        self._weights = np.transpose(np.reshape(self._weights, (self.spectrum.ordinate.shape[1:] + (self._matrix.shape[1],))), (2,0,1))
        self.norm = np.reshape(self.norm, (self.spectrum.ordinate.shape[2], self.spectrum.ordinate.shape[1])).T
        #self._weights = np.zeros((self._precomputed['matrix'].shape[1],) + self.spectrum.ordinate.shape[1:])
        #self.norm = np.zeros(self.spectrum.ordinate.shape[1:])
        #for i in range(self.spectrum.ordinate.shape[1]):
        #    for j in range(self.spectrum.ordinate.shape[2]):
        #        w, n = optimize.nnls(self._matrix, self.spectrum.ordinate[:,i,j])
        #        self._weights[:,i,j] = w
        #        self.norm[i,j] = n


    def _fit(self):
        """
        Return the fitted spectra.

        :return: returns array
        """

        # Lazy Instantiation
        if self._yfit is None:
            ############################################
            # on MacOS np.dot() is not thread safe ... #
            ############################################
            #decomposer_fit = partial(_decomposer_fit, m=self._matrix)
            #pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
            #self._yfit = pool.map(decomposer_fit, np.reshape(self._weights, (self._weights.shape[0], self._weights.shape[1] * self._weights.shape[2])).T)
            #self._yfit = self._matrix.dot(self._weights[:,0,0])
            #pool.close()
            #pool.join()
            #self._yfit = np.transpose(np.reshape(self._yfit, (self.spectrum.ordinate.shape[1:] + (self.spectrum.ordinate.shape[0],))), (2,0,1))

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

    # Make fit a property for easy access
    fit = property(_fit)

    # Make ionized_fraction a property for easy access
    ionized_fraction = property(_get_ionized_fraction)

    # Make large_fraction a property for easy access
    large_fraction = property(_get_large_fraction)
