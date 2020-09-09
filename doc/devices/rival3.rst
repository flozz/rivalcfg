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

This mouse supports colors. Various formats are supported.

.. include:: ./_colors.rst


Light Effect
------------

The Rival 3 offers some onboard light effects.

Please note that the effects are reset if you changes colors. So if you want
specific colors with the breath effect, you have to set colors first and the
effect after::

    rivalcfg --z1 red --z2 lime --z3 blue --logo-color purple
    rivalcfg --light-effect breath


Buttons
-------

.. figure:: ./images/rival_3_buttons.svg
   :alt: Rival 3 buttons schema

.. include:: ./_buttons.rst


Python API
----------

TODO
