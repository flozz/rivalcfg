"""
The "rgbgradient" type handles RGB color gradients. Simple RGB color can also
be used.

RGB gradient syntax example::

    rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)
    rgbgradient(colors=0%: red, 33%: lime, 66%: blue)

It supports both hexadecimal colors:

* ``#FF0000``
* ``FF0000``
* ``#F00``
* ``F00``

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

----

Simple colors can also be used if you want a static color like for the
:doc:`rgbcolor` handler.


Device Profile
--------------

Example of a rgbgradient value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "color": {
                "label": "Logo LED colors and effects",
                "description": "Set the colors and the effects of the logo LED",
                "cli": ["-c", "--logo-color"],
                "command": [0x5B, 0x00, 0x00],
                "value_type": "rgbgradient",
                # TODO
                "default": "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    TODO

Example of CLI usage::

    TODO


Functions
---------
"""  # noqa


import argparse

from ..helpers import uint_to_little_endian_bytearray, merge_bytes
from ..color_helpers import is_color, parse_color_string


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    header_length = setting_info["rgbgradient_header"]["header_length"]
    duration_offset = setting_info["rgbgradient_header"]["duration_offset"]
    duration_length = setting_info["rgbgradient_header"]["duration_length"]
    repeat_offset = setting_info["rgbgradient_header"]["repeat_offset"]
    triggers_offset = setting_info["rgbgradient_header"]["triggers_offset"]
    color_count_offset = setting_info["rgbgradient_header"]["color_count_offset"]  # noqa

    is_gradient = False
    duration = 1000
    repeat = 0x00
    triggers = 0x00
    gradient = []

    # Color tuple
    if type(colors) in (tuple, list):
        if len(colors) != 3:
            raise ValueError("Not a valid color %s" % str(colors))
        for channel in colors:
            if type(channel) != int or channel < 0 or channel > 255:
                raise ValueError("Not a valid color %s" % str(colors))
        is_gradient = False
        gradient.append({
            "pos": 0,
            "color": colors,
        })

    # Simple color string
    elif is_color(colors):
        is_gradient = False
        gradient.append({
            "pos": 0,
            "color": parse_color_string(colors),
        })

    # Color gradient as dict
    elif type(colors) is dict:
        is_gradient = True
        pass  # TODO

    # Color gradient as string
    else:
        is_gradient = True
        pass  # TODO

    # --

    if not is_gradient or triggers != 0x00:
        repeat = 0x01

    # -- Check

    if len(gradient) == 0:
        raise ValueError("no color: %s" % str(colors))

    # TODO len(gradient) <= 14

    # -- Generate header

    header = [0x00] * header_length
    header[repeat_offset] = repeat
    header[triggers_offset] = triggers
    header[color_count_offset] = len(gradient)

    offset = 0
    for b in uint_to_little_endian_bytearray(duration, duration_length):
        header[duration_offset + offset] = b
        offset += 1

    # -- Generate body

    body = list(gradient[0]["color"])

    for pos, color in [(item["pos"], item["color"]) for item in gradient]:
        body = merge_bytes(body, color, pos)

    # --

    return merge_bytes(header, body)


class CheckGradientAction(argparse.Action):
    """Validate colors gradient from CLI"""

    def __call__(self, parser, namespace, value, option_string=None):
        # TODO
        if not is_color(value):
            raise argparse.ArgumentError(self, "invalid color: '%s'" %  value)  # noqa
        setattr(namespace, self.dest.upper(), value)


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "rgbgradient" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (default: %s)" % (  # FIXME more help
            setting_info["description"],
            str(setting_info["default"])
            )
    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            action=CheckGradientAction,
            metavar=setting_name.upper()
            )
