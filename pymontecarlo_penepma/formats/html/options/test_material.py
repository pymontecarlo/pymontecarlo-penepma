#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pymontecarlo.testcase import TestCase

from pymontecarlo_penepma.formats.html.options.material import PenepmaMaterialHtmlHandler
from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class TestPenepmaMaterialHtmlHandler(TestCase):

    def testconvert(self):
        handler = PenepmaMaterialHtmlHandler()
        material = PenepmaMaterial('Brass', {29: 0.5, 30: 0.5}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        root = handler.convert(material)
        self.assertEqual(1, len(root.children))

#        with open('/tmp/test.html', 'w') as fp:
#            fp.write(root.render())

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
