SteelSeries Rival Pro
=====================


Supported Models
----------------

.. rivalcfg_device_family:: rival_pro

.. NOTE::

   The Rival Pro is a wireless-only mouse. rivalcfg talks to it through its
   UWB receiver / base station (``1038:1880``).

.. IMPORTANT::

   Tested with firmware v2.14.2. SteelSeries GG requires a firmware update
   before it lets you change any setting, so older firmware versions may
   behave differently.


Command-Line Usage
------------------

.. rivalcfg_device_cli:: rival_pro


Sensitivity (DPI)
-----------------

This mouse supports up to 5 sensitivity presets. You can set different DPIs on
X and Y axis. You can define them like this:

::

    rivalcfg --sensitivity 800       # 1 preset (x=800dpi:y=800dpi)
    rivalcfg --sensitivity 800,1600  # 2 presets
    rivalcfg --sensitivity 800:1000,1600:1800  # 2 presets ;
    #                      ↑x1 ↑y1  ↑x2  ↑y2   # x1=800dpi  : y1=1000dpi,
                                               # x2=1600dpi : y2=1800dpi

Values from 1 to 65000 DPI are accepted, like in SteelSeries GG. The native
maximum of the sensor is 42000 DPI.

You can switch preset using the button under the mouse (Button6).

.. NOTE::

   When you set the sensitivity through the CLI, the selected preset always
   back to the first one.

.. NOTE::

   The lift-off and landing distances, configurable per preset in
   SteelSeries GG, are always set to 1.0 mm (the factory default).


Polling Rate
------------

The Rival Pro can store up to 5 polling rate "levels", each one with its own
sensor report rate and UWB polling rate. rivalcfg configures a single level,
with the same sensor report rate and UWB polling rate::

    rivalcfg --polling-rate 8000


Power Management
----------------

Sleep timer (from 1 to 20 minutes)::

    rivalcfg --sleep-timer 10

Polling rate used in low power mode (when the battery level drops to 5 %), or
``led-only`` to only show a warning on the LED::

    rivalcfg --low-power-polling-rate 500
    rivalcfg --low-power-polling-rate led-only

Battery level of the battery currently in the mouse::

    rivalcfg --battery-level


Performance and Tracking
------------------------

Click response (debounce time, from 0 to 20 ms)::

    rivalcfg --click-response 8

Scroll jump protection (ignores the first scroll input after a cooldown
period, from 100 to 1500 ms)::

    rivalcfg --scroll-jump-protection 500
    rivalcfg --scroll-jump-protection off

Motion sync, LAN mode (for when multiple UWB mice are nearby, must be enabled
on all mice) and max performance mode::

    rivalcfg --motion-sync on
    rivalcfg --lan-mode on
    rivalcfg --max-performance on

.. NOTE::

   The "Tracking Tools" settings of SteelSeries GG (rotation, angle snapping
   and acceleration / deceleration) are not supported yet.


LED Indicator
-------------

Select what the LED of the receiver / base station indicates::

    rivalcfg --led-indicator polling-rate  # Polling x sensor report rate (default)
    rivalcfg --led-indicator battery       # Mouse battery level
    rivalcfg --led-indicator off


Buttons
-------

==============  ===================  ==============
Button          Location             Default
==============  ===================  ==============
``button1``     Left button          ``button1``
``button2``     Right button         ``button2``
``button3``     Wheel click          ``button3``
``button4``     Side button (back)   ``button4``
``button5``     Side button (front)  ``button5``
``button6``     Under the mouse      ``dpi``
``scrollup``    Wheel up             ``scrollup``
``scrolldown``  Wheel down           ``scrolldown``
==============  ===================  ==============

.. include:: ./_buttons.rst


Python API
----------

TODO
