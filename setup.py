#!/usr/bin/env python

from setuptools import setup, find_packages
from rivalcfg import VERSION

setup(
    name="rivalcfg",
    version=VERSION,
    description="Configure SteelSeries Rival gaming mice",
    url="https://github.com/flozz/rivalcfg",
    license="WTFPL",

    long_description="""
    rivalcfg is a small CLI utility program that allows you to configure
    SteelSeries Rival gaming mice on Linux.

    Supported mice:

    * ~~SteelSeries Rival~~ **WORK IN PROGRESS**
    * SteelSeries Rival 100
    * ~~SteelSeries Rival 300~~ **WORK IN PROGRESS**


    Usage: rivalcfg [options]

    Type "rivalcfg --help" to list available options.
    """,

    author="Fabien LOISON",
    author_email="http://www.flozz.fr/",

    keywords="steelseries rival rival100 mouse",
    platforms=["Linux"],

    packages=find_packages(),

    install_requires=[
        "pyudev>=0.19.0"
    ],

    entry_points = {
        "console_scripts": [
            "rivalcfg = rivalcfg.cli:main"
        ]
    },
)

