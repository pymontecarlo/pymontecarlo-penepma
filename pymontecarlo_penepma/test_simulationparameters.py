""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pymontecarlo_penepma.simulationparameters import SimulationParameters
import pymontecarlo.util.testutil as testutil

# Globals and constants variables.

@pytest.fixture
def simulation_parameters():
    return SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3)

def test_simulation_parameters(simulation_parameters):
    assert simulation_parameters.eabs_electron_eV == pytest.approx(1e3, abs=1e-4)
    assert simulation_parameters.eabs_photon_eV == pytest.approx(2e3, abs=1e-4)
    assert simulation_parameters.eabs_positron_eV == pytest.approx(3e3, abs=1e-4)
    assert simulation_parameters.c1 == pytest.approx(0.1, abs=1e-4)
    assert simulation_parameters.c2 == pytest.approx(0.2, abs=1e-4)
    assert simulation_parameters.wcc_eV == pytest.approx(4e3, abs=1e-4)
    assert simulation_parameters.wcr_eV == pytest.approx(5e3, abs=1e-4)

def test_simulation_parameters_eq(simulation_parameters):
    assert simulation_parameters == SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3)

    assert simulation_parameters != SimulationParameters(99, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 99, 3e3, 0.1, 0.2, 4e3, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 2e3, 99, 0.1, 0.2, 4e3, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 2e3, 3e3, 0.09, 0.2, 4e3, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.09, 4e3, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 99, 5e3)
    assert simulation_parameters != SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 99)

def test_simulation_parameters_hdf5(simulation_parameters, tmp_path):
    testutil.assert_convert_parse_hdf5(simulation_parameters, tmp_path)

def test_simulation_parameters_copy(simulation_parameters):
    testutil.assert_copy(simulation_parameters)

def test_simulation_parameters_pickle(simulation_parameters):
    testutil.assert_pickle(simulation_parameters)

def test_simulation_parameters_series(simulation_parameters, seriesbuilder):
    simulation_parameters.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 7

def test_simulation_parameters_document(simulation_parameters, documentbuilder):
    simulation_parameters.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 12
