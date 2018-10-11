#!/usr/bin/env python
"""
mydecomposer.py

A subclass of Decomposer that extends functionality for writing files
to disk (as PDF or FITS).

From Decomposer:
Using a precomputed matrix of theoretically calculated
PAH emission spectra, an input spectrum is fitted and decomposed into
contributions from PAH subclasses using a nnls-approach.

This file is part of pypahdb - see the module docs for more
information.
"""

import copy
import decimal
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import time

from astropy.io import fits
from matplotlib.backends.backend_pdf import PdfPages
from pypahdb.decomposer import Decomposer


class Mydecomposer(Decomposer):

    def __init__(self, spectrum):
        self.result = Decomposer(spectrum)

    def write_to_disk(self, basename="output", header="",
                      save_pdf=True, save_fits=True):
        """Instantiate a writer object.

        Args:
            result (pypahdb.decomposer): Decomposer object.

        Keywords:
            header (String, list): header
            output_prefix (String): base prefix for saving to a file.

        """

        def _save_summary_pdf():
            """Save a PDF summary of the spectral fits/breakdowns."""

            def smart_round(value, style="0.1"):
                """Round a float correctly, returning a string."""
                tmp = decimal.Decimal(value).quantize(decimal.Decimal(style))
                return str(tmp)

            def _plot_pahdb_fit(i, j):
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
                fig = plt.figure(figsize=(8, 11))
                gs = gridspec.GridSpec(4, 1, height_ratios=[2, 1, 2, 2])
                gs.update(wspace=0.025, hspace=0.00)  # set the spacing between axes.
                ax0 = fig.add_subplot(gs[0])
                ax1 = fig.add_subplot(gs[1], sharex=ax0)
                ax2 = fig.add_subplot(gs[2], sharex=ax0)
                ax3 = fig.add_subplot(gs[3], sharex=ax0)

                # Common quantities for clarity.
                abscissa = self.result.spectrum.abscissa
                charge = self.result.charge

                # ax0 -- Best fit.
                data = self.result.spectrum.ordinate[:, i, j]
                model = self.result.fit[:, i, j]
                ax0.plot(abscissa, data, 'kx', ms=5, mew=0.5, label='input')
                ax0.plot(abscissa, model, label='fit', color='red')
                norm_val = self.result.norm[i][j]
                norm_str = smart_round(norm_val, style="0.1")
                norm_str = '$norm$=' + norm_str
                ax0.text(0.025, 0.9, norm_str, ha='left', va='center',
                         transform=ax0.transAxes)

                # ax1 -- Residuals.
                ax1.plot(abscissa, data - model, lw=1,
                         label='residual', color='black')
                ax1.axhline(y=0, color='0.5', ls='--', dashes=(12, 16),
                            zorder=-10, lw=0.5)

                # ax2 -- Size breakdown.
                ax2.plot(abscissa, model, color='red', lw=1.5)
                ax2.plot(abscissa, self.result.size['large'][:, i, j],
                         label='large', lw=1, color='purple')
                ax2.plot(abscissa, self.result.size['small'][:, i, j],
                         label='small', lw=1, color='crimson')
                size_frac = self.result.large_fraction[i][j]
                size_str = smart_round(size_frac, style="0.01")
                size_str = '$f_{large}$=' + size_str
                ax2.text(0.025, 0.9, size_str, ha='left', va='center',
                         transform=ax2.transAxes)

                # ax3 -- Charge breakdown.
                ax3.plot(abscissa, model, color='red', lw=1.5)
                ax3.plot(abscissa, charge['anion'][:, i, j],
                         label='anion', lw=1, color='orange')
                ax3.plot(abscissa, charge['neutral'][:, i, j],
                         label='neutral', lw=1, color='green')
                ax3.plot(abscissa, charge['cation'][:, i, j],
                         label='cation', lw=1, color='blue')
                ion_frac = self.result.ionized_fraction[i][j]
                ion_str = smart_round(ion_frac, "0.01")
                ion_str = '$f_{ionized}$=' + ion_str
                ax3.text(0.025, 0.9, ion_str, ha='left', va='center',
                         transform=ax3.transAxes)

                # Plot labels.
                ylabel = self.result.spectrum.units['ordinate']['str']
                fig.text(0.02, 0.5, ylabel, va='center', rotation='vertical')
                ax3.set_xlabel(self.result.spectrum.units['abscissa']['str'])

                # Set tick parameters and add legends to all axes.
                for ax in (ax0, ax1, ax2, ax3):
                    ax.tick_params(axis='both', which='both', direction='in',
                                   top=True, right=True)
                    ax.minorticks_on()
                    ax.legend(loc=0, frameon=False)

                return fig

            with PdfPages(self.basename + '_pypahdb.pdf') as pdf:
                d = pdf.infodict()
                d['Title'] = 'pyPAHdb Result Summary'
                d['Author'] = 'pyPAHdb'
                d['Subject'] = 'Summary of a pyPAHdb PAH database Decomposition'
                d['Keywords'] = 'pyPAHdb PAH database'
                for i in range(self.result.spectrum.ordinate.shape[1]):
                    for j in range(self.result.spectrum.ordinate.shape[2]):
                        fig = _plot_pahdb_fit(i, j)
                        pdf.savefig(fig)
                        plt.close(fig)
                        plt.gcf().clear()
            print('Saved: ', self.basename + '_pypahdb.pdf')

            return

        def _save_fits(hdr):
            """Save a FITS file of the spectral fits/breakdowns."""

            hdr['DATE'] = time.strftime("%Y-%m-%dT%H:%m:%S")
            hdr['SOFTWARE'] = "pypahdb"
            hdr['SOFT_VER'] = "0.5.0.a1"
            hdr['COMMENT'] = "This file contains the results from a pypahdb fit"
            hdr['COMMENT'] = "Visit https://github.com/pahdb/pypahdb/ " \
                "for more information on pypahdb"
            hdr['COMMENT'] = "The 1st plane contains the ionized fraction"
            hdr['COMMENT'] = "The 2nd plane contains the large fraction"
            hdr['COMMENT'] = "The 3rd plane contains the norm"

            # write results to fits-file
            hdu = fits.PrimaryHDU(np.stack((self.result.ionized_fraction,
                                            self.result.large_fraction,
                                            self.result.norm), axis=0), header=hdr)
            hdu.writeto(self.basename + '_pypahdb.fits', overwrite=True)
            print('Saved: ', self.basename + '_pypahdb.fits')

            return

        self.basename = basename
        self.header = header
        self.save_pdf = save_pdf
        self.save_fits = save_fits

        # What if not decomposer object ...
        # Make sure we're dealing with a 'decomposer' object
        if isinstance(self.result, Decomposer):
            if save_pdf:
                # save summary pdf
                _save_summary_pdf()

            if save_fits:
                # save resuls to fits
                if isinstance(header, fits.header.Header):
                    # should probably clean up the header
                    # i.e., extract certain keywords only
                    hdr = copy.deepcopy(header)
                else:
                    hdr = fits.Header()

                _save_fits(hdr)





