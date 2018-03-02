#!/usr/bin/env python2
# test_spectrum.py

"""
test_spectrum.py: unit tests for class spectrum.
"""

import unittest
import numpy as np

from pypahdb import spectrum

class SpectrumTestCase(unittest.TestCase):
    """Unit tests for `spectrum.py`"""

    def test_is_instance(self):
        """Can we create an instance of spectrum?"""

        zeros = np.zeros(5)
        self.assertIsInstance(spectrum(zeros, zeros, zeros, ['empty', 'empty']), spectrum)

    def test_convert_units_micron_to_wavenumber(self):
        """Can we correctly convert micron to wavenumber?"""

        micron = np.arange(5, dtype='float') + 1
        zeros = np.zeros(5)
        s = spectrum(micron, zeros, zeros, ['micron', 'flux'])
        s.convertunitsto(aunits='wavenumber')
        self.assertEqual(s.abscissa.tolist(), (1e4 / micron[::-1]).tolist())

if __name__ == '__main__':
    unittest.main()
