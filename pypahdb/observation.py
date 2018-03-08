#!/usr/bin/env python
# observation.py

"""
observation.py: Holds and astronomical observation

This file is part of pypahdb - see the module docs for more
information.
"""

from __future__ import print_function

from astropy.io import ascii
from astropy.io import fits
from astropy import wcs
#from ipdb import set_trace as st
import numpy as np
from spectrum import spectrum


class observation(object):
    """Create an observation object for later analysis.

    Currently setup to read ASCII data.

    Attributes:
        spectrum (spectrum): contains loaded spectrum
    """

    def __init__(self, file_path):
        """Instantiate an observation object.

        Note:
            Assumes ASCII data.

        Args:
            file_path (str): String of file to load.

        """
        self.file_path = file_path
        self.header = ""
        data = ascii.read(self.file_path)
        self.spectrum = spectrum(np.array(data['col1']), np.array(data['col2']), np.zeros(len(data['col1'])), {'abscissa':{'str':'wavelength [um]'}, 'ordinate':{'str':'surface brightness [MJy/sr]'}})
