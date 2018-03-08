#!/usr/bin/env python
# spectrum.py
"""
spectrum.py: Holds a spectrum

This file is part of pypahdb - see the module docs for more
information.
"""

import numpy as np

class spectrum(object):
    """Create a spectrum object.

    Attributes:
        abscissa (numpy.ndarray): The abscissa values.
        ordinate (numpy.ndarray): The ordinate values.
        uncertainties (numpy.ndarray): Uncertainties on the ordinate.
        units (list): The units.

    """

    def __init__(self, abscissa, ordinate, uncertainties, units):
        """Construct a spectrum object.

        Note:
            Assumes JWST FITS file currently.

        Args:
            abscissa (numpy.ndarray): The abscissa values.
            ordinate (numpy.ndarray): The ordinate values.
            uncertainties (numpy.ndarray): Uncertainties on the ordinate.
            units_abscissae (str): Units of abscissa.
            units_ordinate (str): Units of ordinate.

        """
        self.abscissa = abscissa
        self.ordinate = ordinate
        self.uncertainties = uncertainties
        self.units = units

        # Always work as if ordinate is a cube
        if len(self.ordinate.shape) == 1:
            self.ordinate = np.reshape(self.ordinate, self.ordinate.shape + (1, 1))
            self.uncertainties = np.reshape(self.uncertainties, self.uncertainties.shape + (1, 1))
        self._units = units

    def convertunitsto(self, **keywords):
        """Convert units.

        Args:
            aunits (str): The new abscissa units.
            ounits (str): The new ordinate units.

        Returns:
            Nothing.
        """
        # currently hard coded
        if keywords.get('aunits'):
            #print(keywords.get('aunits'))
            self.abscissa = 1e4 / self.abscissa[::-1]
            self.ordinate = self.ordinate[::-1,::,::]

        #if keywords.get('ounits'):
           # print(keywords.get('ounits'))
