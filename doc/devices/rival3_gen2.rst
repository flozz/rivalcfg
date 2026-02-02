SteelSeries Rival 3 Gen 2
=========================


Supported Models
----------------

.. rivalcfg_device_family:: rival3_gen2


Command-Line Usage
------------------

.. rivalcfg_device_cli:: rival3_gen2


Sensitivity (DPI)
-----------------

This mouse supports up to 5 sensitivity presets. You can set different DPIs on X and Y axis. You can define them like this:

::

    rivalcfg --sensitivity 800       # 1 preset (x=800dpi:y=800dpi)
    rivalcfg --sensitivity 800,1600  # 2 presets
    rivalcfg --sensitivity 800:1000,1600:1800  # 2 presets ;
    #                      ↑x1 ↑y1  ↑x2  ↑y2   # x1=800dpi  : y1=1000dpi,
                                               # x2=1600dpi : y2=1800dpi

You can switch preset using the button under the mouse wheel.

.. NOTE::

   When you set the sensitivity through the CLI, the selected preset always
   back to the first one.


.. NOTE:: From Python API, you can pass an ``int``, a ``tuple`` or a ``list``
   as parameter. You are also able to change the currently selected preset::

      mouse.sensitivity(800)
      mouse.sensitivity("800, 1600")
      mouse.sensitivity([800, 1600])
      mouse.sensitivity([
          [800, 1000],   # preset1 -> x1=800dpi,  y1=1000dpi
          [1600, 1800],  # preset2 -> x2=1600dpi, y2=1800dpi
      ])
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

.. include:: ./_default_lighting_reactive.rst


Rainbow Effect
--------------

The Aerox 3 offers an onboard rainbow light effect. Please note that the effect
is reset if you change colors.


Buttons
-------

.. figure:: ./images/rival3_gen2_buttons.svg
   :alt: Aerox 3 buttons schema

.. include:: ./_buttons.rst


Python API
----------

TODO
