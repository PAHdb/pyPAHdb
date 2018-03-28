#!/usr/bin/env python
# example.py

"""example.py: Example of using pypahdb to decompose an astronomical PAH spectrum"""

__author__ = "Christiaan Boersma"
__copyright__ = "Copyright 2018, The NASA Ames PAH IR Spectroscopic Database"
__credits__ = ["Matthew J. Shannon"]
__license__ = "BSD 3-Clause"
__version__ = "0.0.1"
__maintainer__ = "Christiaan Boersma"
__email__ = "Christiaan.Boersma@nasa.gov"
__status__ = "Prototype"

import pypahdb
from astropy.io import fits
from os.path import splitext, basename

if __name__ == "__main__":

    # load an observation from file
    observation = pypahdb.observation('NGC7023.fits')

    # decompose the spectrum with PAHdb
    result = pypahdb.decomposer(observation.spectrum)

    # write results to file
    pypahdb.writer(result, header=observation.header, basename=basename(splitext(observation.file_path)[0]) + '_')
