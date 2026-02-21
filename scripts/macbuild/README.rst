Standalone Build For macOS
==========================

Standalone builds are compiled versions of Rivalcfg that can be run without having to install Python and other dependencies. They are built using Nuitka_, a Python compiler.

.. _Nuitka: https://nuitka.net

This document contains instruction to build the standalone build of Rivalcfg for macOS.


Requirements
------------

To build Rivalcfg for macOS, you need:

* macOS (tested on Sequoia)

* XCode:

  * Download: https://apps.apple.com/us/app/xcode/id497799835?mt=12
  * CLI Tools only: ``xcode-select --install``

* Python 3, installed from official pkg:

  * Download: https://www.python.org/downloads/


Compile Rivalcfg for macOS
--------------------------

Run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    ./scripts/macbuild/build-rivalcfg-cli.sh

Result goes to ``"build/rivalcfg.macbuild/rivalcfg-cli.dist/"``.


Build distribuable files
------------------------

To generate the release DMG, run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    ./scripts/macbuild/release-rivalcfg-cli.sh

Result goes to ``"dist/rivalcfg-cli_v<VERSION>_macos_<ARCH>.dmg``.
