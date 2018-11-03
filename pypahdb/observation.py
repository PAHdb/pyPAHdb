#!/usr/bin/env python3
"""
observation.py

Holds and astronomical observation.

This file is part of pypahdb - see the module docs for more
information.
"""

import numpy as np

from astropy.io import ascii
from astropy.io import fits

from pypahdb.spectrum import Spectrum


class Observation(object):
    """Creates an Observation object.

    Currently reads ASCII data and Spitzer-IRS data cubes.

    Attributes:
        spectrum (spectrum): contains loaded spectrum
    """

    def __init__(self, file_path):
        """Instantiate an Observation object.

        Args:
            file_path (str): String of file to load.

        """
        self.file_path = file_path

        try:
            with fits.open(self.file_path) as hdu:
                hdu_keys = hdu[0].header.keys()

                # use the wcs definitions for coordinate three,
                # either via linear scale or lookup table
                if 'PS3_0' in hdu_keys and 'PS3_1' in hdu_keys:
                    self.header = hdu[0].header
                    # self.wcs = wcs.WCS(hdu[0].header, naxis=2)
                    h0 = self.header['PS3_0']
                    h1 = self.header['PS3_1']
                    abscissa_unit = hdu[h0].columns[h1].name + ' [' + \
                        hdu[h0].columns[h1].unit + ']'
                    ordinate_unit = self.header['BUNIT']

                    # Create spectrum object.
                    self.spectrum = \
                        Spectrum(hdu[h0].data[h1],
                                 hdu[0].data,
                                 np.zeros(hdu[0].data.shape),
                                 {'abscissa': {'str': abscissa_unit},
                                  'ordinate': {'str': ordinate_unit}})
                    return None
        except FileNotFoundError as e:
            raise(e)
        except OSError:
            # Because astropy.io.fits.open raises a generic OSError
            # when the file header is missing the END card (which
            # ASCII files do), we have to catch OSError here and pass
            # so that we can try and read it as ASCII.
            pass

        try:
            data = ascii.read(self.file_path)
            self.header = fits.header.Header()
            self.spectrum = \
                Spectrum(np.array(data[data.colnames[0]]),
                         np.array(data[data.colnames[1]]),
                         np.zeros(len(data[data.colnames[0]])),
                         {'abscissa': {'str': 'wavelength [micron]'},
                          'ordinate': {'str': 'surface brightness [MJy/sr]'}})
            return None
        except Exception as e:
            print(e)
            pass

        raise OSError(self.file_path + ": File-format not recognized")
