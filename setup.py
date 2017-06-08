# -*- coding: utf-8 -*-
#
# you can install this to a local test virtualenv like so:
#   virtualenv venv
#   ./venv/bin/pip install --editable .
#   ./venv/bin/pip install --editable .[dev]  # with dev requirements, too

from __future__ import print_function

from setuptools import setup

from panplot import __version__
import re

def get_requirements(reqs="requirements.txt"):
    reqs = [
        line
        for line in open(reqs).read().split("\n")[0:-1]
        if not re.match(r"git\+", line)
    ]
    print(reqs)
    return reqs


setup(
    name='panplot',
    version=__version__,
    maintainer='Alejandro Gallo',
    maintainer_email='aamsgallo@gmail.com',
    license='GPLv3',
    url='https://github.com/alejandrogallo/panplot',
    install_requires=get_requirements(),
    extras_require=dict(
        dev=[]
    ),
    description='Simple program to plot',
    long_description='Simple program to plot',
    keywords=[
        'plot'
    ],
    packages=[
        "panplot",
        "panplot.commands"
    ],
    test_suite="panplot.tests",
    entry_points=dict(
        console_scripts=[
            'panplot=panplot.main:main'
        ]
    ),
    platforms=['linux'],
)
