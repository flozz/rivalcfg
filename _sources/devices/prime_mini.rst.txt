SteelSeries Prime Mini
======================


.. NOTE::

   * For Prime Mini Wireless, see :doc:`./prime_wireless`.


Supported Models
----------------

.. rivalcfg_device_family:: prime_mini


Command-Line Usage
------------------

.. rivalcfg_device_cli:: prime_mini


Sensitivity (DPI)
-----------------

This mouse supports up to 5 sensitivity presets. You can define them like this:

::

    rivalcfg --sensitivity 800       # one preset
    rivalcfg --sensitivity 800,1600  # two presets

You can switch preset using the button under the mouse wheel.

.. NOTE::

   When you set the sensitivity through the CLI, the selected preset always
   back to the first one.


.. NOTE:: From Python API, you can pass an ``int``, a ``tuple`` or a ``list``
   as parameter. You are also able to change the currently selected preset::

      mouse.sensitivity(800)
      mouse.sensitivity("800, 1600")
      mouse.sensitivity([800, 1600])
      # select the second preset (1600 dpi)
      mouse.sensitivity([800, 1600, 2000, 4000], selected_preset=2)


Colors
------

This mouse supports colors. Various formats are supported.

.. include:: ./_colors.rst

.. IMPORTANT::

   On newer SteelSeries mice, the color settings are not saved in the onboard
   memory anymore (see Default Lighting bellow).


Default Lighting
----------------

.. include:: ./_default_lighting.rst


Buttons
-------

.. figure:: ./images/prime_buttons.svg
   :alt: Prime buttons schema

.. include:: ./_buttons.rst


Python API
----------

TODO
