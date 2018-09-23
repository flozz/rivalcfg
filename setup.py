#!/usr/bin/env python
# encoding: UTF-8

import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


class install(_install):
    def run(self):
        _install.run(self)
        print("Installing udev rules...")
        if not os.path.isdir("/etc/udev/rules.d"):
            print("WARNING: udev rules have not been installed (/etc/udev/rules.d is not a directory)")
            return
        try:
            shutil.copy("./rivalcfg/data/99-steelseries-rival.rules", "/etc/udev/rules.d/")
        except IOError:
            print("WARNING: udev rules have not been installed (permission denied)")
            return
        try:
            subprocess.call(["udevadm", "trigger"])
        except OSError:
            print("WARNING: unable to update udev rules, please run the 'udevadm trigger' command")
            return
        print("Done!")


long_description = ""

try:
    if os.path.isfile("README.rst"):
        long_description = open("README.rst", "r").read()
    elif os.path.isfile("README.md"):
        long_description = open("README.md", "r").read()
except Exception as error:
    print("Unable to read the README file: " + str(error))


setup(
    name="rivalcfg",
    version="3.1.0",
    description="Configure SteelSeries Rival gaming mice",
    url="https://github.com/flozz/rivalcfg",
    license="WTFPL",

    long_description=long_description,

    author="Fabien LOISON",

    keywords="steelseries rival rival100 mouse",
    platforms=["Linux"],

    packages=find_packages(),

    install_requires=[
        "hidapi>=0.7.99.post20"
    ],

    entry_points={
        "console_scripts": [
            "rivalcfg = rivalcfg.__main__:main"
        ]
    },

    cmdclass={"install": install}
)
