#!/usr/bin/env python3
"""
example.py

Example of using pypahdb to decompose an astronomical PAH spectrum.
"""

import pkg_resources

from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation


if __name__ == '__main__':

    # The sample data file.
    file_path = 'data/sample_data_NGC7023-NW-PAHs.txt'

    data_file = pkg_resources.resource_filename('pypahdb', file_path)

    # Load the file into an Observation object.
    obs = Observation(data_file)

    # Decompose the spectrum with pyPAHdb.
    pahdb_fit = Decomposer(obs.spectrum)

    # Save the fit to disk, both as a PDF and FITS file.
    pahdb_fit.save_pdf(filename='NGC7023_pypahdb.pdf')
    pahdb_fit.save_fits(filename='NGC7023_pypahdb.fits')
