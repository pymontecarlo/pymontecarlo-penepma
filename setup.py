#!/usr/bin/env python

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASEDIR, 'README.rst'), 'r') as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()
PACKAGE_DATA = {}

#casinodir = os.path.join(BASEDIR, 'pymontecarlo_casino2', 'casino2')
#for root, _dirnames, filenames in os.walk(casinodir):
#    dirpath = os.path.join('casino2', root[len(casinodir) + 1:])
#    for filename in filenames:
#        relpath = os.path.join(dirpath, filename)
#        PACKAGE_DATA['pymontecarlo_casino2'].append(relpath)

INSTALL_REQUIRES = ['pymontecarlo', 'pypenelopetools']
EXTRAS_REQUIRE = {'develop': ['nose', 'coverage']}

CMDCLASS = versioneer.get_cmdclass()

ENTRY_POINTS = {'pymontecarlo.program':
                ['penepma = pymontecarlo_penepma.program:PenepmaProgram'],

                'pymontecarlo.formats.hdf5':
                ['PenepmaProgramHDF5Handler = pymontecarlo_penepma.formats.hdf5.program:PenepmaProgramHDF5Handler',

                 'PenepmaMaterialHDF5Handler = pymontecarlo_penepma.formats.hdf5.options.material:PenepmaMaterialHDF5Handler',
                 ],

                'pymontecarlo.formats.series':
                ['PenepmaMaterialSeriesHandler = pymontecarlo_penepma.formats.series.options.material:PenepmaMaterialSeriesHandler', ],

                'pymontecarlo.formats.html':
                ['PenepmaMaterialHtmlHandler = pymontecarlo_penepma.formats.html.options.material:PenepmaMaterialHtmlHandler', ],
                 }

setup(name="pyMonteCarlo-PENEPMA",
      version=versioneer.get_version(),
      url='https://github.com/pymontecarlo',
      description="Interface of Monte Carlo simulation program PENEPMA with pyMonteCarlo",
      author="Hendrix Demers and Philippe T. Pinard",
      author_email="hendrix.demers@mail.mcgill.ca and philippe.pinard@gmail.com",
      license="GPL v3",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],

      packages=PACKAGES,
      package_data=PACKAGE_DATA,

      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,

      cmdclass=CMDCLASS,

      entry_points=ENTRY_POINTS,

      test_suite='nose.collector',
)

