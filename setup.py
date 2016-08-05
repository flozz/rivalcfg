#!/usr/bin/env python
# encoding: UTF-8

import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from rivalcfg import VERSION


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

    * SteelSeries Rival
    * SteelSeries Rival 100
    * SteelSeries Rival 300

    If you have trouble running this software, please open an issue on Github:

    * https://github.com/flozz/rivalcfg/issues


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

    entry_points={
        "console_scripts": [
            "rivalcfg = rivalcfg.cli:main"
        ]
    },

    package_data={
        "rivalcfg": ["data/*"]
    },

    cmdclass={"install": install}
)

