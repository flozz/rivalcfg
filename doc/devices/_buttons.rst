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

   **¹** The ``ScrollUp`` and ``ScrollDown`` actions are not available on all devices.

   * **Rival 300 / Rival:** OK
   * **Sensei [RAW]:** Not supported


Mapping Mouse Buttons
~~~~~~~~~~~~~~~~~~~~~

Mouse buttons can be mapped to any other mouse button.

For example, this swap the button 1 and 2 of the mouse::

    buttons(button1=button2; button2=button1)


Mapping Multimedia Keys
~~~~~~~~~~~~~~~~~~~~~~~

Mouse buttons can be mapped to multimedia keys. The following keys are available:

* ``Mute``: turn off the sound
* ``Next``: play next media
* ``PlayPause``: toggle play / pause on the currently playing media
* ``Previous``: play the previous media
* ``VolumeUp``: increase the volume
* ``VolumeDown``: decrease the volume

Example::

    buttons(button4=VolumeDown; button5=VolumeUp)


Mapping Keyboard Keys
~~~~~~~~~~~~~~~~~~~~~

Mouse buttons can be mapped to any keyboard keys, using different layouts.

To select the desired layout, just use the ``layout`` parameter. If this
parameter is not specified, the ``QWERTY`` layout will be used by default.

Available layouts:

* ``QWERTY`` (`see available keys <https://github.com/flozz/rivalcfg/blob/master/rivalcfg/handlers/buttons/layout_qwerty.py>`_)

The available keys depends on the selected layout.

Example::

    buttons(layout=QWERTY; button7=PageDown; button8=PageUp)

.. NOTE::

   Some caracters like ``;`` or ``=`` cannot be used as key identifier as they
   interfer with the ``buttons()`` syntax. For those keys, use one of the
   available aliases, like ``semicolon`` (instead of ``;``) or ``equal``
   (instead of ``=``).

   Example::

       buttons(button4=semicolon; button5=equal)
