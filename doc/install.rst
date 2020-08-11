Installing
==========


.. IMPORTANT::

   In this page, only Python 3 commands are provided. Rivalcfg still work with
   Python 2, but this support will be dropped in future versions... so prefer
   using Python 3 if available.


Prerequisites
-------------

.. NOTE::

   The prerequistes are only needed if you install from PyPI or form sources.


Linux
~~~~~

Installation require a compilation toolchain and python headers to compile
``hidapi``.

On **Debian / Ubuntu**, this can be installed with the following command::

   sudo apt install build-essential python3-pip python3-dev libusb-1.0-0-dev libudev-dev

On **Solus**, use the following commands::

   sudo eopkg install -c system.devel
   sudo eopkg install python3 python3-devel libusb-devel


Windows
~~~~~~~

On Windows, you have to install first:

* Python 3.6+ (see https://www.python.org/downloads/windows/)
* Visual C++ 2015 Build Tools: https://www.microsoft.com/en-us/download/details.aspx?id=48159


Installing From PyPI
--------------------

Run the following command::

   sudo pip3 install rivalcfg


Installing From sources
-----------------------

Clone the repository::

   git clone https://github.com/flozz/rivalcfg.git
   cd rivalcfg

Install rivalcfg::

   sudo pip3 install .


Archlinux AUR package
---------------------

Use package `rivalcfg-git <https://aur.archlinux.org/packages/rivalcfg-git>`_
