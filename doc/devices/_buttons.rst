This mouse supports buttons mapping. Buttons can be mapped with:

* some special actions,
* mouse buttons,
* multimedia keys,
* and keyboard keys.

The general syntax for buttons mapping is the following::

    buttons(layout=<LAYOUT>; button1=<mapping1>; buttonN=<mappingN>)

Example::

    rivalcfg --buttons "buttons(layout=QWERTY; button1=button1; button2=PlayPause; button3=disabled; button5=A; button6=DPI)"

Arguments:

* ``layout``: The keyboard layout to use when papping the keys (see the "Mapping Keyboard Keys" section bellow).
* ``button1``: The first button of the mouse.
* ``button2``: The second button of the mouse.
* ``buttonN``: The Nth button of the mouse (The number of available buttons depends of the mouse model).

.. NOTE::

   All parameters are optional. If you do not define a mapping for a specific button, it will be reset to its default value.

You can also reset all buttons to their factory default by passing ``"default"`` as parameter::

    rivalcfg --buttons default

.. WARNING::

    Be sure to map the mouse button ``button1`` on some button, else you will not be able to click with the mouse!


Mapping Special Actions
~~~~~~~~~~~~~~~~~~~~~~~

The following special actions are available¹:

* ``disabled``: disable the button,
* ``dpi``: use this button to switch between DPI presets,
* ``ScrollUp``: simulate a scroll up (not available on all devices¹)
* ``ScrollDown``: simulate a scroll down (not available on all devices¹)

Example::

    buttons(button4=disabled; button5=disabled; button6=DPI)

.. NOTE::

   **¹** The ``SrollUp`` and ``ScrollDown`` actions are not available on all devices.

   * **Rival 300 / Rival:** OK
   * **Sensei [RAW]:** Not supported


Mapping Mouse Buttons
~~~~~~~~~~~~~~~~~~~~~

TODO


Mapping Multimedia Keys
~~~~~~~~~~~~~~~~~~~~~~~

TODO


Mapping Keyboard Keys
~~~~~~~~~~~~~~~~~~~~~

TODO
