#!/usr/bin/env python3
# test_decomposer.py

"""
test_spectrum.py: unit tests for class decomposer.
"""

import unittest
import pytest

import numpy as np

from pypahdb.observation import Observation
from pypahdb.decomposer import Decomposer


@pytest.fixture(scope='class', autouse=True)
def observation_obj():
    import pkg_resources
    file_name = 'data/sample_data_NGC7023.dat'
    file_path = pkg_resources.resource_filename('pypahdb', file_name)
    return Observation(file_path)


class DecomposerTestCase(unittest.TestCase):
    """Unit tests for `decomposer.py`"""

    def test_is_instance(self):
        """Can we create an instance of Decomposer?"""
        observation = observation_obj()
        self.assertIsInstance(Decomposer(observation.spectrum), Decomposer)

    def test_has_fit(self):
        """Can we create a fit?"""
        observation = observation_obj()
        result = Decomposer(observation.spectrum)
        self.assertIsInstance(result.fit, np.ndarray)

    def test_has_ionized_fraction(self):
        """Can we create an ionized fraction?"""
        observation = observation_obj()
        result = Decomposer(observation.spectrum)
        self.assertIsInstance(result.ionized_fraction, np.ndarray)

    def test_has_large_fraction(self):
        """Can we calculate a large fraction?"""
        observation = observation_obj()
        result = Decomposer(observation.spectrum)
        self.assertIsInstance(result.large_fraction, np.ndarray)

    def test_has_charge(self):
        """Can we generate a charge results?"""
        observation = observation_obj()
        result = Decomposer(observation.spectrum)
        self.assertIsInstance(result.charge, dict)

    def test_has_size(self):
        """Can we generate a size results?"""
        observation = observation_obj()
        result = Decomposer(observation.spectrum)
        self.assertIsInstance(result.size, dict)


if __name__ == '__main__':
    unittest.main()
