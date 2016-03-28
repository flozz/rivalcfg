#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="rivalcfg",
    version="1.0.0",
    description="Configure the SteelSeries Rival 100 gaming mouse",
    url="https://github.com/flozz/rivalcfg",
    license="WTFPL",

    author="Fabien LOISON",
    author_email="http://www.flozz.fr/",

    keywords="steelseries rival rival100 mouse",
    platforms=["Linux"],

    packages=find_packages(),

    install_requires=[
        "pyudev>=0.19.0"
    ]
)

