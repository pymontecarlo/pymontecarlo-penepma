""""""

# Standard library modules.

# Third party modules.

# Local modules.
import pymontecarlo.options.base as base
from pymontecarlo.util.xrayline import find_reference_xrayline, convert_xrayline
from pymontecarlo.options.detector import PhotonDetector

# Globals and constants variables.

class ReferenceLine(base.OptionBase):

    RELATIVE_TOLERANCE_TOLERANCE = 1e-4 # 0.01%

    def __init__(self, xrayline, photon_detector, relative_tolerance):
        super().__init__()

        self.xrayline = xrayline
        self.photon_detector = photon_detector
        self.relative_tolerance = relative_tolerance

    def __eq__(self, other):
        return super().__eq__(other) and \
            base.isclose(self.xrayline, other.xrayline) and \
            base.isclose(self.photon_detector, other.photon_detector) and \
            base.isclose(self.relative_tolerance, other.relative_tolerance, abs_tol=self.RELATIVE_TOLERANCE_TOLERANCE)

#region HDF5

    ATTR_XRAYLINE = 'xray line'
    ATTR_PHOTON_DETECTOR = 'photon detector'
    ATTR_RELATIVE_TOLERANCE = 'relative tolerance'

    @classmethod
    def parse_hdf5(cls, group):
        xrayline = convert_xrayline(cls._parse_hdf5(group, cls.ATTR_XRAYLINE, str).split())
        photon_detector = cls._parse_hdf5(group, cls.ATTR_PHOTON_DETECTOR, PhotonDetector)
        relative_tolerance = cls._parse_hdf5(group, cls.ATTR_RELATIVE_TOLERANCE, float)
        return cls(xrayline, photon_detector, relative_tolerance)

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_XRAYLINE, self.xrayline.iupac)
        self._convert_hdf5(group, self.ATTR_PHOTON_DETECTOR, self.photon_detector)
        self._convert_hdf5(group, self.ATTR_RELATIVE_TOLERANCE, self.relative_tolerance)

#endregion

#region Series

    def convert_series(self, builder):
        super().convert_series(builder)
        builder.add_column('reference xray line', 'ref xray', self.xrayline)
        builder.add_column('reference photon detector', 'ref detector', self.photon_detector.name)
        builder.add_column('reference relative tolerance', 'ref tolerance', self.relative_tolerance, None, self.RELATIVE_TOLERANCE_TOLERANCE)

#endregion

#region Document

    DESCRIPTION_REFERENCE_LINE = 'reference line'

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(self.DESCRIPTION_REFERENCE_LINE)
        description.add_item('X-ray line', self.xrayline)
        description.add_item('Photon detector', self.photon_detector.name)
        description.add_item('Relative tolerance', self.relative_tolerance, None, self.RELATIVE_TOLERANCE_TOLERANCE)

#endregion

class LazyReferenceLine(base.LazyOptionBase):

    def __init__(self, relative_tolerance=0.05):
        self.relative_tolerance = relative_tolerance

    def apply(self, parent_option, options):
        photon_detectors = options.find_detectors(PhotonDetector)
        if not photon_detectors:
            return None

        xrayline = find_reference_xrayline(options)

        detector_elevations = {}
        for photon_detector in photon_detectors:
            detector_elevations[photon_detector.elevation_rad] = photon_detector

        photon_detector = detector_elevations[min(detector_elevations.keys())]

        return ReferenceLine(xrayline, photon_detector, self.relative_tolerance)

    def convert_document(self, builder):
        super().convert_document(builder)

        text = ('Default reference line created using '
                'the X-ray line with the lower energy, '
                'photon detector with the lowest elevation and '
                'a tolerance of {:.2f}%'.format(self.relative_tolerance))
        builder.add_text(text)
