The color setting **is not saved** in the onboard memory on this device. You
can only define if the light goes blank or rainbow at startup.

Supported values are:

* ``off``: All LEDs are off when the mouse wakes up. Clicking on mouse buttons will
  not trigger light reaction.

* ``reactive``: All LEDs are off when the mouse wakes up. Clicking on mouse buttons will trigger a light reaction.

* ``rainbow``: LEDs display an animated rainbow effect when the mouse wakes up.
  Clicking on mouse buttons will not trigger a light reaction.

* ``reactive-rainbow``: LEDs display an animated rainbow effect when the mouse
  wakes up. Clicking on mouse buttons will trigger a light reacion.

Examples::

    rivalcfg --default-lighting off
    rivalcfg --default-lighting reactive-rainbow
