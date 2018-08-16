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
        test_dict = {'abscissa': {'type': 0, 'str': 'empty'},
                     'ordinate': {'type': 0, 'str': 'empty'}}
        test_spec = spectrum(zeros, zeros, zeros, test_dict)
        self.assertIsInstance(test_spec, spectrum)

    def test_convert_units_micron_to_wavenumber(self):
        """Can we correctly convert micron to wavenumber?"""

        micron = np.arange(5, dtype='float') + 1
        zeros = np.zeros(5)

        test_dict = {'abscissa': {'type': 0, 'str': 'empty'},
                     'ordinate': {'type': 0, 'str': 'empty'}}
        s = spectrum(micron, zeros, zeros, test_dict)
        s.convertunitsto(aunits='wavenumber')
        self.assertEqual(s.abscissa.tolist(), (1e4 / micron[::-1]).tolist())


if __name__ == '__main__':
    unittest.main()
