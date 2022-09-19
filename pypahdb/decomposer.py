#!/usr/bin/env python3
"""decomposer.py

Subclass of DecomposerBase for writting results to disk.

This file is part of pypahdb - see the module docs for more
information.

"""
import copy
import sys
from datetime import datetime, timezone

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from matplotlib.backends.backend_pdf import PdfPages

import pypahdb
from pypahdb.decomposer_base import DecomposerBase


class Decomposer(DecomposerBase):
    """Extends DecomposerBase to write results to disk (PDF, FITS)."""

    def __init__(self, spectrum):
        """Initialize Decomposer object.

        Inherits from DecomposerBase defined in decomposer_base.py.

        Args:
            spectrum (specutils.Spectrum1D): The data to fit/decompose.
        """
        DecomposerBase.__init__(self, spectrum)

    def save_pdf(self, filename, header="", domaps=True, doplots=True):
        """Save a PDF summary of the fit results.

            Notes:
                None.

            Args:
                filename (str): Path to save to.
                header (str): Optional, header data.

            Keywords:
                domaps (bool): Save maps to PDF (defaults to True).
                doplots (bool): Save plots to PDF (defaults to True).

            Returns:
                None.

        """

        def _plot_map(im, title, wcs=None):
            """Plots an image and saves it to a PDF.

            Notes:
                None.

            Args:
                im (numpy): Image.
                title (string): Image title.

            Keywords:
                wcs (wcs.wcs): WCS (defaults to None).

            Returns:
                fig (matplotlib.figure.Figure): Instance of figure.

            """
            fig = plt.figure(figsize=(8, 11))
            if isinstance(wcs, WCS):
                ax = fig.add_subplot(111, projection=wcs)
            else:
                ax = fig.add_subplot(111)
            ax.grid('on', color='black')
            ax.minorticks_on()
            ax.xaxis.set_tick_params(direction='in',
                                     which='both',
                                     bottom=True,
                                     top=True,
                                     left=True,
                                     right=True)
            ax.yaxis.set_tick_params(direction='in',
                                     which='both',
                                     bottom=True,
                                     top=True,
                                     left=True,
                                     right=True)
            fig.subplots_adjust(left=0.2)
            plt.imshow(im, origin='lower', cmap='viridis',
                       interpolation='nearest')
            ax.set_xlabel(r"Ra [$^{\circ}$ ' '']")
            ax.set_ylabel(r"Dec [$^{\circ}$ ' '']")
            cbar = plt.colorbar(shrink=0.4)
            cbar.set_label(title)
            return fig

        def _plot_fit(i, j):
            """Plots a fit and saves it to a PDF.

            Notes:
                None.

            Args:
                i (int): Pixel coordinate (abscissa).
                j (int): Pixel coordinate (ordinate).

            Returns:
                fig (matplotlib.figure.Figure): Instance of figure.

            """

            # Enable quantity_support.
            from astropy.visualization import quantity_support
            quantity_support()

            # Create figure on shared axes.
            fig = plt.figure(figsize=(8, 11))
            gs = gridspec.GridSpec(4, 1, height_ratios=[2, 1, 2, 2])

            # Add some spacing between axes.
            gs.update(wspace=0.025, hspace=0.00)
            ax0 = fig.add_subplot(gs[0])
            ax1 = fig.add_subplot(gs[1], sharex=ax0)
            ax2 = fig.add_subplot(gs[2], sharex=ax0)
            ax3 = fig.add_subplot(gs[3], sharex=ax0)

            # Convenience defintions.
            abscissa = self.spectrum.spectral_axis
            charge = self.charge

            # ax0: Best fit.
            data = self.spectrum.flux.T[:, i, j]
            unc = None
            if self.spectrum.uncertainty:
                unc = self.spectrum.uncertainty.quantity.T[:, i, j]
            model = self.fit[:, i, j]
            ax0.errorbar(abscissa, data, yerr=unc, marker='x', ms=5, mew=0.5,
                         lw=0, color='black', ecolor='grey', capsize=2, label='input')
            ax0.plot(abscissa, model, label='fit', color='red', lw=1.5)
            error_str = "$error$=%-4.2f" % (self.error[i][j])
            ax0.text(0.025, 0.9, error_str, ha='left', va='center',
                     transform=ax0.transAxes)

            # ax1: Residual.
            ax1.plot(abscissa, data - model, lw=1,
                     label='residual', color='black')
            ax1.axhline(y=0, color='0.5', ls='--', dashes=(12, 16),
                        zorder=-10, lw=0.5)

            # ax2: Size breakdown.
            ax2.errorbar(abscissa, data, yerr=unc, marker='x', ms=5,
                         mew=0.5, lw=0, color='black', ecolor='grey', capsize=2, label='input')
            ax2.plot(abscissa, model, color='red', lw=1.5)
            ax2.plot(abscissa, self.size['large'][:, i, j],
                     label='large', lw=1, color='purple')
            ax2.plot(abscissa, self.size['small'][:, i, j],
                     label='small', lw=1, color='crimson')
            size_str = "$f_{large}$=%3.1f" % (self.large_fraction[i][j])
            ax2.text(0.025, 0.9, size_str, ha='left', va='center',
                     transform=ax2.transAxes)

            # ax3: Charge breakdown.
            ax3.errorbar(abscissa, data, yerr=unc, marker='x', ms=5,
                         mew=0.5, lw=0, color='black', ecolor='grey', capsize=2, label='input')
            ax3.plot(abscissa, model, color='red', lw=1.5)
            ax3.plot(abscissa, charge['anion'][:, i, j],
                     label='anion', lw=1, color='orange')
            ax3.plot(abscissa, charge['neutral'][:, i, j],
                     label='neutral', lw=1, color='green')
            ax3.plot(abscissa, charge['cation'][:, i, j],
                     label='cation', lw=1, color='blue')
            ion_str = "$f_{ionized}$=%3.1f" % (self.ionized_fraction[i][j])
            ax3.text(0.025, 0.9, ion_str, ha='left', va='center',
                     transform=ax3.transAxes)

            # Set tick parameters and add legends to axes.
            for ax in (ax0, ax1, ax2, ax3):
                ax.tick_params(axis='both', which='both', direction='in',
                               top=True, right=True)
                ax.minorticks_on()
                ax.legend(loc=0, frameon=False)

            return fig

        with PdfPages(filename) as pdf:
            d = pdf.infodict()
            d['Title'] = 'Pypahdb Result Summary'
            d['Author'] = 'Dr. C. Boersma, Dr. M.J. Shannon, and Dr. A. ' \
                'Maragkoudakis'
            d['Producer'] = 'NASA Ames Research Center'
            d['Creator'] = "pypahdb v{}(Python {}.{}.{})".format(
                pypahdb.__version__, sys.version_info.major,
                sys.version_info.minor, sys.version_info.micro)
            d['Subject'] = 'Summary of Pypahdb Decomposition'
            d['Keywords'] = 'pypahdb, PAH, database, ERS, JWST'
            d['CreationDate'] = datetime.now(
                timezone.utc).strftime("D:%Y%m%d%H%M%S")
            d['Description'] = "This file contains results from pypahdb.\n" \
                "pypahdb was created as part of the JWST ERS " \
                "Program titled 'Radiative Feedback from Massive Stars as " \
                "Traced by Multiband Imaging and Spectroscopic Mosaics' (ID " \
                "1288)).\n Visit https://github.com/pahdb/pypahdb/ for more" \
                "information on pypahdb."

            if (domaps is True):
                if isinstance(header, fits.header.Header):
                    if 'OBJECT' in header:
                        d['Title'] = d['Title'] + ' - ' + header['OBJECT']

                    hdr = copy.deepcopy(header)
                    hdr['NAXIS'] = 2
                    cards = ['NAXIS3', 'PC3_3', 'CRPIX3',
                             'CRVAL3', 'CTYPE3', 'CDELT3',
                             'CUNIT3', 'PS3_0', 'PS3_1',
                             'WCSAXES']
                    for c in cards:
                        if c in hdr:
                            del hdr[c]

                    wcs = WCS(hdr)
                else:
                    wcs = None
                fig = _plot_map(self.ionized_fraction,
                                'ionization fraction', wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                plt.gcf().clear()
                fig = _plot_map(self.large_fraction,
                                'large fraction', wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                plt.gcf().clear()
                fig = _plot_map(self.error, 'error', wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                plt.gcf().clear()

            if (doplots):
                ordinate = self.spectrum.flux.T
                for i in range(ordinate.shape[1]):
                    for j in range(ordinate.shape[2]):
                        fig = _plot_fit(i, j)
                        pdf.savefig(fig)
                        plt.close(fig)
                        plt.gcf().clear()

        return

    def save_fits(self, filename, header=""):
        """Save FITS file summary of the fit results.

        Args:
            filename (str): Path to save to.
            header (str): Optional, header for the FITS file.
        """

        def _fits_to_disk(hdr, filename):
            """Writes the FITS file to disk, with header.

            Args:
                hdr (fits.header.Header): FITS header.
                filename (str): Path of FITS file to be saved.
            """

            hdr['DATE'] = (datetime.today(
            ).isoformat(), "When this file was generated")
            hdr['ORIGIN'] = ("NASA Ames Research Center",
                             "Organization generating this file")
            hdr['CREATOR'] = ("pypahdb v{} (Python {}.{}.{})".format(
                pypahdb.__version__, sys.version_info.major,
                sys.version_info.minor, sys.version_info.micro),
                "Software used to create this file")
            hdr['AUTHOR'] = ("Dr. C. Boersma,  Dr. M.J. Shannon, and Dr. A. "
                             "Maragkoudakis", "Authors of the software")
            comments = "This file contains results from pypahdb.\n" \
                       "Pypahdb was created as part of the JWST ERS Program " \
                       "titled 'Radiative Feedback from Massive Stars as " \
                       "Traced by Multiband Imaging and Spectroscopic " \
                       "Mosaics' (ID 1288).\n" \
                       "Visit https://github.com/pahdb/pypahdb/ for more " \
                       "information on pypahdb."
            for line in comments.split('\n'):
                for chunk in [line[i:i+72] for i in range(0, len(line), 72)]:
                    hdr['COMMENT'] = chunk
            hdr['COMMENT'] = "1st data plane contains the PAH ionization " \
                "fraction."
            hdr['COMMENT'] = "2nd data plane contains the PAH large fraction."
            hdr['COMMENT'] = "3rd data plane contains the error"

            # Write results to FITS-file.
            hdu = fits.PrimaryHDU(np.stack((self.ionized_fraction.value,
                                            self.large_fraction.value,
                                            self.error.value), axis=0),
                                  header=hdr)
            hdu.writeto(filename, overwrite=True, output_verify='fix')

            return

        # Save results to FITS-file
        if isinstance(header, fits.header.Header):
            # TODO: Clean up header.
            hdr = copy.deepcopy(header)
        else:
            hdr = fits.Header()

        _fits_to_disk(hdr, filename)

        return
