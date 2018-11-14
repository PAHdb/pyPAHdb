#!/usr/bin/env python3
# test_decomposer.py

"""
test_spectrum.py: unit tests for class spectrum.
"""

import unittest
import pkg_resources

from pypahdb.observation import Observation
from pypahdb.decomposer import Decomposer


class DecomposerTestCase(unittest.TestCase):
    """Unit tests for `decomposer.py`"""

    def test_is_instance(self):
        """Can we create an instance of Decomposer?"""
        file_name = 'data/sample_data_NGC7023.dat'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)
        observation = Observation(file_path)

        self.assertIsInstance(Decomposer(observation.spectrum), Decomposer)


if __name__ == '__main__':
    unittest.main()
