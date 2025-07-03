#!/usr/bin/env python3
# test_decomposer.py

"""
test_spectrum.py: unit tests for class decomposer.
"""

import unittest
import os.path
import numpy as np
import matplotlib

from astropy.wcs import WCS
from astropy import units as u

from pypahdb.observation import Observation
from pypahdb.decomposer import Decomposer


class DecomposerTestCase(unittest.TestCase):
    """Unit tests for `decomposer.py`."""

    def setUp(self):
        import importlib_resources
        import tempfile

        file_name = "resources/sample_data_NGC7023.tbl"
        file_path = importlib_resources.files("pypahdb") / file_name
        self.observation = Observation(file_path)
        self.decomposer = Decomposer(self.observation.spectrum)
        self.tmpdir = tempfile.gettempdir()

    def test_is_instance(self):
        """Can we create an instance of Decomposer?"""
        assert isinstance(self.decomposer, Decomposer)

    def test_has_fit(self):
        """Can we create a fit?"""
        assert isinstance(self.decomposer.fit, np.ndarray)

    def test_has_charge_fractions(self):
        """Can we create an charge fractions?"""
        assert isinstance(self.decomposer.charge_fractions, dict)

    def test_has_size_fractions(self):
        """Can we calculate a size fractions?"""
        assert isinstance(self.decomposer.size_fractions, dict)

    def test_has_charge(self):
        """Can we generate a charge results?"""
        assert isinstance(self.decomposer.charge, dict)

    def test_has_size(self):
        """Can we generate a size results?"""
        assert isinstance(self.decomposer.size, dict)

    def test_has_nc(self):
        """Can we generate an nc results?"""
        assert isinstance(self.decomposer.nc, u.quantity.Quantity)

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

    def test_plot_map(self):
        assert isinstance(
            Decomposer.plot_map(
                np.ones((1, 1)), np.ones((1, 1), dtype=bool), "dummy", WCS()
            ),
            matplotlib.figure.Figure,
        )


if __name__ == "__main__":
    unittest.main()
