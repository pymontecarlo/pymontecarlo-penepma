""""""

# Standard library modules.

# Third party modules.
import pytest

import pyxray

# Local modules.
from pymontecarlo_penepma.referenceline import ReferenceLine

import pymontecarlo.util.testutil as testutil
from pymontecarlo.options.detector import PhotonDetector

# Globals and constants variables.


@pytest.fixture
def reference_line():
    xrayline = pyxray.xray_line(13, 'Ka1')
    photon_detector = PhotonDetector('det', 0.5, 0.6)
    return ReferenceLine(xrayline, photon_detector, 0.05)

def test_reference_line(reference_line):
    assert reference_line.xrayline == pyxray.xray_line(13, 'Ka1')
    assert reference_line.photon_detector.name == 'det'
    assert reference_line.relative_tolerance == pytest.approx(0.05, abs=1e-4)

def test_reference_line_eq(reference_line):
    xrayline = pyxray.xray_line(13, 'Ka1')
    photon_detector = PhotonDetector('det', 0.5, 0.6)
    assert reference_line == ReferenceLine(xrayline, photon_detector, 0.05)

    assert reference_line != ReferenceLine(pyxray.xray_line(14, 'Ka1'), photon_detector, 0.05)
    assert reference_line != ReferenceLine(xrayline, PhotonDetector('det2', 0.5, 0.6), 0.05)
    assert reference_line != ReferenceLine(xrayline, photon_detector, 0.99)

def test_reference_line_hdf5(reference_line, tmp_path):
    testutil.assert_convert_parse_hdf5(reference_line, tmp_path)

def test_reference_line_copy(reference_line):
    testutil.assert_copy(reference_line)

def test_reference_line_pickle(reference_line):
    testutil.assert_pickle(reference_line)

def test_reference_line_series(reference_line, seriesbuilder):
    reference_line.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 3

def test_reference_line_document(reference_line, documentbuilder):
    reference_line.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 8
