#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pymontecarlo.testcase import TestCase

from pymontecarlo_penepma.formats.series.options.material import \
    PenepmaMaterialSeriesHandler
from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class TestPenepmaMaterialSeriesHandler(TestCase):

    def testconvert(self):
        handler = PenepmaMaterialSeriesHandler()
        material = PenepmaMaterial('Brass', {29: 0.5, 30: 0.5}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        s = handler.convert(material)
        self.assertEqual(10, len(s))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
