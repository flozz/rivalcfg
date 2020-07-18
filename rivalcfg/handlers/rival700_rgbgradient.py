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
"""  # noqa


import argparse

from ..helpers import uint_to_little_endian_bytearray, merge_bytes
from ..helpers import bytes_to_high_low_nibbles, nibbles_to_byte
from ..helpers import parse_param_string, REGEXP_PARAM_STRING
from ..color_helpers import is_color, parse_color_string
from ..color_helpers import parse_color_gradient_string


# Compatibility with Python 2.7.
# On Python 2 the type is 'unicode'
# On Python 3 the type is 'str'
_unicode_type = type(u"")

_default_duration = 1000


def _handle_color_tuple(color):
    if len(color) != 3:
        raise ValueError("Not a valid color %s" % str(color))
    for channel in color:
        if type(channel) != int or channel < 0 or channel > 255:
            raise ValueError("Not a valid color %s" % str(color))
    return [{
        "pos": 0,
        "color": color,
    }]


def _handle_color_string(color):
    return [{
        "pos": 0,
        "color": parse_color_string(color),
    }]


def _handle_rival700_rgbgradient_dict(colors):
    duration = _default_duration
    gradient = []

    if "duration" in colors:
        duration = colors["duration"]

    if "colors" in colors:
        for stop in colors["colors"]:
            color = stop["color"]
            if type(color) in [str, _unicode_type]:
                color = parse_color_string(color)
            if type(color) not in [tuple, list] or len(color) != 3:
                raise ValueError("Not a valid color %s" % str(color))
            for channel in color:
                if type(channel) != int or channel < 0 or channel > 255:
                    raise ValueError("Not a valid color %s" % str(color))
            gradient.append({
                "pos": stop["pos"] if "pos" in stop else 0,
                "color": color
            })

    # Smooth gradient (if possible) by adding a final color
    if len(gradient) < 14 and gradient[-1]["pos"] != 100:
        gradient.append({
            "pos": 100,
            "color": gradient[0]["color"],
            })

    return duration, gradient


def _handle_rival700_rgbgradient_string(colors):
    gradient_dict = parse_param_string(colors, value_parsers={
            "rgbgradient": {
                "duration": int,
                "colors": parse_color_gradient_string,
            }
        })

    return _handle_rival700_rgbgradient_dict(gradient_dict["rgbgradient"])


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    color_field_length = setting_info["rival700_rgbgradient_header"]["color_field_length"]
    duration_length = setting_info["rival700_rgbgradient_header"]["duration_length"]
    maxgradient = setting_info["rival700_rgbgradient_header"]["maxgradient"]
    duration = _default_duration
    gradient = []

    # Color tuple
    if type(colors) in (tuple, list):
        gradient = _handle_color_tuple(colors)

    # Simple color string
    elif type(colors) in [str, _unicode_type] and is_color(colors):
        gradient = _handle_color_string(colors)

    # Color gradient as dict
    elif type(colors) is dict:
        duration, gradient = _handle_rival700_rgbgradient_dict(colors)

    # Color gradient as string
    elif is_rgbgradient(colors)[0]:
        duration, gradient = _handle_rival700_rgbgradient_string(colors)
    else:
        raise ValueError("Not a valid color or rgbgradient %s" % str(colors))

    # -- Check

    if len(gradient) == 0:
        raise ValueError("no color: %s" % str(colors))

    """ Sse allowes a maximun of 14 rgbgradient patterns but there is room in the
    command for up to 16 rgbgradient patterns and it will take 16 arguments.
    """
    if len(gradient) > maxgradient:
        raise ValueError("a maximum of %i color stops are allowed" % (maxgradient))

    # TODO check pos orders

    # -- Generate header

    start_header = [0x1d, 0x01, 0x02, 0x31, 0x51, 0xff, 0xc8, 0x00]
    """            [0xff, 0x3c, 0x00, 0xff, 0x32, 0xc8, 0xc8, 0x00]
    [WIP] header command
    """
    header = merge_bytes(setting_info["led_id"], start_header)

    """ 7 bytes in a stage, first byte is index, 2nd is padding,
    3-5 is signed bytes depecting color increase/decrease, 6 bytes
    is padding, the 7-8 is time since last stage in ms
    Process colors and positions in shift array, appending each stage
    to the previous one
    """
    stage = []
    last_pos = gradient[0]["pos"]
    start_color = gradient[0]["color"]

    oldcolor = list(start_color)
    num = 0
    del gradient[0]
    for pos, color in [(item["pos"], item["color"]) for item in gradient]:
        stage.append(num)  # Stage index number
        stage.append(00)   # Padding
        pos = pos - last_pos
        time = int((duration / 100) * pos)
        last_pos = last_pos + pos
        if time == 0:
            raise ValueError("Incompatble times set, please set different timings")
        index = 0
        for rgb in color:
            diff = rgb - oldcolor[index]
            ramp = int(diff / time * 16)
            oldcolor[index] = rgb
            stage = merge_bytes(stage, ramp & 255)
            index = index + 1
            # print("rgb", rgb, diff, ramp, ramp & 255, hex(ramp & 255),num)
        stage.append(00)  # Padding
        time = uint_to_little_endian_bytearray(time, 2)
        stage = merge_bytes(stage, time)
        num = num + 1

    header = merge_bytes(header, stage)
    """ Pad the rest of the command so we can place start color, end suffix and
    cycle time at the correct location in the command
    """
    padding = [0] * (color_field_length - len(header))
    header = merge_bytes(header, padding)
    duration = uint_to_little_endian_bytearray(duration, duration_length)

    # Split start color into high low nibbles
    split_color = []
    for i in range(len(start_color)):
        high, low = bytes_to_high_low_nibbles(start_color[i])
        left_byte = nibbles_to_byte(low, 00)
        right_byte = high & 0x0F
        split_color.append(left_byte)
        split_color.append(right_byte)

    end_suffix = [0xff, 0x00, 0xdc, 0x05, 0x8a, 0x02, 0x00, 0x00, 0x00, 0x00,
                  0x01, 0x00, 0x03, 0x00]
    #                         0x0c need to work out what this does
    suffix = merge_bytes(split_color, end_suffix, duration)

    return merge_bytes(header, suffix)


def is_rgbgradient(string):
    """Check if the regbradient expression is valid.

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
        rgbgradient_dict = parse_param_string(string, value_parsers={
            "rgbgradient": {
                "duration": int,
                "colors": parse_color_gradient_string,
            }
        })
    except ValueError as e:
        return False, str(e)

    if "rgbgradient" not in rgbgradient_dict:
        reason = ""
        reason += "invalid rgbgradient expression. "
        reason += "It must looks like 'rgbgradient(<PARAMS>)'."
        return False, reason

    if "colors" not in rgbgradient_dict["rgbgradient"] \
            or len(rgbgradient_dict["rgbgradient"]) == 0:
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
                    ["'%s'" % p for p in _allowed_params])
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
            raise argparse.ArgumentError(self, "not a valid color or rgbgradient: '%s'" % value)  # noqa


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
            metavar=setting_name.upper()
            )
