""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pymontecarlo.formats.series.options.material import MaterialSeriesHandler
from pymontecarlo.formats.series.base import NamedSeriesColumn

from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class PenepmaMaterialSeriesHandler(MaterialSeriesHandler):

    def convert(self, material):
        s = super().convert(material)

        column = NamedSeriesColumn('absorption energy electron', 'EABS(1)', 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        s[column] = material.absorption_energy_electron_eV

        column = NamedSeriesColumn('absorption energy photon', 'EABS(2)', 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        s[column] = material.absorption_energy_photon_eV

        column = NamedSeriesColumn('absorption energy positron', 'EABS(3)', 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        s[column] = material.absorption_energy_positron_eV

        column = NamedSeriesColumn('elastic scattering C1', 'C1', None, PenepmaMaterial.ELASTIC_SCATTERING_TOLERANCE)
        s[column] = material.elastic_scattering_c1

        column = NamedSeriesColumn('elastic scattering C2', 'C2', None, PenepmaMaterial.ELASTIC_SCATTERING_TOLERANCE)
        s[column] = material.elastic_scattering_c2

        column = NamedSeriesColumn('cutoff energy inelastic', 'WCC', 'eV', PenepmaMaterial.CUTOFF_ENERGY_TOLERANCE_eV)
        s[column] = material.cutoff_energy_inelastic_eV

        column = NamedSeriesColumn('cutoff energy Bremsstrahlung', 'WCR', 'eV', PenepmaMaterial.CUTOFF_ENERGY_TOLERANCE_eV)
        s[column] = material.cutoff_energy_bremsstrahlung_eV

        return s

    @property
    def CLASS(self):
        return PenepmaMaterial
