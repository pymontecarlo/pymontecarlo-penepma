""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pymontecarlo.formats.html.options.material import MaterialHtmlHandler

from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class PenepmaMaterialHtmlHandler(MaterialHtmlHandler):

    def convert_rows(self, material):
        rows = super().convert_rows(material)
        row = rows[0]

        key = self._create_label('Absorption energy electron', 'eV')
        value = self._format_value(material.absorption_energy_electron_eV, 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        row[key] = value

        key = self._create_label('Absorption energy photon', 'eV')
        value = self._format_value(material.absorption_energy_photon_eV, 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        row[key] = value

        key = self._create_label('Absorption energy positron', 'eV')
        value = self._format_value(material.absorption_energy_positron_eV, 'eV', PenepmaMaterial.ABSORPTION_ENERGY_TOLERANCE_eV)
        row[key] = value

        key = self._create_label('Elastic scattering C1')
        value = self._format_value(material.elastic_scattering_c1, None, PenepmaMaterial.ELASTIC_SCATTERING_TOLERANCE)
        row[key] = value

        key = self._create_label('Elastic scattering C2')
        value = self._format_value(material.elastic_scattering_c2, None, PenepmaMaterial.ELASTIC_SCATTERING_TOLERANCE)
        row[key] = value

        key = self._create_label('Cutoff energy inelastic', 'eV')
        value = self._format_value(material.cutoff_energy_inelastic_eV, 'eV', PenepmaMaterial.CUTOFF_ENERGY_TOLERANCE_eV)
        row[key] = value

        key = self._create_label('Cutoff energy Bremsstrahlung', 'eV')
        value = self._format_value(material.cutoff_energy_bremsstrahlung_eV, 'eV', PenepmaMaterial.CUTOFF_ENERGY_TOLERANCE_eV)
        row[key] = value

        return rows

    @property
    def CLASS(self):
        return PenepmaMaterial
