#!/usr/bin/env python2
# test_writer.py

"""
test_writer.py: unit tests for class writer.
"""

import unittest
import numpy as np

from pypahdb import writer

class WriterTestCase(unittest.TestCase):
    """Unit tests for `writer.py`"""

    def test_is_instance(self):
        """Can we create an instance of writer?"""

        zeros = np.zeros(5)
        self.assertIsInstance(writer(zeros), writer)

if __name__ == '__main__':
    unittest.main()
