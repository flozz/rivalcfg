Frequently Asked Questions
==========================


How can I turn the lights off?
------------------------------

On devices that supports RGB colors, you can turn the lights off by setting the
black color to the LED.

Example with Rival 100::

   rivalcfg --color=black

Example with Rival 300::

   rivalcfg --logo-color=black --wheel-color=black

On devices that have monochrome LEDs, you can turn the lights off using the
LED brightness option.

Example with the Sensei [RAW]::

    rivalcfg --led-brightness=off

Example with the Kana v2::

    rivalcfg --led-brightness1=off --led-brightness2=off

Look at :ref:`the page dedicated to your device <devices>` for more about
available CLI options.


How can I dim the brightness of the lights
------------------------------------------

On devices that supports RGB colors, just set a darker color (e.g. ``#880000``
instead of ``#FF0000`` for a darker red).

Example with Rival 100::

   rivalcfg --color=880000

On devices that have monochrome LEDs, use the LED brightness option.

Example with the Sensei [RAW]::

    rivalcfg --led-brightness=low

Look at :ref:`the page dedicated to your device <devices>` for more about
available CLI options.


Why Rivalcfg does not support color gradients / color shift / rainbow lighting effect on my mouse whereas the SteelSeries Engine does?
--------------------------------------------------------------------------------------------------------------------------------------

Rivalcfg only supports hardware features of the devices, so there is two
possibilities:

* Your device do not support this feature by hardware, so the SteelSeries
  Engine sends color command to the mouse several times per second. As Rivalcfg
  is only a library and a CLI tool, not a deamon, it cannot support this
  feature. But you can implement it yourself with a Bash script or using the
  Python API.

* Your device has an hardware support of this feature, but this functionnality
  is not supported yet by Rivalcfg. In that case, please consider
  :ref:`contributing <contributing>` to this project! 😁️

Here is an **non-exhausting** list of devices that do not support color
gradients:

* Rival 3
* Rival 100
* Rival 110
* Rival 300
