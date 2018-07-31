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
                # use the wcs definitions for coordinate three, either via linear scale or lookup table
                if 'PS3_0' in hdu[0].header.keys() and 'PS3_1' in hdu[0].header.keys():
                    self.header = hdu[0].header
                    #self.wcs = wcs.WCS(hdu[0].header, naxis=2)
                    self.spectrum = spectrum(hdu[self.header['PS3_0']].data[self.header['PS3_1']],
                                             hdu[0].data,
                                             np.zeros(hdu[0].data.shape),
                                             {'abscissa':{'str':hdu[self.header['PS3_0']].columns[self.header['PS3_1']].name +  ' [' + hdu[self.header['PS3_0']].columns[self.header['PS3_1']].unit + ']'},
                                              'ordinate':{'str':self.header['BUNIT']}})
                    return None
        except:
            pass

        try:
            data = ascii.read(self.file_path)
            self.header = fits.header.Header()
            self.spectrum = spectrum(np.array(data[data.colnames[0]]),
                                     np.array(data[data.colnames[1]]),
                                     np.zeros(len(data[data.colnames[0]])),
                                     {'abscissa':{'str':'wavelength [micron]'},
                                      'ordinate':{'str':'surface brightness [MJy/sr]'}})
            return None
        except:
            pass

        raise IOError(self.file_path + ": File-format not recognized")
