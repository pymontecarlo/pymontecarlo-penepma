#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pymontecarlo.testcase import TestCase

from pymontecarlo_penepma.formats.hdf5.options.material import \
    PenepmaMaterialHDF5Handler
from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class TestPenepmaMaterialHDF5Handler(TestCase):

    def testconvert_parse(self):
        handler = PenepmaMaterialHDF5Handler()
        material = PenepmaMaterial('Brass', {29: 0.5, 30: 0.5}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        material2 = self.convert_parse_hdf5handler(handler, material)
        self.assertEqual(material2, material)

#        import h5py
#        with h5py.File('/tmp/material.h5', 'w') as f:
#            handler.convert(material, f)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
