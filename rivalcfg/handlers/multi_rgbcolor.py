"""
The "multi_rgbcolor" type handles multiple RGB color values in one command.

::

    <COLOR>

::

    <COLOR1>, <COLOR2>, ..., <COLOR N>

It supports hexadecimal colors:

* ``#FF0000``
* ``FF0000``
* ``#F00``
* ``F00``

RGB tuples or list (only from Python API for this one):

* ``(255, 0, 0)``
* ``[255, 0, 0]``
* ``[[255, 0, 0], [0, 255, 0], ...]``
* ``[(255, 0, 0), "lime", "#0000ff", ...]``

and named colors:

+------------+------------+-----------+-------------+
| ``white``  | ``red``    | ``lime``  | ``blue``    |
+------------+------------+-----------+-------------+
| ``silver`` | ``maroon`` | ``green`` | ``navy``    |
+------------+------------+-----------+-------------+
| ``gray``   | ``yellow`` | ``aqua``  | ``fuchsia`` |
+------------+------------+-----------+-------------+
| ``black``  | ``olive``  | ``teal``  | ``purple``  |
+------------+------------+-----------+-------------+


Device Profile
--------------

Example of a rgbcolor value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "color": {
                "label": "LED colors",
                "description": "Set the color of the mouse LEDs",
                "cli": ["-c", "--color"],
                "command": [[0x0A, 0x00, 0x0F],
                "value_type": "multi_rgbcolor",
                "color_count": 4,
                "default": "#FF1800"
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -c COLORS, --colors COLORS
                        Set the color of the mouse LEDs (format: '<COLOR>' or
                        '<COLOR_TOP>,<COLOR_MIDDLE>,<COLOR_BOTTOM>,<COLOR_LOGO>') (default:
                        #FF1800)

Example of CLI usage::

    rivalcfg --color=red
    rivalcfg --color=ff0000
    rivalcfg --color=red,aqua,blue,purple


Functions
---------
"""  # noqa


import argparse

from ..helpers import merge_bytes
from ..color_helpers import is_color, parse_color_string


def process_value(setting_info, value):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "multi_rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list value: The color.
    :rtype: [int]
    """
    colors = []

    # List / Tuple
    if type(value) in (tuple, list):
        if len(value) == 3 \
                and type(value[0]) is int \
                and type(value[1]) is int \
                and type(value[2]) is int:
            colors = [value]
        elif len(value) in (1, setting_info["color_count"]):
            colors = value
    # Str
    else:
        colors = value.replace(" ", "").split(",")

    # 1 colors -> duplicate it to have the right color count

    if len(colors) == 1:
        colors = colors * setting_info["color_count"]

    # Check color count

    if len(colors) != setting_info["color_count"]:
        raise ValueError("%i colors provided but the mouse requires %i" % (
            len(colors),
            setting_info["color_count"]))

    # Handle colors

    packet = []

    for color in colors:
        if type(color) in (tuple, list):
            if len(color) != 3:
                raise ValueError("Not a valid color %s" % str(color))
            for channel in color:
                if type(channel) != int or channel < 0 or channel > 255:
                    raise ValueError("Not a valid color %s" % str(color))
            packet = merge_bytes(packet, color)

        elif is_color(color):
            packet = merge_bytes(packet, parse_color_string(color))

        else:
            raise ValueError("Not a valid color %s" % str(color))

    return packet


def cli_colors_validator(color_count):
    class CheckColorsAction(argparse.Action):
        """Validate colors from CLI"""

        def __call__(self, parser, namespace, value, option_string=None):
            colors = value.replace(" ", "").split(",")
            if len(colors) not in (1, color_count):
                raise argparse.ArgumentError(self, "you provided %i colors but the the mouse requires %i" %  (  # noqa
                    len(colors),
                    color_count,
                    ))
            for color in colors:
                if not is_color(color):
                    raise argparse.ArgumentError(self, "invalid color: '%s'" %  color)  # noqa
            setattr(namespace, self.dest.upper(), value)

    return CheckColorsAction


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "multi_rgbcolor" type setting to the given CLI arguments
    parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (default: %s)" % (
            setting_info["description"],
            str(setting_info["default"])
            )
    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            action=cli_colors_validator(setting_info["color_count"]),
            metavar=setting_name.upper()
            )
