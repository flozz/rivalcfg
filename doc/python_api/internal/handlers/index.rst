handlers
========

There is a different handler for each ``value_type`` that can be used in
a device profile. Each handler module provides at least two functions:

* ``process_value``: transforms an input value into bytes that can be sent to
  a device,
* ``add_cli_option``: generate a CLI option for a setting of the device, with
  all required validation.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   ./none.rst
   ./choice.rst
   ./range.rst
   ./multidpi_range.rst
   ./rgbcolor.rst
   ./reactive_rgbcolor.rst
   ./rgbgradient.rst
   ./rgbgradientv2.rst
   ./buttons.rst
