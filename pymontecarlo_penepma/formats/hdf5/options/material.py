""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pymontecarlo.formats.hdf5.options.material import MaterialHDF5Handler
from pymontecarlo_penepma.options.material import PenepmaMaterial

# Globals and constants variables.

class PenepmaMaterialHDF5Handler(MaterialHDF5Handler):

    ATTR_ABSORPTION_ENERGY_ELECTRON = 'absorption energy electron'
    ATTR_ABSORPTION_ENERGY_PHOTON = 'absorption energy photon'
    ATTR_ABSORPTION_ENERGY_POSITRON = 'absorption energy positron'
    ATTR_ELASTIC_SCATTERING_C1 = 'elastic scattering c1'
    ATTR_ELASTIC_SCATTERING_C2 = 'elastic scattering c2'
    ATTR_CUTOFF_ENERGY_INELASTIC = 'cutoff energy inelastic'
    ATTR_CUTOFF_ENERGY_BREMSSTRAHLUNG = 'cutoff energy Bremsstrahlung'

    def _parse_absorption_energy_electron(self, group):
        return float(group.attrs[self.ATTR_ABSORPTION_ENERGY_ELECTRON])

    def _parse_absorption_energy_photon(self, group):
        return float(group.attrs[self.ATTR_ABSORPTION_ENERGY_PHOTON])

    def _parse_absorption_energy_positron(self, group):
        return float(group.attrs[self.ATTR_ABSORPTION_ENERGY_POSITRON])

    def _parse_elastic_scattering_c1(self, group):
        return float(group.attrs[self.ATTR_ELASTIC_SCATTERING_C1])

    def _parse_elastic_scattering_c2(self, group):
        return float(group.attrs[self.ATTR_ELASTIC_SCATTERING_C2])

    def _parse_cutoff_energy_inelastic(self, group):
        return float(group.attrs[self.ATTR_CUTOFF_ENERGY_INELASTIC])

    def _parse_cutoff_energy_bremsstrahlung(self, group):
        return float(group.attrs[self.ATTR_CUTOFF_ENERGY_BREMSSTRAHLUNG])

    def can_parse(self, group):
        return super().can_parse(group) and \
            self.ATTR_ABSORPTION_ENERGY_ELECTRON in group.attrs and \
            self.ATTR_ABSORPTION_ENERGY_PHOTON in group.attrs and \
            self.ATTR_ABSORPTION_ENERGY_POSITRON in group.attrs and \
            self.ATTR_ELASTIC_SCATTERING_C1 in group.attrs and \
            self.ATTR_ELASTIC_SCATTERING_C2 in group.attrs and \
            self.ATTR_CUTOFF_ENERGY_INELASTIC in group.attrs and \
            self.ATTR_CUTOFF_ENERGY_BREMSSTRAHLUNG in group.attrs

    def parse(self, group):
        name = self._parse_name(group)
        composition = self._parse_composition(group)
        density_kg_per_m3 = self._parse_density_kg_per_m3(group)
        eabsel = self._parse_absorption_energy_electron(group)
        eabsph = self._parse_absorption_energy_photon(group)
        eabspo = self._parse_absorption_energy_positron(group)
        c1 = self._parse_elastic_scattering_c1(group)
        c2 = self._parse_elastic_scattering_c2(group)
        wcc = self._parse_cutoff_energy_inelastic(group)
        wcr = self._parse_cutoff_energy_bremsstrahlung(group)
        return self.CLASS(name, composition, density_kg_per_m3,
                          eabsel, eabsph, eabspo, c1, c2, wcc, wcr)

    def _convert_absorption_energy_electron(self, material, group):
        group.attrs[self.ATTR_ABSORPTION_ENERGY_ELECTRON] = material.absorption_energy_electron_eV

    def _convert_absorption_energy_photon(self, material, group):
        group.attrs[self.ATTR_ABSORPTION_ENERGY_PHOTON] = material.absorption_energy_photon_eV

    def _convert_absorption_energy_positron(self, material, group):
        group.attrs[self.ATTR_ABSORPTION_ENERGY_POSITRON] = material.absorption_energy_positron_eV

    def _convert_elastic_scattering_c1(self, material, group):
        group.attrs[self.ATTR_ELASTIC_SCATTERING_C1] = material.elastic_scattering_c1

    def _convert_elastic_scattering_c2(self, material, group):
        group.attrs[self.ATTR_ELASTIC_SCATTERING_C2] = material.elastic_scattering_c2

    def _convert_cutoff_energy_inelastic(self, material, group):
        group.attrs[self.ATTR_CUTOFF_ENERGY_INELASTIC] = material.cutoff_energy_inelastic_eV

    def _convert_cutoff_energy_bremsstrahlung(self, material, group):
        group.attrs[self.ATTR_CUTOFF_ENERGY_BREMSSTRAHLUNG] = material.cutoff_energy_bremsstrahlung_eV

    def convert(self, material, group):
        super().convert(material, group)
        self._convert_absorption_energy_electron(material, group)
        self._convert_absorption_energy_photon(material, group)
        self._convert_absorption_energy_positron(material, group)
        self._convert_elastic_scattering_c1(material, group)
        self._convert_elastic_scattering_c2(material, group)
        self._convert_cutoff_energy_inelastic(material, group)
        self._convert_cutoff_energy_bremsstrahlung(material, group)

    @property
    def CLASS(self):
        return PenepmaMaterial
