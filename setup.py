#!/usr/bin/env python

from setuptools import setup, find_packages
from rivalcfg import VERSION

setup(
    name="rivalcfg",
    version=VERSION,
    description="Configure the SteelSeries Rival 100 gaming mouse",
    long_description=open("README.md").read(),
    url="https://github.com/flozz/rivalcfg",
    license="WTFPL",

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
            "rivalcfg = rivalcfg.__main__:main"
        ]
    },
)

