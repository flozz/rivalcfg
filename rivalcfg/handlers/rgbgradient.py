"""
The "rgbgradientv2" type handles RGB color gradients. Simple RGB color can also
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

A Python ``dict`` can also be used (Python API only)::

    {
        "duration": 1000,  # ms
        "colors": [
            {"pos": 0, "color": "red"},
            {"pos": 33, "color": "#00FF00"},
            {"pos": 66, "color": (0, 0, 255)},
        ]
    }

.. NOTE::

   A maximum of 14 color stops can be defined in a gradient.


Device Profile
--------------

Example of a rgbgradient value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "logo_color": {
                "label": "Logo LED colors and effects",
                "description": "Set the colors and the effects of the logo LED",
                "cli": ["-c", "--logo-color"],
                "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
                "command": [0x05, 0x00],
                "value_type": "rgbgradient",
                "rgbgradient_header": {
                    "header_length": 28,       # Length of the header excuding command / LED ID
                    "led_id_offsets": [0, 5],  # Offset of the "led_id" fields
                    "duration_offset": 6,      # Offset of the "duration" field
                    "duration_length": 2,      # Length of the "duration" field (in Bytes)
                    "repeat_offset": 22,       # Offset of the "repeat" flag
                    "triggers_offset": 23,     # Offset of the "triggers" field (buttons mask)
                    "color_count_offset": 27,  # Offset of the "color_count" field
                },
                "led_id": 0x01,
                "default": "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -c LOGO_COLOR, --logo-color LOGO_COLOR
                         Set the colors and the effects of the logo LED (default:
                         rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff))

Example of CLI usage::

    rivalcfg --logo-color="rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
    rivalcfg --logo-color=red
    rivalcfg --logo-color=FF1800


Functions
---------
"""


import argparse

from ..helpers import uint_to_little_endian_bytearray, merge_bytes
from ..helpers import parse_param_string, REGEXP_PARAM_STRING
from ..color_helpers import is_color, parse_color_string
from ..color_helpers import parse_color_gradient_string


_default_duration = 1000


def _handle_color_tuple(color):
    if len(color) != 3:
        raise ValueError("Not a valid color %s" % str(color))
    for channel in color:
        if type(channel) != int or channel < 0 or channel > 255:
            raise ValueError("Not a valid color %s" % str(color))
    return [
        {
            "pos": 0,
            "color": color,
        }
    ]


def _handle_color_string(color):
    return [
        {
            "pos": 0,
            "color": parse_color_string(color),
        }
    ]


def _handle_rgbgradient_dict(colors):
    duration = _default_duration
    gradient = []

    if "duration" in colors:
        duration = colors["duration"]

    if "colors" in colors:
        for stop in colors["colors"]:
            color = stop["color"]
            if type(color) is str:
                color = parse_color_string(color)
            if type(color) not in [tuple, list] or len(color) != 3:
                raise ValueError("Not a valid color %s" % str(color))
            for channel in color:
                if type(channel) != int or channel < 0 or channel > 255:
                    raise ValueError("Not a valid color %s" % str(color))
            gradient.append(
                {
                    "pos": stop["pos"] if "pos" in stop else 0,
                    "color": color,
                }
            )

    # Smooth gradient (if possible) by adding a final color
    if len(gradient) < 14 and gradient[-1]["pos"] != 100:
        gradient.append(
            {
                "pos": 100,
                "color": gradient[0]["color"],
            }
        )

    return duration, gradient


def _handle_rgbgradient_string(colors):
    gradient_dict = parse_param_string(
        colors,
        value_parsers={
            "rgbgradient": {
                "duration": int,
                "colors": parse_color_gradient_string,
            }
        },
    )

    return _handle_rgbgradient_dict(gradient_dict["rgbgradient"])


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbgradient" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    header_length = setting_info["rgbgradient_header"]["header_length"]
    led_id_offsets = setting_info["rgbgradient_header"]["led_id_offsets"]
    duration_offset = setting_info["rgbgradient_header"]["duration_offset"]
    duration_length = setting_info["rgbgradient_header"]["duration_length"]
    repeat_offset = setting_info["rgbgradient_header"]["repeat_offset"]
    triggers_offset = setting_info["rgbgradient_header"]["triggers_offset"]
    color_count_offset = setting_info["rgbgradient_header"]["color_count_offset"]

    is_gradient = False
    duration = _default_duration
    repeat = 0x00
    triggers = 0x00
    led_id = setting_info["led_id"]
    gradient = []

    # Color tuple
    if type(colors) in (tuple, list):
        is_gradient = False
        gradient = _handle_color_tuple(colors)

    # Simple color string
    elif type(colors) is str and is_color(colors):
        is_gradient = False
        gradient = _handle_color_string(colors)

    # Color gradient as dict
    elif type(colors) is dict:
        is_gradient = True
        duration, gradient = _handle_rgbgradient_dict(colors)

    # Color gradient as string
    elif is_rgbgradient(colors)[0]:
        is_gradient = True
        duration, gradient = _handle_rgbgradient_string(colors)
    else:
        raise ValueError("Not a valid color or rgbgradient %s" % str(colors))

    # -- handle repeat flag

    if not is_gradient or triggers != 0x00:
        repeat = 0x01

    # -- Check

    if len(gradient) == 0:
        raise ValueError("no color: %s" % str(colors))

    if len(gradient) > 14:
        raise ValueError("a maximum of 14 color stops are allowed")

    # TODO check pos orders

    # -- Generate header

    header = [0x00] * header_length
    header[repeat_offset] = repeat
    header[triggers_offset] = triggers
    header[color_count_offset] = len(gradient)

    for led_id_offset in led_id_offsets:
        header[led_id_offset] = led_id

    offset = 0
    for b in uint_to_little_endian_bytearray(duration, duration_length):
        header[duration_offset + offset] = b
        offset += 1

    # -- Generate body

    body = list(gradient[0]["color"])

    last_real_pos = 0
    for pos, color in [(item["pos"], item["color"]) for item in gradient]:
        real_pos = int(pos * 255 / 100)
        body = merge_bytes(body, color, real_pos - last_real_pos)
        last_real_pos = real_pos

    # --

    return merge_bytes(header, body)


def is_rgbgradient(string):
    """Check if the rgbradient expression is valid.

    :param str string: The string to validate.
    :rtype: (bool, str)

    >>> is_rgbgradient("foo(colors=0:red)")
    (False, "... It must looks like 'rgbgradient(<PARAMS>)'...")
    >>> is_rgbgradient("rgbgradient(duration=1000)")
    (False, "... You must provide at least one color: ...")
    >>> is_rgbgradient("rgbgradient(colors=red)")
    (False, "invalid color gradient...")
    >>> is_rgbgradient("rgbgradient(colors=0:red; foo=bar)")
    (False, "unknown parameter 'foo'...")
    """
    try:
        rgbgradient_dict = parse_param_string(
            string,
            value_parsers={
                "rgbgradient": {
                    "duration": int,
                    "colors": parse_color_gradient_string,
                }
            },
        )
    except ValueError as e:
        return False, str(e)

    if "rgbgradient" not in rgbgradient_dict:
        reason = ""
        reason += "invalid rgbgradient expression. "
        reason += "It must looks like 'rgbgradient(<PARAMS>)'."
        return False, reason

    if (
        "colors" not in rgbgradient_dict["rgbgradient"]
        or len(rgbgradient_dict["rgbgradient"]) == 0
    ):
        reason = ""
        reason += "invalid rgbgradient expression. "
        reason += "You must provide at least one color: "
        reason += "'rgbgradient(colors=<POS>: <COLOR>)'."
        return False, reason

    _allowed_params = ["colors", "duration"]
    for key in rgbgradient_dict["rgbgradient"].keys():
        if key not in _allowed_params:
            reason = ""
            reason += "unknown parameter '%s'. " % key
            reason += "Allowed parameters are %s." % ", ".join(
                ["'%s'" % p for p in _allowed_params]
            )
            return False, reason

    return True, ""


class CheckGradientAction(argparse.Action):
    """Validate colors gradient from CLI"""

    def __call__(self, parser, namespace, value, option_string=None):
        if is_color(value):
            setattr(namespace, self.dest.upper(), value)
            return

        if REGEXP_PARAM_STRING.match(value):
            is_valid, reason = is_rgbgradient(value)

            if is_valid:
                setattr(namespace, self.dest.upper(), value)
                return

            raise argparse.ArgumentError(self, "%s" % reason)

        else:
            raise argparse.ArgumentError(
                self, "not a valid color or rgbgradient: '%s'" % value
            )


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "rgbgradient" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (default: %s)" % (
        setting_info["description"],
        str(setting_info["default"]).replace("%", "%%"),
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        dest=setting_name,
        help=description,
        type=str,
        action=CheckGradientAction,
        metavar=setting_name.upper(),
    )
