#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pymontecarlo.testcase import TestCase

from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class TestPenepmaMaterial(TestCase):

    def setUp(self):
        super().setUp()

        self.m = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0,
                                 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3,
                                 '#FF0000')

    def testskeleton(self):
        self.assertTrue(True)

        self.assertEqual('Pure Cu', str(self.m))
        self.assertEqual('Pure Cu', self.m.name)

        self.assertTrue(29 in self.m.composition)
        self.assertAlmostEqual(1.0, self.m.composition[29])

        self.assertAlmostEqual(8960.0, self.m.density_kg_per_m3, 4)
        self.assertAlmostEqual(8.960, self.m.density_g_per_cm3, 4)

        self.assertAlmostEqual(2e3, self.m.absorption_energy_electron_eV, 4)
        self.assertAlmostEqual(3e3, self.m.absorption_energy_photon_eV, 4)
        self.assertAlmostEqual(4e3, self.m.absorption_energy_positron_eV, 4)

        self.assertAlmostEqual(0.15, self.m.elastic_scattering_c1, 4)
        self.assertAlmostEqual(0.16, self.m.elastic_scattering_c2, 4)

        self.assertAlmostEqual(5e3, self.m.cutoff_energy_inelastic_eV, 4)
        self.assertAlmostEqual(6e3, self.m.cutoff_energy_bremsstrahlung_eV, 4)

        self.assertEqual('#FF0000', self.m.color)

    def testpure(self):
        m = PenepmaMaterial.pure(29)

        self.assertEqual('Copper', str(m))

        self.assertIn(29, m.composition)
        self.assertAlmostEqual(1.0, m.composition[29], 4)

        self.assertAlmostEqual(8.96, m.density_kg_per_m3 / 1000.0, 4)
        self.assertAlmostEqual(8.96, m.density_g_per_cm3, 4)

        self.assertAlmostEqual(1e3, m.absorption_energy_electron_eV, 4)
        self.assertAlmostEqual(1e3, m.absorption_energy_photon_eV, 4)
        self.assertAlmostEqual(1e3, m.absorption_energy_positron_eV, 4)

        self.assertAlmostEqual(0.1, m.elastic_scattering_c1, 4)
        self.assertAlmostEqual(0.1, m.elastic_scattering_c2, 4)

        self.assertAlmostEqual(1e3, m.cutoff_energy_inelastic_eV, 4)
        self.assertAlmostEqual(1e3, m.cutoff_energy_bremsstrahlung_eV, 4)

    def testfrom_formula(self):
        m = PenepmaMaterial.from_formula('SiO2', 1250.0)

        self.assertEqual('SiO2', str(m))

        self.assertIn(14, m.composition)
        self.assertAlmostEqual(0.4674, m.composition[14], 4)

        self.assertIn(8, m.composition)
        self.assertAlmostEqual(0.5326, m.composition[8], 4)

        self.assertAlmostEqual(1.25, m.density_kg_per_m3 / 1000.0, 4)
        self.assertAlmostEqual(1.25, m.density_g_per_cm3, 4)

        self.assertAlmostEqual(1e3, m.absorption_energy_electron_eV, 4)
        self.assertAlmostEqual(1e3, m.absorption_energy_photon_eV, 4)
        self.assertAlmostEqual(1e3, m.absorption_energy_positron_eV, 4)

        self.assertAlmostEqual(0.1, m.elastic_scattering_c1, 4)
        self.assertAlmostEqual(0.1, m.elastic_scattering_c2, 4)

        self.assertAlmostEqual(1e3, m.cutoff_energy_inelastic_eV, 4)
        self.assertAlmostEqual(1e3, m.cutoff_energy_bremsstrahlung_eV, 4)

    def test__repr__(self):
        expected = '<PenepmaMaterial(Pure Cu, 100%Cu, 8960 kg/m3, abs. electron=2000.0 eV, abs. photon=3000.0 eV, abs. positron=4000.0 eV, c1=0.15, c2=0.16, wcc=5000.0 eV, wcr=6000.0 eV)>'
        self.assertEqual(expected, repr(self.m))

    def test__eq__(self):
        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        self.assertEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8961.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 0.5, 30: 0.5}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 9e3, 3e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 9e3, 4e3, 0.15, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 9e3, 0.15, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 4e3, 0.9, 0.16, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.9, 5e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 9e3, 6e3)
        self.assertNotEqual(m2, self.m)

        m2 = PenepmaMaterial('Pure Cu', {29: 1.0}, 8960.0, 2e3, 3e3, 4e3, 0.15, 0.16, 5e3, 9e3)
        self.assertNotEqual(m2, self.m)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
