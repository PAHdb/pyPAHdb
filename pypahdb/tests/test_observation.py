#!/usr/bin/env python3
# test_observation.py

"""
test_observation.py: unit tests for class observation.
"""

import unittest
import pkg_resources

from pypahdb import observation


class SpectrumTestCase(unittest.TestCase):
    """Unit tests for `observation.py`"""

    def test_is_instance(self):
        """Can we create an instance of observation?"""
        file_name = 'data/sample_data_NGC7023.dat'
        file_path = pkg_resources.resource_filename('pypahdb', file_name)

        self.assertIsInstance(observation(file_path), observation)


if __name__ == '__main__':
    unittest.main()
