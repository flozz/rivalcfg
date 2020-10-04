#!/usr/bin/env python
# encoding: UTF-8

import os
from setuptools import setup, find_packages

long_description = ""

try:
    if os.path.isfile("README.rst"):
        long_description = open("README.rst", "r").read()
except Exception as error:
    print("Unable to read the README file: " + str(error))


setup(
    name="rivalcfg",
    version="4.1.0",
    description="Configure SteelSeries gaming mice",
    url="https://github.com/flozz/rivalcfg",
    license="WTFPL",

    long_description=long_description,

    author="Fabien LOISON",

    keywords="steelseries rival sensei mouse",
    platforms=["Linux", "Windows"],

    packages=find_packages(),

    install_requires=[
        "hidapi>=0.7.99.post20"
    ],

    extras_require={
        "dev": [
            "flake8",
            "pytest",
            "Sphinx",
            "sphinx-rtd-theme",
            "nox",
        ],
    },

    entry_points={
        "console_scripts": [
            "rivalcfg = rivalcfg.__main__:main"
        ]
    },

    # cmdclass={"install": install}
)
