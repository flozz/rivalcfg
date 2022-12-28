The color setting **is not saved** in the onboard memory on this device. You
can only define if the light goes blank or rainbow at startup.

Supported values are:

* ``off``: All LEDs are off when the mouse wakeup. Clinking on mouse buttons do
  not trigger light reaction.

* ``reactive``: All LEDs are off when the mouse wakeup. Clinking on mouse buttons trigger a light reacion.

* ``rainbow``: LEDs displays an animated raibow effet when the mouse wakeup.
  Clinking on mouse buttons do not trigger light reaction.

* ``reactive-rainbow``: LEDs displays an animated raibow effet when the mouse
  wakeup. Clinking on mouse buttons trigger a light reacion.

Examples::

    rivalcfg --default-lighting off
    rivalcfg --default-lighting reactive-rainbow
