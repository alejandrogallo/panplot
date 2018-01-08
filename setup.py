# -*- coding: utf-8 -*-
#
# you can install this to a local test virtualenv like so:
#   virtualenv venv
#   ./venv/bin/pip install --editable .
#   ./venv/bin/pip install --editable .[dev]  # with dev requirements, too

import sys

main_dependencies = [
    "setuptools",
]

for dep in main_dependencies:
    try:
        __import__(dep)
    except ImportError:
        print(
            "Error: You do not have %s installed, please\n"
            "       install it. For example doing\n"
            "\n"
            "       pip3 install %s\n" % (dep, dep)
        )
        sys.exit(1)


from setuptools import setup
import panplot


setup(
    name='panplot',
    version=panplot.__version__,
    maintainer='Alejandro Gallo',
    maintainer_email='aamsgallo@gmail.com',
    author=panplot.__author__,
    author_email=panplot.__email__,
    license=panplot.__license__,
    url='https://github.com/alejandrogallo/panplot',
    install_requires=[
        "configparser>=3.0.0",
    ],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    extras_require=dict(
        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[develop]
        develop=[
            "sphinx",
            'sphinx-argparse',
            'sphinx_rtd_theme',
            'pytest',
        ]
    ),
    description='Powerful and highly extensible command-line based plotting '
                'suite',
    long_description='',
    keywords=[
        'plot',
    ],
    data_files=[

        ("share/doc/panplot/", [
            "README.md",
            "AUTHORS",
            "LICENSE.txt",
        ]),

    ],
    packages=[
        "panplot",
        "panplot.commands",
    ],
    test_suite="panplot.tests",
    entry_points=dict(
        console_scripts=[
            'panplot=panplot.main:main'
        ]
    ),
    platforms=['linux', 'osx'],
)
