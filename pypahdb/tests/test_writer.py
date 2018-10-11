#!/usr/bin/env python2
# test_writer.py

"""
test_writer.py: unit tests for class Writer.
"""

import unittest
import numpy as np

from pypahdb.writer import Writer


class WriterTestCase(unittest.TestCase):
    """Unit tests for `writer.py`"""

    def test_is_instance(self):
        """Can we create an instance of writer?"""

        zeros = np.zeros(5)
        self.assertIsInstance(Writer(zeros), Writer)


if __name__ == '__main__':
    unittest.main()
