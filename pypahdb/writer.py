#!/usr/bin/env python
# writer.py

"""
writer.py: Writes decomposer results to file

This file is part of pypahdb - see the module docs for more
information.
"""

import time
import copy
from astropy.io import fits
from astropy import wcs
import numpy as np
import matplotlib.pyplot as plt
from decomposer import decomposer

#from ipdb import set_trace as st

class writer(object):
    """Creates a writer object.

    Writes PDF and FITS files.

    Attributes:

    """

    def __init__(self, result, header="", basename=""):
        """Instantiate a writer object.

        Args:
            result (pypahdb.decomposer): Decomposer object.

        Keywords:
            header (String, list): header
            basename (String): basename

        """

        # Think about output we want to show ...
        # What if not decomposer object ...
        # Make sure we're dealing with a 'decomposer' object
        if isinstance(result, decomposer):

            # deal with maps ... Add large/ionized fractions
            # save summary pdf
            plt.plot(result.spectrum.abscissa, result.spectrum.ordinate[:,0,0], color='blue')
            plt.plot(result.spectrum.abscissa, result.fit[:,0,0], color='red')
            plt.xlabel(result.spectrum.units['abscissa']['str'])
            plt.ylabel(result.spectrum.units['ordinate']['str'])
            plt.legend(['Observations', 'Fit'])
            plt.savefig(basename + '_summary.pdf')

            # save resuls to fits
            if isinstance(header, fits.header.Header):
                hdr = copy.deepcopy(header)
            else:
                hdr = fits.Header()

            # common cards
            hdr['DATE'] = time.strftime("%Y-%m-%dT%H:%m:%S")
            hdr['SOFTWARE'] = "pypahdb"
            hdr['SOFT_VER'] = "0.5.0.a1"
            hdr['COMMENT'] = "Visit https://www.github.com/pahdb/pypahdb/ for information on pypahdb"

            # need to deal with writting the breakdown spectra ...
            # write fit to fits-file
            h = copy.deepcopy(hdr)
            h['COMMENT'] = "This file contains a pypahdb fit"
            h['BUNIT'] = 'MJy/sr'
            h['CTYPE3'] = 'FREQ-TAB'
            h['CUNIT3'] = '1/cm'
            h['PS3_0'] = 'FREQ-TAB'
            h['PS3_1'] = 'FREQUENCY'
            if result.fit.shape[1] == 1 and result.fit.shape[2] == 1:
                h['FRAC_ION'] = result.ionized_fraction[0,0]
                h['FRAC_SIZ'] = result.large_fraction[0,0]
            hdu = fits.PrimaryHDU(result.fit, header=h)
            tbl = fits.BinTableHDU.from_columns([fits.Column(name=h['PS3_1'], format='E', array=result.spectrum.abscissa)])
            tbl.name = h['PS3_0']
            hdulist = fits.HDUList([hdu, tbl])
            hdulist.writeto(basename + '_fit.fits', overwrite=True)

            if result.fit.shape[1] != 1 or result.fit.shape[2] != 1:
                # write norm to fits-file
                h = copy.deepcopy(hdr)
                h['COMMENT'] = "This file contains the norm of a pahdb decomposition"
                hdu = fits.PrimaryHDU(result.norm, header=h)
                hdu.writeto(basename + '_norm.fits', overwrite=True)

                # write ionization fraction to fits-file
                h = copy.deepcopy(hdr)
                h['COMMENT'] = "This file contains the ionized fraction from a pahdb decomposition"
                hdu = fits.PrimaryHDU(result.ionized_fraction, header=h)
                hdu.writeto(basename + '_fi.fits', overwrite=True)

                # write large fraction to fits-file
                h = copy.deepcopy(hdr)
                h['COMMENT'] = "This file contains the large fraction from a pahdb decomposition"
                hdu = fits.PrimaryHDU(result.large_fraction, header=h)
                hdu.writeto(basename + '_fl.fits', overwrite=True)
