SteelSeries Aerox 9 Wireless
============================


Supported Models
----------------

.. rivalcfg_device_family:: aerox9_wireless_wired
.. rivalcfg_device_family:: aerox9_wireless_wireless


Missing Features
----------------

The following feature are currently not supported by Rivalcfg:

* Smart illumination


Command-Line Usage
------------------

.. rivalcfg_device_cli:: aerox9_wireless_wired


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


Rainbow Effect
--------------

The Aerox 9 offers an onboard rainbow light effect. Please note that the effect
is reset if you change colors.


Default Lighting
----------------

.. include:: ./_default_lighting_reactive.rst


Buttons
-------

.. include:: ./_buttons.rst


Python API
----------

TODO
