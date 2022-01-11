SteelSeries Rival 3 Wireless
============================


Supported Models
----------------

.. rivalcfg_device_family:: rival3_wireless


Missing Features
----------------

The following feature are currently not supported by Rivalcfg:

* Color / illumination
* Wheel mapping
* Powering settings (high efficiency, smart illumination, sleep timer)


Command-Line Usage
------------------

.. rivalcfg_device_cli:: rival3_wireless


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


Buttons
-------

.. figure:: ./images/rival_3_wireless_buttons.svg
   :alt: Rival 3 Wireless buttons schema

.. include:: ./_buttons.rst


Python API
----------

TODO
