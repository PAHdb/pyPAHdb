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

from astropy import units as u
from specutils import Spectrum1D


class Observation(object):
    """Creates an Observation object.

    Currently reads IPAC tables and Spitzer-IRS data cubes.

    Attributes:
        spectrum (specutils.Spectrum1D): contains loaded spectrum
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

                    # Create Spectrum1D object.
                    flux = hdu[0].data.T * u.Unit(self.header['BUNIT'])
                    wave = hdu[h0].data[h1] * u.Unit(hdu[h0].columns[h1].unit)
                    self.spectrum = Spectrum1D(flux, spectral_axis=wave)

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
            # Always work as if spectrum is a cube
            flux = np.reshape(data['FLUX'].quantity,
                              (1, 1, )+data['FLUX'].quantity.shape)
            # Create Spectrum1D object.
            wave = data['WAVELENGTH'].quantity
            self.spectrum = Spectrum1D(flux, spectral_axis=wave)
            str = ''
            for card in data.meta['keywords'].keys():
                value = data.meta['keywords'][card]['value']
                str += "%-8s=%71s" % (card, value)
            self.header = fits.header.Header.fromstring(str)
            return None
        except Exception as e:
            print(e)
            pass

        raise OSError(self.file_path + ": Format not recognized")
