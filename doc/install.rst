Install Rivalcfg From Sources
=============================

This page contains instructions to install Rivalcfg from sources on different operating systems.

See the documentation from the Rivalcfg website for other installation methods:

* https://rivalcfg.flozz.org/download.html


Linux
-----

Prerequisites
~~~~~~~~~~~~~

Installation requires a complete Python 3 installation that contains the ``venv`` module. You can install it using one of the following commands depending of your distribution::

    # Debian / Ubuntu
    sudo apt install python3-venv

    # Fedora
    # Nothing to install

    # Solus
    # Nothing to install

In some rare cases, you may need additional dependencies to build ``hidapi`` package if now wheel (binary pakage) is available for your system. You can install everything required with following commands::

    # Debian / Ubuntu
    sudo apt install build-essential python3-dev libusb-1.0-0-dev libudev-dev

    # Fedora
    sudo dnf groupinstall "Development Tools"
    sudo dnf install python3-devel libusb1-devel

    # Solus
    sudo eopkg install -c system.devel
    sudo eopkg install python3-devel libusb-devel


Install / Update / Remove
~~~~~~~~~~~~~~~~~~~~~~~~~

First create a virtualenv using the following command::

    python3 -m venv ./rivalcfg.venv

This will create a ``rivalcfg.venv`` folder in the current directory. Then you can install Rivalcfg:

* from PyPI (recommended),
* or from Git repository.


From PyPI (recommended)
^^^^^^^^^^^^^^^^^^^^^^^

To install latest stable version of Rivalcfg from PyPI, use the following command::

    ./rivalcfg.venv/bin/pip install rivalcfg

Later, to update Rivalcfg, you will be able to use the following command::

    ./rivalcfg.venv/bin/pip install --upgrade rivalcfg

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


From Git
^^^^^^^^

To install Rivalcfg from Git, to test the latest development version, use the following command::

    ./rivalcfg.venv/bin/pip install git+https://github.com/flozz/rivalcfg.git#master

.. NOTE::

    * For everyday use, prefer installing stable versions of Rivalcfg from PyPI.
    * The ``git`` utility must be installed on your system (``sudo apt install git`` on Debian / Ubuntu).
    * You can install the version from a specific branch by replacing ``master`` by the branch name at the end of the repository URL.

Later, to update Rivalcfg, you will need to uninstall Rivlacfg first using the command bellow and then reinstall it using the previous command::

    ./rivalcfg.venv/bin/pip uninstall rivalcfg
    ./rivalcfg.venv/bin/pip install git+https://github.com/flozz/rivalcfg.git#master

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


After Installation
~~~~~~~~~~~~~~~~~~

Once Rivalcfg installed from sources (either from PyPI or Git), you will have to run the following command on udev-based Linux distro (Debian / Ubuntu / Fedora / ...)::

   sudo ./rivalcfg.venv/bin/rivalcfg --update-udev

This will install *udev* rules to allow non-privileged users to configure the devices.


Run Rivalcfg
~~~~~~~~~~~~

You can now run Rivalcfg with commands like::

   ./rivalcfg.venv/bin/rivalcfg --help


macOS
-----

Prerequisites
~~~~~~~~~~~~~

On macOS, **you may not need any requirement**. But in some cases you may need a compiler to build the ``hidapi`` package if now wheel (binary pakage) is available for your system and Python version.

You should be able to install XCode with the following command::

    xcode-select --install

Other requirements may be needed, open an issue on GitHub if you are in trouble.


Install / Update / Remove
~~~~~~~~~~~~~~~~~~~~~~~~~

First create a virtualenv using the following command::

    python3 -m venv ./rivalcfg.venv

This will create a ``rivalcfg.venv`` folder in the current directory. Then you can install Rivalcfg:

* from PyPI (recommended),
* or from Git repository.


From PyPI (recommended)
^^^^^^^^^^^^^^^^^^^^^^^

To install latest stable version of Rivalcfg from PyPI, use the following command::

    ./rivalcfg.venv/bin/pip install rivalcfg

Later, to update Rivalcfg, you will be able to use the following command::

    ./rivalcfg.venv/bin/pip install --upgrade rivalcfg

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


From Git
^^^^^^^^

To install Rivalcfg from Git, to test the latest development version, use the following command::

    ./rivalcfg.venv/bin/pip install git+https://github.com/flozz/rivalcfg.git#master

.. NOTE::

    * For everyday use, prefer installing stable versions of Rivalcfg from PyPI.
    * The ``git`` utility must be installed on your system.
    * You can install the version from a specific branch by replacing ``master`` by the branch name at the end of the repository URL.

Later, to update Rivalcfg, you will need to uninstall Rivlacfg first using the command bellow and then reinstall it using the previous command::

    ./rivalcfg.venv/bin/pip uninstall rivalcfg
    ./rivalcfg.venv/bin/pip install git+https://github.com/flozz/rivalcfg.git#master

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


Run Rivalcfg
~~~~~~~~~~~~

You can now run Rivalcfg with commands like::

   ./rivalcfg.venv/bin/rivalcfg --help


Windows
-------

Prerequisites
~~~~~~~~~~~~~

On Windows, you have to install Python first:

* Download Python >= 3.10 from https://www.python.org/downloads/windows/
* **IMPORTANT:** During the installation process, check the "Add Python X.Y to PATH" checkbox.
* Finally reboot your computer to complete the installation.

It should be enough to install and run Rivalcfg, but in some cases you may need to install additional tools to build the ``hidapi`` package if not wheel (binary package) is available for your system:

* Visual C++ 2015 Build Tools: https://www.microsoft.com/en-us/download/details.aspx?id=48159


Install / Update / Remove
~~~~~~~~~~~~~~~~~~~~~~~~~

First open a terminal (either CMD.exe or PowerShell).

Then create a virtualenv using the following command::

    python -m venv .\rivalcfg.venv

This will create a ``rivalcfg.venv`` folder in the current directory. Then you can install Rivalcfg:

* from PyPI (recommended),
* or from Git repository.


From PyPI (recommended)
^^^^^^^^^^^^^^^^^^^^^^^

To install latest stable version of Rivalcfg from PyPI, use the following command::

    .\rivalcfg.venv\Scripts\pip install rivalcfg

Later, to update Rivalcfg, you will be able to use the following command::

    .\rivalcfg.venv\Scripts\pip install --upgrade rivalcfg

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


From Git
^^^^^^^^

To install Rivalcfg from Git, to test the latest development version, use the following command::

    .\rivalcfg.venv\Scripts\pip install git+https://github.com/flozz/rivalcfg.git#master

.. NOTE::

    * For everyday use, prefer installing stable versions of Rivalcfg from PyPI.
    * The ``git`` utility must be installed on your system and available in the ``PATH``.
    * You can install the version from a specific branch by replacing ``master`` by the branch name at the end of the repository URL.

Later, to update Rivalcfg, you will need to uninstall Rivlacfg first using the command bellow and then reinstall it using the previous command::

    .\rivalcfg.venv\Scripts\pip uninstall rivalcfg
    .\rivalcfg.venv\Scripts\pip install git+https://github.com/flozz/rivalcfg.git#master

To remove Rivalcfg from your computer, simply delete the ``rivalcfg.venv`` folder.


Run Rivalcfg
~~~~~~~~~~~~

You can now run Rivalcfg with commands like::

   .\rivalcfg.venv\Scripts\rivalcfg --help

