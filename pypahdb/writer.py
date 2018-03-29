#!/usr/bin/env python
# writer.py

"""
writer.py: Writes decomposer results to file

This file is part of pypahdb - see the module docs for more
information.
"""

from __future__ import print_function

import copy
import decimal
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import time

from .decomposer import decomposer
from astropy.io import fits
from astropy import wcs
from ipdb import set_trace as st
from matplotlib.backends.backend_pdf import PdfPages


class writer(object):
    """Creates a writer object.

    Writes PDF and FITS files.

    Attributes:
        result (pypahdb.decomposer): Decomposer object.
        header (fits.header.Header): FITS header (normally).
        basename (str): Base string, used for saving files.

    """

    def __init__(self, result, header="", basename="", opdf=True, ofits=True):
        """Instantiate a writer object.

        Args:
            result (pypahdb.decomposer): Decomposer object.

        Keywords:
            header (String, list): header
            basename (String): basename

        """
        self.result = result
        self.header = header
        self.basename = basename
        self.opdf = opdf
        self.ofits = ofits

        # What if not decomposer object ...
        # Make sure we're dealing with a 'decomposer' object
        if isinstance(result, decomposer):
            if opdf:
                # save summary pdf
                self._save_summary_pdf()

            if ofits:
                # save resuls to fits
                if isinstance(header, fits.header.Header):
                    # should probably clean up the header, i.e., extract certain keywords only
                    hdr = copy.deepcopy(header)
                else:
                    hdr = fits.Header()

                self._save_fits(hdr)

    def _plot_pahdb_fit(self, i, j):
        """Plot a pyPAHdb fit and save to a PDF. 
        
        Note:
            Designed to accept (i,j) because it will be adjusted to make plots
            for spectral cubes (outputting a multipage PDF.)

        Args:
            i (int): Pixel coordiante (abscissa).
            j (int): Pixel coordinate (ordinate).

        Returns:
            True if successful.

        """

        # Create figure, shared axes.
        fig = plt.figure(figsize=(8,8))
        gs = gridspec.GridSpec(4, 1, height_ratios=[2,1,2,2])
        gs.update(wspace=0.025, hspace=0.00) # set the spacing between axes.
        ax0 = fig.add_subplot(gs[0])
        ax1 = fig.add_subplot(gs[1], sharex=ax0)
        ax2 = fig.add_subplot(gs[2], sharex=ax0)
        ax3 = fig.add_subplot(gs[3], sharex=ax0)

        # Common abscissa.
        wave = 1e4 / self.result.spectrum.abscissa
        
        # Best fit.
        data = self.result.spectrum.ordinate[:,i,j]
        model = self.result.fit[:,i,j]
        ax0.plot(wave, data, label='Observations')
        ax0.plot(wave, model, label='Model')
        norm_val = self.result.norm[0][0]
        norm_str = str(decimal.Decimal(norm_val).quantize(decimal.Decimal("0.1")))
        ax0.text(0.1, 0.9, 'Norm = ' + norm_str, ha='center', va='center',
                transform=ax0.transAxes)

        # Residuals.
        ax1.plot(wave, data - model, label='Residuals')
        ax1.axhline(y=0, color='k', ls=':', zorder=-10, lw=0.5)

        # Size breakdown.
        ax2.plot(wave, model, label='Model')
        ax2.plot(wave, self.result.size['large'][:,i,j], label='Large')
        ax2.plot(wave, self.result.size['small'][:,i,j], label='Small')
        
        # Charge breakdown.
        ax3.plot(wave, model, label='Model')
        ax3.plot(wave, self.result.charge['anion'][:,i,j], label='Anion')
        ax3.plot(wave, self.result.charge['neutral'][:,i,j], label='Neutral')
        ax3.plot(wave, self.result.charge['cation'][:,i,j], label='Cation')

        # Plot labels.
        ylabel = self.result.spectrum.units['ordinate']['str']
        fig.text(0.04, 0.5, ylabel, va='center', rotation='vertical')
        ax3.set_xlabel(self.result.spectrum.units['abscissa']['str'])

        # Plot legends and ticks.
        [ax.minorticks_on() for ax in (ax0,ax1,ax2,ax3)]
        ax0.legend(loc=0)
        ax1.legend(loc=0)
        ax2.legend(loc=0)
        ax3.legend(loc=0)

        

        ion_frac = self.result.ionized_fraction[0][0]
        ion_str = str(decimal.Decimal(ion_frac).quantize(decimal.Decimal("0.01")))

        size_frac = self.result.large_fraction[0][0]
        size_str = str(decimal.Decimal(size_frac).quantize(decimal.Decimal("0.01")))

        cat_str = 'Cation fraction: ' + ion_str
        size_str = 'Large fraction: ' + size_str

        ax0.set_title(cat_str + ', ' + size_str)


        # Save figure.
        savename = self.basename + 'pypahdb.pdf'
        fig.savefig(savename, format='pdf', bbox_inches='tight')
        print("Saved: ", savename)
        fig.clear()
        plt.close()

        return True

    def _save_summary_pdf(self):
        for i in range(self.result.spectrum.ordinate.shape[1]):
            for j in range(self.result.spectrum.ordinate.shape[2]):

                self._plot_pahdb_fit(i, j)
                # pdf.savefig()
                # plt.gcf().clear()

                # with PdfPages(self.basename + 'pypahdb.pdf') as pdf:
                #     d = pdf.infodict()
                #     d['Title'] = 'pyPAHdb Result Summary'
                #     d['Author'] = 'pyPAHdb'
                #     d['Subject'] = 'Summary of a pyPAHdb PAH database Decomposition'
                #     d['Keywords'] = 'pyPAHdb PAH database'

        return

    def _save_fits(self, hdr):

        hdr['DATE'] = time.strftime("%Y-%m-%dT%H:%m:%S")
        hdr['SOFTWARE'] = "pypahdb"
        hdr['SOFT_VER'] = "0.5.0.a1"
        hdr['COMMENT'] = "This file contains the results from a pypahdb fit"
        hdr['COMMENT'] = "Visit https://github.com/pahdb/pypahdb/ for more information on pypahdb"
        hdr['COMMENT'] = "The 1st plane contains the ionized fraction"
        hdr['COMMENT'] = "The 2nd plane contains the large fraction"
        hdr['COMMENT'] = "The 3rd plane contains the norm"

        # write results to fits-file
        hdu = fits.PrimaryHDU(np.stack((self.result.ionized_fraction,
                                        self.result.large_fraction,
                                        self.result.norm), axis=0), header=hdr)
        hdu.writeto(self.basename + 'pypahdb.fits', overwrite=True)
        
        return













