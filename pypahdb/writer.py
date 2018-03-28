#!/usr/bin/env python
# writer.py

"""
writer.py: Writes decomposer results to file

This file is part of pypahdb - see the module docs for more
information.
"""

import copy
import matplotlib.pyplot as plt
import numpy as np
import time

from matplotlib.backends.backend_pdf import PdfPages

from astropy.io import fits
from astropy import wcs

from .decomposer import decomposer


class writer(object):
    """Creates a writer object.

    Writes PDF and FITS files.

    Attributes:

    """

    def __init__(self, result, header="", basename="", opdf=True, ofits=True):
        """Instantiate a writer object.

        Args:
            result (pypahdb.decomposer): Decomposer object.

        Keywords:
            header (String, list): header
            basename (String): basename

        """
        # What if not decomposer object ...
        # Make sure we're dealing with a 'decomposer' object
        if isinstance(result, decomposer):
            if opdf:
                # save summary pdf
                with PdfPages(basename + 'pypahdb.pdf') as pdf:
                    d = pdf.infodict()
                    d['Title'] = 'pyPAHdb Result Summary'
                    d['Author'] = 'pyPAHdb'
                    d['Subject'] = 'Summary of a pyPAHdb PAH database Decomposition'
                    d['Keywords'] = 'pyPAHdb PAH database'
                    for i in range(result.spectrum.ordinate.shape[1]):
                        for j in range(result.spectrum.ordinate.shape[2]):
                            plt.plot(1e4 / result.spectrum.abscissa, result.spectrum.ordinate[:,i,j], color='blue')
                            plt.plot(1e4 / result.spectrum.abscissa, result.fit[:,i,j], color='red')
                            plt.plot(1e4 / result.spectrum.abscissa, result.size['large'][:,i,j], color='green')
                            plt.plot(1e4 / result.spectrum.abscissa, result.size['small'][:,i,j], color='orange')
                            plt.plot(1e4 / result.spectrum.abscissa, result.charge['anion'][:,i,j], color='magenta')
                            plt.plot(1e4 / result.spectrum.abscissa, result.charge['neutral'][:,i,j], color='cyan')
                            plt.plot(1e4 / result.spectrum.abscissa, result.charge['cation'][:,i,j], color='violet')
                            plt.xlabel(result.spectrum.units['abscissa']['str'])
                            plt.ylabel(result.spectrum.units['ordinate']['str'])
                            plt.legend(['Observations', 'Fit', 'Large', 'Small', 'Anion', 'Neutral', 'Cation'])
                            pdf.savefig()
                            plt.gcf().clear()

            if ofits:
                # save resuls to fits
                if isinstance(header, fits.header.Header):
                    # should probably clean up the header, i.e., extract certain keywords only
                    hdr = copy.deepcopy(header)
                else:
                    hdr = fits.Header()

                hdr['DATE'] = time.strftime("%Y-%m-%dT%H:%m:%S")
                hdr['SOFTWARE'] = "pypahdb"
                hdr['SOFT_VER'] = "0.5.0.a1"
                hdr['COMMENT'] = "This file contains the results from a pypahdb fit"
                hdr['COMMENT'] = "Visit https://github.com/pahdb/pypahdb/ for more information on pypahdb"
                hdr['COMMENT'] = "The 1st plane contains the ionized fraction"
                hdr['COMMENT'] = "The 2nd plane contains the large fraction"
                hdr['COMMENT'] = "The 3rd plane contains the norm"

                # write results to fits-file
                hdu = fits.PrimaryHDU(np.stack((result.ionized_fraction,
                                                result.large_fraction,
                                                result.norm), axis=0), header=hdr)
                hdu.writeto(basename + 'pypahdb.fits', overwrite=True)
