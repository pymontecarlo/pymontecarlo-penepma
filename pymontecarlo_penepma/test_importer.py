""""""

# Standard library modules.
import os

# Third party modules.
import pytest

# Local modules.
from pymontecarlo_penepma.importer import PenepmaImporter

# Globals and constants variables.

@pytest.fixture
def importer():
    return PenepmaImporter()

@pytest.mark.asyncio
async def test_import(event_loop, importer, options, testdatadir):
    dirpath = os.path.join(testdatadir, 'sim1')

    results = await importer.import_(options, dirpath)

    assert len(results) == 2
