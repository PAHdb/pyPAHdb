#!/usr/bin/env python3
# test_decomposer.py

"""
test_spectrum.py: unit tests for class decomposer.
"""

import unittest
import os.path
import numpy as np

from pypahdb.observation import Observation
from pypahdb.decomposer import Decomposer


class DecomposerTestCase(unittest.TestCase):
    """Unit tests for `decomposer.py`."""

    def setUp(self):
        import pkg_resources
        import tempfile
        file_name = 'resources/sample_data_NGC7023.tbl'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)
        self.observation = Observation(file_path)
        self.decomposer = Decomposer(self.observation.spectrum)
        self.tmpdir = tempfile.gettempdir()

    def test_is_instance(self):
        """Can we create an instance of Decomposer?"""
        assert isinstance(self.decomposer, Decomposer)

    def test_has_fit(self):
        """Can we create a fit?"""
        assert isinstance(self.decomposer.fit, np.ndarray)

    def test_has_ionized_fraction(self):
        """Can we create an ionized fraction?"""
        assert isinstance(self.decomposer.ionized_fraction, np.ndarray)

    def test_has_large_fraction(self):
        """Can we calculate a large fraction?"""
        assert isinstance(self.decomposer.large_fraction, np.ndarray)

    def test_has_charge(self):
        """Can we generate a charge results?"""
        assert isinstance(self.decomposer.charge, dict)

    def test_has_size(self):
        """Can we generate a size results?"""
        assert isinstance(self.decomposer.size, dict)

    def test_do_pdf(self):
        """Can we output a PDF?"""
        ofile = os.path.join(self.tmpdir, "result.pdf")
        self.decomposer.save_pdf(ofile)
        assert os.path.isfile(ofile)

    def test_do_fits(self):
        """Can we output FITS?"""
        ofile = os.path.join(self.tmpdir, "result.pdf")
        self.decomposer.save_fits(ofile)
        assert os.path.isfile(ofile)


if __name__ == '__main__':
    unittest.main()
