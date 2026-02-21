Standalone Build For Windows
============================

Standalone builds are compiled versions of Rivalcfg that can be run without having to install Python and other dependencies. They are built using Nuitka_, a Python compiler.

.. _Nuitka: https://nuitka.net

This document contains instruction to build the standalone build of Rivalcfg for Windows.


Requirements
------------

To build Rivalcfg for windows, you need:

* Windows 11:

  * Download (VM): https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/

* Install Chocolatey (optional, but simpler setup):

  * Run in PowerShell as administrator:
    ``Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))``
  * NOTE: all ``choco`` commands should be run as administrator

* Python 3:

  * 64bit version
  * Must be added to the PATH (there is a checkbox during the installation)
  * Download: https://www.python.org/
  * Choco: ``choco install python``

* Visual Studio 17 (2022)

  * Already installed in the Windows 11 Dev VM, else use Chocolatey
  * Choco: ``choco install visualstudio2022-workload-vctools``

Restart to finish setup.


Compile Rivalcfg for Windows
----------------------------

Run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    .\scripts\winbuild\build-rivalcfg-cli.bat

Result goes to ``"build\rivalcfg.winbuild\rivalcfg-cli.dist\"``.


Build distribuable files
------------------------

To generate the release Zip, run the following command from project's root dir (the one with the ``"pyproject.toml"`` file)::

    .\scripts\winbuild\release-rivalcfg-cli.bat

Result goes to ``"dist\rivalcfg-cli_v<VERSION>_windows_<ARCH>.zip"``.
