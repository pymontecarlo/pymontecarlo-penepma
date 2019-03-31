""""""

# Standard library modules.
import os
import sys

# Third party modules.

# Local modules.
import pymontecarlo.options.base as base
from pymontecarlo.options.program.base import ProgramBase
from pymontecarlo.exceptions import ProgramNotFound

from pymontecarlo_penepma.expander import PenepmaExpander
from pymontecarlo_penepma.exporter import PenepmaExporter
from pymontecarlo_penepma.importer import PenepmaImporter
from pymontecarlo_penepma.worker import PenepmaWorker
from pymontecarlo_penepma.simulationparameters import SimulationParameters, LazySimulationParameters
from pymontecarlo_penepma.interactionforcings import InteractionForcings, LazyInteractionForcings
from pymontecarlo_penepma.referenceline import ReferenceLine, LazyReferenceLine

# Globals and constants variables.
DEFAULT = object()

class PenepmaProgram(ProgramBase):

    SIMULATION_TIME_TOLERANCE_s = 1

    def __init__(self, simulation_parameters=DEFAULT,
                 interaction_forcings=DEFAULT,
                 reference_line=DEFAULT,
                 simulation_time_s=1e38,
                 number_trajectories=1e38):
        """
        Program for PENEPMA simulation program.
        
        Args:
            simulation_parameters (SimulationParameters): 
                Simulation parameters that will be applied to all materials. 
                By default, the simulation parameters are adjusted to the 
                simulation (see :class:`LazySimulationParameters`).
            interaction_forcings (InteractionForcings):
                Defines the interaction forcings that will be applied to all
                bodies of the geometry. By default, the interaction forcings
                are adjusted to the simulation (see :class:`LazyInteractionForcings`).
            reference_line (ReferenceLine):
                Termination condition based on the relative uncertainty on 
                a certain X-ray line. By default, the reference line is defined
                as the lowest X-ray line for the simulation with a relative
                uncertainty of 5% (see :class:`LazyReferenceLine`). If
                *reference_line* is ``None``, this termination condition is
                disabled.
            simulation_time_s (int):
                Termination condition based on the simulation time (in seconds).
                By default, the simulation time is set to 1e38 (i.e. infinite).
            number_trajectories (int):
                Termination condition based on the number of simulated trajectories.
                By default, the number of trajectories is set to 1e38 (i.e. infinite).
        """
        super().__init__('PENEPMA')

        self._expander = PenepmaExpander()
        self._exporter = PenepmaExporter()
        self._importer = PenepmaImporter()
        self._worker = PenepmaWorker()

        if simulation_parameters is DEFAULT:
            simulation_parameters = LazySimulationParameters()
        self.simulation_parameters = simulation_parameters

        if interaction_forcings is DEFAULT:
            interaction_forcings = LazyInteractionForcings()
        self.interaction_forcings = interaction_forcings

        if reference_line is DEFAULT:
            reference_line = LazyReferenceLine(relative_tolerance=0.05)
        self.reference_line = reference_line

        self.simulation_time_s = simulation_time_s
        self.number_trajectories = number_trajectories

    def __eq__(self, other):
        return super().__eq__(other) and \
            self.simulation_parameters == other.simulation_parameters and \
            self.interaction_forcings == other.interaction_forcings and \
            self.reference_line == other.reference_line and \
            base.isclose(self.simulation_time_s, other.simulation_time_s, abs_tol=self.SIMULATION_TIME_TOLERANCE_s) and \
            self.number_trajectories == other.number_trajectories

    @property
    def expander(self):
        return self._expander

    @property
    def exporter(self):
        return self._exporter

    @property
    def worker(self):
        return self._worker

    @property
    def importer(self):
        return self._importer

    def _get_executable(self, filename):
        basedir = os.path.abspath(os.path.dirname(__file__))

        platform = sys.platform
        bindir = os.path.join(basedir, 'penepma', 'bin_{}'.format(platform))

        if not os.path.exists(bindir):
            raise ProgramNotFound('{} program cannot be found'.format(filename))

        if sys.platform == 'win32':
            filename += '.exe'
        filepath = os.path.join(bindir, filename)

        if not os.path.exists(filepath):
            raise ProgramNotFound('Cannot find {}. Installation might be corrupted.'
                               .format(filepath))

        return filepath

    @property
    def executable(self):
        """
        Returns the path to the PENEPMA executable.
        
        Raises
            ProgramNotFound: if the executable cannot be found
        """
        return self._get_executable('penepma')

    @property
    def material_executable(self):
        """
        Returns the path to the material executable.
        
        Raises
            ProgramNotFound: if the executable cannot be found
        """
        return self._get_executable('material')

    @property
    def pendbase_directory(self):
        """
        Returns the path to the pendbase directory.
        
        Raises
            ProgramNotFound: if the directory cannot be found
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        pendbasedir = os.path.join(basedir, 'penepma', 'pendbase')

        if not os.path.exists(pendbasedir):
            raise ProgramNotFound('pendbase directory cannot be found')

        return pendbasedir

#region HDF5

    ATTR_NUMBER_TRAJECTORIES = 'number trajectories'
    ATTR_SIMULATION_TIME = 'simulation time'
    ATTR_SIMULATION_PARAMETERS = 'simulation parameters'
    ATTR_INTERACTION_FORCINGS = 'interaction forcings'
    ATTR_REFERENCE_LINE = 'reference line'

    @classmethod
    def parse_hdf5(cls, group):
        simulation_parameters = cls._parse_hdf5(group, cls.ATTR_SIMULATION_PARAMETERS, SimulationParameters)
        interaction_forcings = cls._parse_hdf5(group, cls.ATTR_INTERACTION_FORCINGS, InteractionForcings)
        reference_line = cls._parse_hdf5(group, cls.ATTR_REFERENCE_LINE, ReferenceLine)
        simulation_time_s = cls._parse_hdf5(group, cls.ATTR_SIMULATION_TIME, float)
        number_trajectories = cls._parse_hdf5(group, cls.ATTR_NUMBER_TRAJECTORIES, int)
        return cls(simulation_parameters, interaction_forcings, reference_line, simulation_time_s, number_trajectories)

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_SIMULATION_PARAMETERS, self.simulation_parameters)
        self._convert_hdf5(group, self.ATTR_INTERACTION_FORCINGS, self.interaction_forcings)
        self._convert_hdf5(group, self.ATTR_REFERENCE_LINE, self.reference_line)
        self._convert_hdf5(group, self.ATTR_SIMULATION_TIME, self.simulation_time_s)
        self._convert_hdf5(group, self.ATTR_NUMBER_TRAJECTORIES, self.number_trajectories)

#endregion

#region Series

    def convert_series(self, builder):
        super().convert_series(builder)

        builder.add_entity(self.simulation_parameters)
        builder.add_entity(self.interaction_forcings)
        builder.add_entity(self.reference_line)
        builder.add_column('simulation time', 'simtime', self.simulation_time_s, 's', self.SIMULATION_TIME_TOLERANCE_s)
        builder.add_column('number trajectories', 'ntraj', self.number_trajectories)

#endregion

#region Document

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description('program')
        description.add_item('Number of trajectories', self.number_trajectories)
        description.add_item('Simulation time', self.simulation_time_s, 's', self.SIMULATION_TIME_TOLERANCE_s)

        # Simulation parameters
        section = builder.add_section()
        section.add_title('Simulation parameters')
        section.add_entity(self.simulation_parameters)

        # Interaction forcings
        section = builder.add_section()
        section.add_title('Interaction forcings')
        section.add_entity(self.interaction_forcings)

        # Reference line
        section = builder.add_section()
        section.add_title('Reference line')
        section.add_entity(self.reference_line)

#endregion
