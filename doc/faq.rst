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
