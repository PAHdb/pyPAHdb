#!/usr/bin/env python2
# test_observation.py

"""
test_observation.py: unit tests for class observation.
"""

import unittest
from os import path
from pypahdb import observation


class SpectrumTestCase(unittest.TestCase):
    """Unit tests for `observation.py`"""

    def test_is_instance(self):
        """Can we create an instance of observation?"""
        file_path = path.join(path.abspath(path.dirname(__file__)),
                              'data/NGC7023.dat')
        self.assertIsInstance(observation(file_path), observation)


if __name__ == '__main__':
    unittest.main()
