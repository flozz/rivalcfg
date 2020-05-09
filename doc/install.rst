Installing
==========


Prerequisites
-------------

.. NOTE::

   The prerequistes are only needed if you install from PYPI or form sources.


Linux
~~~~~

Installation require a compilation toolchain and python headers to
compile ``hidapi``. On Debian / Ubuntu, this can be installed with the
following command (as root)::

   apt install build-essential python-dev libusb-1.0-0-dev libudev-dev


Windows
~~~~~~~

On Windows, you have to install first:

* Python 3.5+ or 2.7 (see https://www.python.org/downloads/windows/)
* Visual C++ 2015 Build Tools: https://www.microsoft.com/en-us/download/details.aspx?id=48159


Installing From PYPI
--------------------

Run the following command (as root)::

   pip install rivalcfg


Installing From sources
-----------------------

Clone the repository::

   git clone https://github.com/flozz/rivalcfg.git
   cd rivalcfg

Install rivalcfg (as root)::

   pip install .


Archlinux AUR package
---------------------

Use package `rivalcfg-git <https://aur.archlinux.org/packages/rivalcfg-git>`_
