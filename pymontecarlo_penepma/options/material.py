""""""

# Standard library modules.
import math

# Third party modules.

# Local modules.
from pymontecarlo.options.material import Material
from pymontecarlo.options.composition import to_repr

# Globals and constants variables.

class PenepmaMaterial(Material):

    ABSORPTION_ENERGY_TOLERANCE_eV = 1e-2 # 0.01 eV
    ELASTIC_SCATTERING_TOLERANCE = 1e-6
    CUTOFF_ENERGY_TOLERANCE_eV = 1e-2 # 0.01 eV

    def __init__(self, name, composition, density_kg_per_m3,
                 absorption_energy_electron_eV=1e3,
                 absorption_energy_photon_eV=1e3,
                 absorption_energy_positron_eV=1e3,
                 elastic_scattering_c1=0.1,
                 elastic_scattering_c2=0.1,
                 cutoff_energy_inelastic_eV=1e3,
                 cutoff_energy_bremsstrahlung_eV=1e3,
                 color=None):
        """
        Creates a new material, compatible with PENEPMA.

        :arg composition: composition in weight fraction.
            The composition is specified by a dictionary.
            The keys are atomic numbers and the values are weight fraction 
            between ]0.0, 1.0].
        :type composition: :class:`dict`

        :arg name: name of the material
        :type name: :class:`str`

        :arg density_kg_per_m3: material's density in kg/m3.
        :type density_kg_per_m3: :class:`float`
        
        :arg absorption_energy_electron_eV: absorption energy of electron in eV.
            Electrons are tracked down to this energy.
        :type absorption_energy_electron_eV: :class:`float`
        
        :arg absorption_energy_photon_eV: absorption energy of photon in eV.
            Photons are tracked down to this energy.
        :type absorption_energy_photon_eV: :class:`float`
        
        :arg absorption_energy_positron_eV: absorption energy of positron in eV.
            Positrons are tracked down to this energy.
        :type absorption_energy_positron_eV: :class:`float`
        
        :arg elastic_scattering_c1: elastic scattering parameters C1
        :type elastic_scattering_c1: :class:`float`
        
        :arg elastic_scattering_c2: elastic scattering parameters C2
        :type elastic_scattering_c2: :class:`float`
        
        :arg cutoff_energy_inelastic_eV: cutoff energy losses for inelastic collisions
        :type cutoff_energy_inelastic_eV: :class:`float`
        
        :arg cutoff_energy_bremsstrahlung_eV: cutoff energy losses for Bremsstrahlung emission
        :type cutoff_energy_bremsstrahlung_eV: :class:`float`
        
        :arg color: color representing a material. If ``None``, a color is
            automatically selected from the provided color set. See
            :meth:`set_color_set`.
        """

        super().__init__(name, composition, density_kg_per_m3, color)

        self.absorption_energy_electron_eV = absorption_energy_electron_eV
        self.absorption_energy_photon_eV = absorption_energy_photon_eV
        self.absorption_energy_positron_eV = absorption_energy_positron_eV
        self.elastic_scattering_c1 = elastic_scattering_c1
        self.elastic_scattering_c2 = elastic_scattering_c2
        self.cutoff_energy_inelastic_eV = cutoff_energy_inelastic_eV
        self.cutoff_energy_bremsstrahlung_eV = cutoff_energy_bremsstrahlung_eV

    def __repr__(self):
        return '<{classname}({name}, {composition}, {density:g} kg/m3, abs. electron={eabsel} eV, abs. photon={eabsph} eV, abs. positron={eabspo} eV, c1={c1}, c2={c2}, wcc={wcc} eV, wcr={wcr} eV)>' \
            .format(classname=self.__class__.__name__,
                    name=self.name,
                    composition=to_repr(self.composition),
                    density=self.density_kg_per_m3,
                    eabsel=self.absorption_energy_electron_eV,
                    eabsph=self.absorption_energy_photon_eV,
                    eabspo=self.absorption_energy_positron_eV,
                    c1=self.elastic_scattering_c1,
                    c2=self.elastic_scattering_c2,
                    wcc=self.cutoff_energy_inelastic_eV,
                    wcr=self.cutoff_energy_bremsstrahlung_eV)

    def __eq__(self, other):
        # NOTE: color is not tested in equality
        return super().__eq__(other) and \
            math.isclose(self.absorption_energy_electron_eV, other.absorption_energy_electron_eV, abs_tol=self.ABSORPTION_ENERGY_TOLERANCE_eV) and \
            math.isclose(self.absorption_energy_photon_eV, other.absorption_energy_photon_eV, abs_tol=self.ABSORPTION_ENERGY_TOLERANCE_eV) and \
            math.isclose(self.absorption_energy_positron_eV, other.absorption_energy_positron_eV, abs_tol=self.ABSORPTION_ENERGY_TOLERANCE_eV) and \
            math.isclose(self.elastic_scattering_c1, other.elastic_scattering_c1, abs_tol=self.ELASTIC_SCATTERING_TOLERANCE) and \
            math.isclose(self.elastic_scattering_c2, other.elastic_scattering_c2, abs_tol=self.ELASTIC_SCATTERING_TOLERANCE) and \
            math.isclose(self.cutoff_energy_inelastic_eV, other.cutoff_energy_inelastic_eV, abs_tol=self.CUTOFF_ENERGY_TOLERANCE_eV) and \
            math.isclose(self.cutoff_energy_bremsstrahlung_eV, other.cutoff_energy_bremsstrahlung_eV, abs_tol=self.CUTOFF_ENERGY_TOLERANCE_eV)
