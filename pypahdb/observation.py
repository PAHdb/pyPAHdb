#!/usr/bin/env python
# observation.py

"""
observation.py: Holds and astronomical observation

This file is part of pypahdb - see the module docs for more
information.
"""

import numpy as np

from astropy.io import ascii
from astropy.io import fits
from astropy import wcs

from .spectrum import spectrum


class observation(object):
    """Creates an observation object.

    Currently reads ASCII data and Spitzer-IRS data cubes.

    Attributes:
        spectrum (spectrum): contains loaded spectrum
    """

    def __init__(self, file_path):
        """Instantiate an observation object.

        Args:
            file_path (str): String of file to load.

        """
        self.file_path = file_path

        try:
            with fits.open(self.file_path) as hdu:
                # what if we're loading a table?
                # use the wcs definitions for coordinate three, either via linear scale or lookup table
                if ('TELESCOP' in hdu[0].header.keys() and hdu[0].header['TELESCOP'] == 'Spitzer' and
                   'INSTRUME' in hdu[0].header.keys() and hdu[0].header['INSTRUME'] == 'IRSX'):
                    self.header = hdu[0].header
                    #self.wcs = wcs.WCS(hdu[0].header, naxis=2)
                    self.spectrum = spectrum(hdu[1].data['wavelength'], hdu[0].data, np.zeros(hdu[0].data.shape), {'abscissa':{'str':'wavelength [um]'}, 'ordinate':{'str':'surface brightness [MJy/sr]'}})
                    return None
        except IOError:
            pass

        try:
            data = ascii.read(self.file_path)
            self.header = fits.header.Header()
            self.spectrum = spectrum(np.array(data['col1']), np.array(data['col2']), np.zeros(len(data['col1'])), {'abscissa':{'str':'wavelength [um]'}, 'ordinate':{'str':'surface brightness [MJy/sr]'}})
            return None
        except UnicodeDecodeError:
            pass
