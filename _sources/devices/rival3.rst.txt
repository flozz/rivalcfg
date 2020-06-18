SteelSeries Rival 3
===================


Supported Models
----------------

.. rivalcfg_device_family:: rival3


Command-Line Usage
------------------

.. rivalcfg_device_cli:: rival3


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

This mouse supports 4 color zone.

You can pass 1 color if you want all zones to be set to the same color::

    "<COLOR>"

Or 4 colors if you want to set a different color for each zone::

    "<COLOR_TOP>, <COLOR_MIDDLE>, <COLOR_BOTTOM>, <COLOR_LOGO>"

Examples:

* |clr-ss-orange| ``"#ff1800"``
* |clr-red| |clr-aqua| |clr-blue| |clr-purple| ``"#ff0000, #00ffff, #0000ff, purple"``

.. |clr-ss-orange| raw:: html

   <span class="color-preview" style="background: #ff4400;"></span>

.. include:: ./_colors.rst

If you pass only one ``tuple``, all zones will be set to the same color. You
can also provide 4 colors, one for each zone:

::

    [
        (255, 0, 0),    # Zone 1 (top)
        (0, 255, 255),  # Zone 2 (middle)
        (0, 0, 255),    # Zone 3 (bottom)
        (128, 0, 128),  # Logo
    ]


Mixes with color strings are also allowed:

::


    [
        (255, 0, 0),    # Zone 1 (top)
        "#00FFFF",      # Zone 2 (middle)
        "0ff",          # Zone 3 (bottom)
        "purple",       # Logo
    ]


Python API
----------

TODO
