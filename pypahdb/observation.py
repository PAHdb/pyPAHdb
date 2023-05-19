#!/usr/bin/env python3
"""
observation.py

Manages reading an astronomical observation from file.

This file is part of pypahdb - see the module docs for more
information.
"""

import warnings

import numpy as np
from astropy import units as u
from astropy.io import ascii, fits
from astropy.io.fits.verify import VerifyWarning
from astropy.io.registry import IORegistryError
from astropy.nddata import StdDevUncertainty
from specutils import Spectrum1D


class Observation(object):
    """Creates an Observation object.

    Reads IPAC tables, Spitzer-IRS data cubes, and JWST spectra.

    Attributes:
        spectrum (specutils.Spectrum1D): contains loaded spectrum.
    """

    def __init__(self, file_path):
        """Instantiate an Observation object.

        Args:
            file_path (str): String of file to load.
        """
        self.file_path = file_path

        # TODO: implement try-except block for reading in pyPAHFit results

        try:
            # Suppress warning when Spectrum1D cannot load the file.
            warnings.simplefilter("ignore", category=VerifyWarning)

            self.spectrum = Spectrum1D.read(self.file_path)

            # Always work as if spectrum is a cube.
            if len(self.spectrum.flux.shape) == 1:
                self.spectrum = Spectrum1D(
                    flux=np.reshape(
                        self.spectrum.flux,
                        (
                            1,
                            1,
                        )
                        + self.spectrum.flux.shape,
                    ),
                    spectral_axis=self.spectrum.spectral_axis,
                )

            if "header" in self.spectrum.meta:
                self.header = self.spectrum.meta["header"]
            else:
                self.header = fits.header.Header()

            return None
        except FileNotFoundError as e:
            raise (e)
        except (OSError, IORegistryError):
            # Because Spectrum1D raises a generic OSError when the
            # file cannot be read, we have to catch OSError here and pass
            # so that we can try and read it directly as FITS or ASCII.
            pass

        try:
            with fits.open(self.file_path) as hdu:
                for h in hdu:
                    hdu_keys = list(h.header.keys())

                    # Use the WCS definitions for coordinate three
                    # lookup table.
                    if "PS3_0" in hdu_keys and "PS3_1" in hdu_keys:
                        self.header = h.header

                        # Create WCS object.
                        # self.wcs = wcs.WCS(hdu[0].header, naxis=2)

                        h0 = self.header["PS3_0"]
                        h1 = self.header["PS3_1"]

                        # Create Spectrum1D object.
                        flux = h.data.T * u.Unit(h.header["BUNIT"])
                        wave = hdu[h0].data[h1] * u.Unit(hdu[h0].columns[h1].unit)
                        self.spectrum = Spectrum1D(flux, spectral_axis=wave)

                        return None

                    # Use the WCS definitions for coordinate three
                    # linear.
                    if "CDELT3" in hdu_keys:
                        self.header = h.header

                        # Create WCS object
                        # self.wcs = wcs.WCS(hdu[0].header, naxis=2)

                        # Create Spectrum1D object
                        # u.Unit(self.header['BUNIT'])
                        flux = h.data.T * u.Unit("Jy")
                        wave = (
                            h.header["CRVAL3"]
                            + h.header["CDELT3"] * np.arange(0, h.header["NAXIS3"])
                        ) * u.Unit(h.header["CUNIT3"])
                        self.spectrum = Spectrum1D(flux, spectral_axis=wave)

                        return None

        except OSError:
            # Because astropy.io.fits.open raises a generic OSError
            # when the file header is missing the END card (which
            # ASCII files do), we have to catch OSError here and pass
            # so that we can try and read it as ASCII.
            pass

        try:
            data = ascii.read(self.file_path)
            # Always work as if spectrum is a cube.
            flux = np.reshape(
                data["FLUX"].quantity,
                (
                    1,
                    1,
                )
                + data["FLUX"].quantity.shape,
            )
            # Create Spectrum1D object.
            for name in data.colnames:
                data.rename_column(name, name.upper())
            wave = data["WAVELENGTH"].quantity
            unc = None
            if "FLUX_UNCERTAINTY" in data.colnames:
                unc = StdDevUncertainty(
                    np.reshape(
                        data["FLUX_UNCERTAINTY"].quantity,
                        (
                            1,
                            1,
                        )
                        + (data["FLUX_UNCERTAINTY"].quantity.shape),
                    )
                )
            self.spectrum = Spectrum1D(flux, spectral_axis=wave, uncertainty=unc)
            str = ""
            for card in data.meta["keywords"].keys():
                value = data.meta["keywords"][card]["value"]
                str += "%-8s=%71s" % (card, value)
            self.header = fits.header.Header.fromstring(str)
            return None
        except Exception:
            pass

        # Like astropy.io we, simply raise a generic OSError when
        # we fail to read the file.
        raise OSError(self.file_path + ": Format not recognized")
