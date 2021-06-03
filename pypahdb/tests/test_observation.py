#!/usr/bin/env python3
# test_observation.py

"""
test_observation.py: unit tests for class observation.
"""

import unittest
import pkg_resources

from pypahdb.observation import Observation


class SpectrumTestCase(unittest.TestCase):
    """Unit tests for `observation.py`"""

    def test_read_spectrum1d(self):
        """Can we create an instance of Observation from a Spectrum1D file?"""
        file_name = 'resources/sample_data_jwst.fits'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)

        assert isinstance(Observation(file_path), Observation)

    def test_read_ascii(self):
        """Can we create an instance of Observation from an ASCII file?"""
        file_name = 'resources/sample_data_NGC7023.tbl'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)

        assert isinstance(Observation(file_path), Observation)

    def test_read_fits(self):
        """Can we create an instance of Observation from a FITS file?"""
        file_name = 'resources/sample_data_NGC7023.fits'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)

        assert isinstance(Observation(file_path), Observation)


if __name__ == '__main__':
    unittest.main()
