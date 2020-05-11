"""
The "rgbcolor" type handles RGB color values.

It supports hexadecimal colors:

* ``#FF0000``
* ``FF0000``
* ``#F00``
* ``F00``

RGB tuples or list (only from Python API for this one):

* ``(255, 0, 0)``
* ``[255, 0, 0]``

and named colors:

* ``white``
* ``silver``
* ``gray``
* ``black``
* ``red``
* ``maroon``
* ``yellow``
* ``olive``
* ``lime``
* ``green``
* ``aqua``
* ``teal``
* ``blue``
* ``navy``
* ``fuchsia``
* ``purple``


Device Profile
--------------

Example of a rgbcolor value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "color": {
                "label": "LED color",
                "description": "Set the mouse backlight color",
                "cli": ["-c", "--color"],
                "command": [0x05, 0x00],
                "value_type": "rgbcolor",
                "default": "#FF1800"
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    -c COLOR, --color=COLOR
                        Set the mouse backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)

Example of CLI usage::

    rivalcfg --color=red
    rivalcfg --color=ff0000
    rivalcfg --color=f00


Functions
---------
"""


from ..color_helpers import is_color, parse_color_string


def process_value(setting_info, color):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list color: The color.
    :rtype: [int, int, int]
    """
    # Color tuple
    if type(color) in (tuple, list):
        if len(color) != 3:
            raise ValueError("Not a valid color %s" % str(color))
        for channel in color:
            if type(channel) != int or channel < 0 or channel > 255:
                raise ValueError("Not a valid color %s" % str(color))
            return list(color)

    if is_color(color):
        return list(parse_color_string(color))

    raise ValueError("Not a valid color %s" % str(color))


def add_cli_option(cli, setting_name, setting_info):
    """Add the given "rgbcolor" type setting to the given CLI arguments parser.

    :param ArgumentParser cli: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    pass
