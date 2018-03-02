#!/usr/bin/env python
# observation.py

"""
observation.py: Holds and astronomical observation ...

This file is part of pypahdb - see the module docs for more
information.
"""

from __future__ import print_function

from astropy.io import ascii
from astropy.io import fits
from astropy import wcs
#from ipdb import set_trace as st
import numpy as np
from spectrum import spectrum


class observation(object):
    """Create an observation object for later analysis.

    Currently structured for two-column ASCII data.

    Attributes:
        abscissae (float, np.array): Independent variable (typically
            wavelength array).
        file_path (str): String of FITS file to load.
        fits_file: astropy.io.fits file (hdulist) object.
        header: astropy.io.fits header object.
        obs_type (str): Whether 'CUBE' or 'STARE' observation.
        ordinate (float, np.array): Dependent variable (typically flux
            density).
        telescope (str): 'JWST', 'Spitzer' or 'ISO'.
        uncertainties (float, np.array): Uncertainties on dependent
            variable.
        units_abscissa (str): Units of independent variable.
        units_ordinate (str): Units of dependent variable and
            uncertainties.

    """

    def __init__(self, file_path):
        """Instantiate an observation object.

        Note:
            Assumes ASCII data.

        Args:
            file_path (str): String of file to load.

        """
        self.file_path = file_path
        self.header = ""
        data = ascii.read(self.file_path)
        self.spectrum = spectrum(np.array(data['col1']), np.array(data['col2']), np.array(data['col3']), {'abscissa':{'str':'wavelength [um]'}, 'ordinate':{'str':'surface brightness [MJy/sr]'}})
