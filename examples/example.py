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

    # Write the output to disk, as both PDF and FITS (by default).
    pahdb_fit.write_to_disk(basename='example_output')
