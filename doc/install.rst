Installing
==========

Archlinux AUR Package
---------------------

Use package `rivalcfg <https://aur.archlinux.org/packages/rivalcfg/>`_


From Sources (Git / PyPI)
-------------------------

Prerequisites
~~~~~~~~~~~~~

.. IMPORTANT::

   In this page, only Python 3 commands are provided. Rivalcfg still work with
   Python 2, but this support will be dropped in future versions... so prefer
   using Python 3 if available.


Linux
^^^^^

Installation require a compilation toolchain and python headers to compile
``hidapi``.

On **Debian / Ubuntu**, this can be installed with the following command::

   sudo apt install build-essential python3-pip python3-dev python3-setuptools libusb-1.0-0-dev libudev-dev

On **Solus**, use the following commands::

   sudo eopkg install -c system.devel
   sudo eopkg install python3 python3-devel libusb-devel


Windows
^^^^^^^

On Windows, you have to install first:

* Python 3.6+ (see https://www.python.org/downloads/windows/)
* Visual C++ 2015 Build Tools: https://www.microsoft.com/en-us/download/details.aspx?id=48159


Installing From PyPI
~~~~~~~~~~~~~~~~~~~~

Run the following command::

   sudo pip3 install rivalcfg


Installing From Github
~~~~~~~~~~~~~~~~~~~~~~

Clone the repository::

   git clone https://github.com/flozz/rivalcfg.git
   cd rivalcfg

Install rivalcfg::

   sudo pip3 install .


After the installation
~~~~~~~~~~~~~~~~~~~~~~

Once Rivalcfg installed from sources (Git or PyPI), you will have to run the
following command on udev-based Linux distro (Debian / Ubuntu / Fedora / ...)::

    sudo rivalcfg --update-udev
