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
from matplotlib import cm, colormaps, colors
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import pypahdb
from pypahdb.decomposer_base import DecomposerBase, SMALL_SIZE, MEDIUM_SIZE


class Decomposer(DecomposerBase):
    """Extends DecomposerBase to write results to disk (PDF, FITS)."""

    def __init__(self, spectrum):
        """Initialize Decomposer object.

        Inherits from DecomposerBase defined in decomposer_base.py.

        Args:
            spectrum (specutils.Spectrum1D): The data to fit/decompose.
        """
        DecomposerBase.__init__(self, spectrum)
        self.large_fraction = self.size_fraction[0]
        self.medium_fraction = self.size_fraction[1]
        self.small_fraction = self.size_fraction[2]

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

        with PdfPages(filename) as pdf:
            d = pdf.infodict()
            d["Title"] = "pyPAHdb Results Summary"
            d["Author"] = (
                "Dr. C. Boersma, Dr. M.J. Shannon, and Dr. A. Maragkoudakis"
            )
            d["Producer"] = "NASA Ames Research Center"
            d["Creator"] = "pypahdb v{}(Python {}.{}.{})".format(
                pypahdb.__version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            )
            d["Subject"] = "Summary of pyPAHdb Decomposition"
            d["Keywords"] = "pyPAHdb, PAH, database, ERS, JWST"
            d["CreationDate"] = datetime.now(timezone.utc).strftime("D:%Y%m%d%H%M%S")
            d["Description"] = (
                "This file contains results from pyPAHdb. "
                "pyPAHdb was created as part of the JWST ERS "
                "Program titled 'Radiative Feedback from Massive Stars as "
                "Traced by Multiband Imaging and Spectroscopic Mosaics' (ID "
                "1288)). Visit https://github.com/pahdb/pypahdb/ for more"
                "information."
            )

            if domaps is True:
                if isinstance(header, fits.header.Header):
                    if "OBJECT" in header:
                        d["Title"] = d["Title"] + " - " + header["OBJECT"]

                    hdr = copy.deepcopy(header)
                    hdr["NAXIS"] = 2
                    cards = [
                        "NAXIS3",
                        "PC3_3",
                        "CRPIX3",
                        "CRVAL3",
                        "CTYPE3",
                        "CDELT3",
                        "CUNIT3",
                        "PS3_0",
                        "PS3_1",
                        "WCSAXES",
                    ]
                    for c in cards:
                        if c in hdr:
                            del hdr[c]

                    wcs = WCS(hdr)
                else:
                    wcs = None
                fig = self.plot_map(self.ionized_fraction, "n$_{{cation}}$/n$_{{neutral}}$", wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                fig = self.plot_map(self.large_fraction, f"large fraction (N$_{{C}}$ > {MEDIUM_SIZE})", wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                fig = self.plot_map(self.medium_fraction, f"medium fraction ({SMALL_SIZE} < N$_{{C}}$ ≤ {MEDIUM_SIZE})", wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                fig = self.plot_map(self.small_fraction, f"small fraction (N$_{{C}}$ ≤ {SMALL_SIZE})", wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)
                fig = self.plot_map(self.error, "error", wcs=wcs)
                pdf.savefig(fig)
                plt.close(fig)

            if doplots:
                ordinate = self.spectrum.flux.T
                for i in range(ordinate.shape[1]):
                    for j in range(ordinate.shape[2]):
                        fig = self.plot_fit(i, j)
                        pdf.savefig(fig)
                        plt.close(fig)

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

            hdr["DATE"] = (datetime.today().isoformat(), "When this file was generated")
            hdr["ORIGIN"] = (
                "NASA Ames Research Center",
                "Organization generating this file",
            )
            hdr["CREATOR"] = (
                "pypahdb v{} (Python {}.{}.{})".format(
                    pypahdb.__version__,
                    sys.version_info.major,
                    sys.version_info.minor,
                    sys.version_info.micro,
                ),
                "Software used to create this file",
            )
            hdr["AUTHOR"] = (
                "Dr. C. Boersma,  Dr. M.J. Shannon, and Dr. A. Maragkoudakis",
                "Authors of the software",
            )
            cards = [
                "PC3_3",
                "CRPIX3",
                "CRVAL3",
                "CTYPE3",
                "CDELT3",
                "CUNIT3",
                "PS3_0",
                "PS3_1",
                "WCSAXES",
            ]
            for c in cards:
                if c in hdr:
                    del hdr[c]
            comments = (
                "This file contains results from pypahdb.\n"
                "Pypahdb was created as part of the JWST ERS Program "
                "titled 'Radiative Feedback from Massive Stars as "
                "Traced by Multiband Imaging and Spectroscopic "
                "Mosaics' (ID 1288).\n"
                "Visit https://github.com/pahdb/pypahdb/ for more "
                "information on pypahdb."
            )
            for line in comments.split("\n"):
                for chunk in [line[i: i + 72] for i in range(0, len(line), 72)]:
                    hdr["COMMENT"] = chunk
            hdr["COMMENT"] = "1st data plane contains the PAH ionization fraction."
            hdr["COMMENT"] = "2nd data plane contains the PAH large fraction."
            hdr["COMMENT"] = "3rd data plane contains the PAH medium fraction."
            hdr["COMMENT"] = "4th data plane contains the PAH small fraction."
            hdr["COMMENT"] = "5th data plane contains the error."

            # Write results to FITS-file.
            hdu = fits.PrimaryHDU(
                np.stack(
                    (
                        self.ionized_fraction.value,
                        self.large_fraction.value,
                        self.medium_fraction.value,
                        self.small_fraction.value,
                        self.error.value,
                    ),
                    axis=0,
                ),
                header=hdr,
            )
            hdu.writeto(filename, overwrite=True, output_verify="fix")

            return

        # Save results to FITS-file
        if isinstance(header, fits.header.Header):
            # TODO: Clean up header.
            hdr = copy.deepcopy(header)
        else:
            hdr = fits.Header()

        _fits_to_disk(hdr, filename)

        return

    @staticmethod
    def plot_map(data, title, wcs=None):
        """Plots a map.

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
        m = np.nanmax(data)

        im = data / m

        cmap = colormaps["rainbow"]

        x, y = np.meshgrid(np.arange(0, im.shape[1] + 1), np.arange(0, im.shape[0] + 1))
        x = x.astype("float") - 0.5
        y = y.astype("float") - 0.5

        if wcs:
            a, d = wcs.pixel_to_world_values(x, y)
            wcs_proj = wcs.deepcopy()
            wcs_proj.wcs.pc = [[-1, 0], [0, 1]]
            x, y = wcs_proj.world_to_pixel_values(a, d)
            ax = plt.subplot(projection=wcs_proj)
        else:
            ax = plt.subplot()

        ax.set_aspect("equal", adjustable="box", anchor="SW")
        ax.set_facecolor("#000000")

        ax.set_xlim(x.min() - 1, x.max() + 1)
        ax.set_ylim(y.min() - 1, y.max() + 1)

        args = list()
        for i in range(im.shape[0]):
            ii = [i, i + 1, i + 1, i, i]
            for j in range(im.shape[1]):
                if np.isfinite(im[i, j]):
                    jj = [j, j, j + 1, j + 1, j]
                    args += [x[ii, jj], y[ii, jj], colors.to_hex(cmap(im[i, j]))]
        plt.fill(*tuple(args))

        if wcs:
            reverse = x[0, 0] < x[-1, 0]
            if reverse:
                ax.invert_xaxis()
            plt.arrow(
                0.98,
                0.02,
                0.0,
                0.1,
                transform=ax.transAxes,
                width=0.005,
                color="white",
            )
            plt.text(
                0.84,
                0.02,
                "E",
                transform=ax.transAxes,
                color="white",
                horizontalalignment="center",
                verticalalignment="center",
            )
            plt.arrow(
                0.98,
                0.02,
                -0.1,
                0.0,
                transform=ax.transAxes,
                width=0.005,
                color="white",
            )
            plt.text(
                0.98,
                0.16,
                "N",
                transform=ax.transAxes,
                color="white",
                horizontalalignment="center",
                verticalalignment="center",
            )
            x0, y0 = ax.transLimits.inverted().transform((0.075, 0.1))
            if reverse:
                x1 = x0 - 1
            else:
                x1 = x0 + 1
            y1 = y0 + 1
            x = [x0, x1, x1, x0, x0]
            y = [y0, y0, y1, y1, y0]
            plt.fill(
                x,
                y,
                hatch=r"\\\\\\\\\/////////",
                edgecolor="white",
                facecolor=(1, 1, 1, 0.0),
            )
            plt.text(
                x0 + (x1 - x0) / 2.0,
                y0 - 0.5,
                "pixel",
                color="white",
                horizontalalignment="center",
                verticalalignment="top",
            )
            x0, y0 = ax.transLimits.inverted().transform((0.25, 0.1))
            if reverse:
                x1 = x0 - 1.0 / (3600 * wcs.wcs.cdelt[0])
            else:
                x1 = x0 + 1.0 / (3600 * wcs.wcs.cdelt[0])
            plt.plot([x0, x1], [y0, y0], color="white", linewidth=1.5)
            plt.text(
                x0 + (x1 - x0) / 2.0,
                y0 - 0.5,
                '1"',
                color="white",
                horizontalalignment="center",
                verticalalignment="top",
            )

            plt.xlabel("right ascension")
            plt.ylabel("declination")
        else:
            plt.xlabel("pixel [#]")
            plt.ylabel("pixel [#]")

        fig = plt.gcf()
        fig.set_layout_engine("constrained")

        colorbar = cm.ScalarMappable(cmap=cmap)
        colorbar.set_clim(0.0, m)
        cax = inset_axes(
            ax, width="2%", height="100%", loc="center right", borderpad=-1
        )
        plt.colorbar(colorbar, cax=cax)
        cax.set_ylabel(title)

        return fig

    def plot_fit(self, i=0, j=0):
        """Plots a fit and saves it to a PDF.

        Notes:
            None.

        Args:
            i (int): Pixel coordinate (abscissa).
            j (int): Pixel coordinate (ordinate).

        Returns:
            fig (matplotlib.figure.Figure): Instance of figure.

        """

        # Create figure on shared axes.
        fig = plt.figure()
        gs = gridspec.GridSpec(4, 1, height_ratios=[2, 1, 2, 2], figure=fig)

        # Add some spacing between axes.
        gs.update(wspace=0.025, hspace=0.00)
        ax0 = fig.add_subplot(gs[0])
        ax1 = fig.add_subplot(gs[1], sharex=ax0)
        ax2 = fig.add_subplot(gs[2], sharex=ax0)
        ax3 = fig.add_subplot(gs[3], sharex=ax0)
        for ax in [ax0, ax2, ax3]:
            fmt = ax.yaxis.get_major_formatter()
            fmt.set_scientific(True)
            fmt.set_powerlimits((-3, 1))
        for ax in [ax0, ax1, ax2]:
            plt.setp(ax.get_xticklabels(), visible=False)

        # Convenience definitions.
        abscissa = self.spectrum.spectral_axis
        charge = self.charge
        # Check if size of datapoints are too large and change marker size.
        ms = 5 if len(abscissa) < 1000 else 2

        # ax0: Best fit.
        data = self.spectrum.flux.T[:, i, j]
        unc = None
        if self.spectrum.uncertainty:
            unc = self.spectrum.uncertainty.quantity.T[:, i, j]
        model = self.fit[:, i, j]
        ax0.errorbar(
            abscissa,
            data,
            yerr=unc,
            marker=".",
            ms=ms,
            mew=0.5,
            lw=0,
            color="black",
            ecolor="grey",
            capsize=2,
            label="input",
            zorder=0,
        )
        ax0.plot(abscissa, model, label="fit", color="tab:red", lw=1.5)
        error_str = "$error$=%-4.2f" % (self.error[i][j])
        ax0.text(0.025, 0.88, error_str, ha="left", va="center", transform=ax0.transAxes)
        ax0.set_ylabel(f'{self.spectrum.meta["colnames"][1]} [{self.spectrum.flux.unit}]')

        # ax1: Residual.
        ax1.plot(abscissa, data - model, lw=1, label="residual", color="gray")
        ax1.axhline(y=0, color="0.5", ls="--", dashes=(12, 16), zorder=-10, lw=0.5)

        # ax2: Size breakdown.
        ax2.errorbar(
            abscissa,
            data,
            yerr=unc,
            marker=".",
            ms=ms,
            mew=0.5,
            lw=0,
            color="black",
            ecolor="grey",
            capsize=2,
            zorder=0,
        )
        ax2.plot(abscissa, model, color="tab:red", lw=1.5)
        ax2.plot(
            abscissa, self.size["large"][:, i, j], label="large", lw=1, color="tab:orange"
        )
        ax2.plot(
            abscissa, self.size["medium"][:, i, j], label="medium", lw=1, color="tab:green"
        )
        ax2.plot(
            abscissa, self.size["small"][:, i, j], label="small", lw=1, color="tab:blue"
        )
        size_str = "$f_{large}$=%3.1f" % (self.large_fraction[i][j])
        ax2.text(0.025, 0.88, size_str, ha="left", va="center", transform=ax2.transAxes)
        ax2.set_ylabel(f'{self.spectrum.meta["colnames"][1]} [{self.spectrum.flux.unit}]')

        # ax3: Charge breakdown.
        ax3.errorbar(
            abscissa,
            data,
            yerr=unc,
            marker=".",
            ms=ms,
            mew=0.5,
            lw=0,
            color="black",
            ecolor="grey",
            capsize=2,
            zorder=0,
        )
        ax3.plot(abscissa, model, color="red", lw=1.5)
        ax3.plot(
            abscissa, charge["anion"][:, i, j], label="anion", lw=1, color="tab:orange"
        )
        ax3.plot(
            abscissa, charge["neutral"][:, i, j], label="neutral", lw=1, color="tab:cyan"
        )
        ax3.plot(
            abscissa, charge["cation"][:, i, j], label="cation", lw=1, color="tab:purple"
        )
        ion_str = "$n_{cation}/n_{neutral}$=%3.1f" % (self.ionized_fraction[i][j])
        ax3.text(0.025, 0.88, ion_str, ha="left", va="center", transform=ax3.transAxes)
        ax3.set_xlabel(f'{self.spectrum.meta["colnames"][0]} [{self.spectrum.spectral_axis.unit}]')
        ax3.set_ylabel(f'{self.spectrum.meta["colnames"][1]} [{self.spectrum.flux.unit}]')

        # Set tick parameters and add legends to axes.
        for ax in (ax0, ax1, ax2, ax3):
            ax.tick_params(
                axis="both", which="both", direction="in", top=True, right=True
            )
            ax.minorticks_on()
            ax.legend(loc=0, frameon=False)

        fig.set_layout_engine("constrained")

        return fig
