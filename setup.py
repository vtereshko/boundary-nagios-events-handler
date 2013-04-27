#!/usr/bin/env python
# -*- coding: utf-8 -*-

# boundary_nagios_events_handler
# setup.py

from setuptools import setup, find_packages

from boundary_nagios_events_handler import __author__, __email__, __version__, __licence__, __description__, __url__

SHARED_FILES = ['README.rst', 'COPYING', ]

setup(
    name="boundary-nagios-events-handler",
    version=__version__,
    packages=find_packages(),
    scripts=['boundary_nagios_events_handler.py', ],
    install_requires=['httplib2' ],
    package_data={
        '': SHARED_FILES,
    },
    data_files=[
        ('/usr/share/doc/boundary-nagios-events-handler/', SHARED_FILES),
    ],
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=open('README.rst').read(),
    license=__licence__,
    url=__url__,
    zip_safe=False,
    include_package_data=True
)
