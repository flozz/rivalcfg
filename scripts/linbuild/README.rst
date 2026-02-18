Standalone Build For Linux
==========================

Standalone builds are compiled versions of Rivalcfg that can be run without having to install Python and other dependencies. They are built using Nuitka_, a Python compiler.

.. _Nuitka: https://nuitka.net

This document contains instruction to build the standalone build of Rivalcfg for Linux.


Requirements
------------

To build Rivalcfg for Linux, you need:

* A Linux distribution. The older, the better (libc compat).
* A complete Python 3 distribution, with ``venv`` module, and headers.
* Compilation tools (gcc & co).

On Debian and Ubuntu, this can be installed with the following command::

    sudo apt install build-essential python3-dev python3-venv


Compile Rivalcfg for Linux
--------------------------

Run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    ./scripts/linbuild/build-rivalcfg-cli.sh

Result goes to ``"build/rivalcfg.linbuild/rivalcfg-cli.dist/"``.


Build distribuable files
------------------------

To generate the release Tarball, run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    ./scripts/linbuild/release-rivalcfg-cli.sh

Result goes to ``"dist/rivalcfg-cli_v<VERSION>_linux_<ARCH>.tar.gz"``.
