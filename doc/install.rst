Installing
==========

From Sources (Git / PyPI)
-------------------------

Prerequisites
~~~~~~~~~~~~~

Linux
^^^^^

Installation require a compilation toolchain and python headers to compile
``hidapi`` (if the *wheel* (binary package) cannot be used).

* On **Debian / Ubuntu**, this can be installed with the following command::

   sudo apt install build-essential python3-dev libusb-1.0-0-dev libudev-dev

* On **Solus**, use the following commands::

   sudo eopkg install -c system.devel
   sudo eopkg install python3 python3-devel libusb-devel

We will also need Python's venv module that is packaged separately on Debian / Ubuntu, so you will have to install it with the following command::

   sudo apt install python3-venv


macOS
^^^^^

On macOS, you will probably need to install XCode to compile ``hidapi`` (if the *wheel* (binary package) cannot be used). This can be done with the following command::

    xcode-select --install

Other requirements may be required, open an issue on GitHub if you are in trouble.


Windows
^^^^^^^

On Windows, you have to install Python first:

* Python >= 3.10 (see https://www.python.org/downloads/windows/)

And Visual C++ build tools are also required to compile ``hidapi`` if the *weel* (binary package) cannot be used:

* Visual C++ 2015 Build Tools: https://www.microsoft.com/en-us/download/details.aspx?id=48159


Installing From PyPI
~~~~~~~~~~~~~~~~~~~~

First create a virtualenv using the following command::

    python3 -m venv ./rivalcfg.venv

This will create a ``rivalcfg.venv`` folder in the current directory. We will then be able to install Rivalcfg in it with the following command:

* On Linux or macOS::

   ./rivalcfg.venv/bin/pip install rivalcfg

* On Windows::

   .\rivalcfg.venv\Scripts\pip install rivalcfg


Installing From GitHub
~~~~~~~~~~~~~~~~~~~~~~

Clone the repository::

   git clone https://github.com/flozz/rivalcfg.git
   cd rivalcfg

Then create a virtualenv using::

    python3 -m venv ./rivalcfg.venv

This will create a ``rivalcfg.venv`` folder in the current directory. Finally, install Rivalcfg in it with the following command:

* On Linux or macOS::

   ./rivalcfg.venv/bin/pip install rivalcfg

* On Windows::

   .\rivalcfg.venv\Scripts\pip install rivalcfg


After the installation (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once Rivalcfg installed from sources (Git or PyPI), you will have to run the
following command on udev-based Linux distro (Debian / Ubuntu / Fedora / ...)::

   sudo ./rivalcfg.venv/bin/rivalcfg --update-udev


Running Rivalcfg from the CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Linux and macOS::

   ./rivalcfg.venv/bin/rivalcfg --help

On Windows::

   .\rivalcfg.venv\Scripts\rivalcfg --help


Running Rivalcfg from a script (Bash)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run Rivlacfg from a shell script, you can import the virtualenv at the start of the script (before calling the ``rivalcfg`` command for the first time).

Example:

.. code-block:: bash

   #!/bin/bash

   # Import the virtualenv
   source /path/to/rivalcfg.venv/bin/activate

   # Call Rivalcfg
   rivalcfg --help


Archlinux AUR Package
---------------------

Use package `rivalcfg <https://aur.archlinux.org/packages/rivalcfg/>`_

.. NOTE::

   I do not maintain this package anymore but other contributor seems to continue to update it. Please check if it is up to date before repporting issues. :)
