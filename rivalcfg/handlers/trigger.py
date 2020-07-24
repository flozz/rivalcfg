"""
The "trigger" type handles RGB color triggers. Simple RGB color can also
be used.

RGB trigger syntax example::

    trigger(duration=1000; colors=#ff0000, #00ff00)
    trigger(colors=red, lime)

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

   A maximum of 14 color stops can be defined in a trigger.


Device Profile
--------------

Example of a trigger value type in a device profile:

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
                "value_type": "trigger",
                "trigger_header": {
                    "header_length": 28,       # Length of the header excuding command / LED ID
                    "led_id_offsets": [0, 5],  # Offset of the "led_id" fields
                    "duration_offset": 6,      # Offset of the "duration" field
                    "duration_length": 2,      # Length of the "duration" field (in Bytes)
                    "repeat_offset": 22,       # Offset of the "repeat" flag
                    "triggers_offset": 23,     # Offset of the "triggers" field (buttons mask)
                    "color_count_offset": 27,  # Offset of the "color_count" field
                },
                "led_id": 0x01,
                "default": "trigger(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -c LOGO_COLOR, --logo-color LOGO_COLOR
                         Set the colors and the effects of the logo LED (default:
                         trigger(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff))

Example of CLI usage::

    rivalcfg --logo-color="trigger(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
    rivalcfg --logo-color=red
    rivalcfg --logo-color=FF1800


Functions
---------
"""  # noqa


import argparse

from ..helpers import uint_to_little_endian_bytearray, merge_bytes
from ..helpers import parse_param_string, REGEXP_PARAM_STRING
from ..color_helpers import is_color, parse_color_string
from ..color_helpers import parse_multi_color_string


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
        "color": color,
    }]


def _handle_color_string(color):
    return [{
        "color": parse_color_string(color),
    }]


def _handle_trigger_dict(colors):
    duration = _default_duration
    trigger = []

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
            trigger.append({
                "color": color
            })

    # Smooth trigger (if possible) by adding a final color
    if len(trigger) < 2:
        trigger.append({
            "color": trigger[0]["color"],
            })

    return duration, trigger


def _handle_trigger_string(colors):
    trigger_dict = parse_param_string(colors, value_parsers={
            "trigger": {
                "duration": int,
                "colors": parse_multi_color_string,
            }
        })

    return _handle_trigger_dict(trigger_dict["trigger"])


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    duration_length = 2

    duration = _default_duration
    trigger = []

    # Color tuple
    if type(colors) in (tuple, list):
        trigger = _handle_color_tuple(colors)

    # Simple color string
    elif type(colors) in [str, _unicode_type] and is_color(colors):
        trigger = _handle_color_string(colors)

    # Color trigger as dict
    elif type(colors) is dict:
        duration, trigger = _handle_trigger_dict(colors)

    # Color trigger as string
    elif is_trigger(colors)[0]:
        duration, trigger = _handle_trigger_string(colors)
    else:
        raise ValueError("Not a valid color or trigger %s" % str(colors))

    # -- Check
    trigger_length = len(trigger)

    if trigger_length == 0:
        raise ValueError("no color: %s" % str(colors))

    if trigger_length > 2:
        raise ValueError("a maximum of 2 color stops are allowed")

    minimum_duration = 1000
    if duration < minimum_duration:
        raise ValueError("a duration of %i or above" %
                         (minimum_duration))

    # See allows a max duration of 30.00 sec
    if duration > 9990:
        raise ValueError("a maximum duration of 30000ms is allowed")

    # -- Generate header

    duration = uint_to_little_endian_bytearray(duration, duration_length)

    # -- Generate body
    body = []
    for color in [item["color"] for item in trigger]:
        body = merge_bytes(body, color)

    return merge_bytes(setting_info["led_id"], body, duration)


def is_trigger(string):
    """Check if the regbradient expression is valid.

    :param str string: The string to validate.
    :rtype: (bool, str)

    >>> is_trigger("foo(colors=0:red)")
    (False, "... It must looks like 'trigger(<PARAMS>)'...")
    >>> is_trigger("trigger(duration=1000)")
    (False, "... You must provide at least one color: ...")
    >>> is_trigger("trigger(colors=red)")
    (False, "invalid color trigger...")
    >>> is_trigger("trigger(colors=0:red; foo=bar)")
    (False, "unknown parameter 'foo'...")
    """
    try:
        trigger_dict = parse_param_string(string, value_parsers={
            "trigger": {
                "duration": int,
                "colors": parse_multi_color_string,
            }
        })
    except ValueError as e:
        return False, str(e)

    if "trigger" not in trigger_dict:
        reason = ""
        reason += "invalid trigger expression. "
        reason += "It must looks like 'trigger(<PARAMS>)'."
        return False, reason

    if "colors" not in trigger_dict["trigger"] \
            or len(trigger_dict["trigger"]) == 0:
        reason = ""
        reason += "invalid trigger expression. "
        reason += "You must provide at least one color: "
        reason += "'trigger(colors=<COLOR>)'."
        return False, reason

    _allowed_params = ["colors", "duration"]
    for key in trigger_dict["trigger"].keys():
        if key not in _allowed_params:
            reason = ""
            reason += "unknown parameter '%s'. " % key
            reason += "Allowed parameters are %s." % ", ".join(
                    ["'%s'" % p for p in _allowed_params])
            return False, reason

    return True, ""


class CheckGradientAction(argparse.Action):
    """Validate colors trigger from CLI"""

    def __call__(self, parser, namespace, value, option_string=None):
        if is_color(value):
            setattr(namespace, self.dest.upper(), value)
            return

        if REGEXP_PARAM_STRING.match(value):
            is_valid, reason = is_trigger(value)

            if is_valid:
                setattr(namespace, self.dest.upper(), value)
                return

            raise argparse.ArgumentError(self, "%s" % reason)

        else:
            raise argparse.ArgumentError(self, "not a valid color or trigger: '%s'" % value)  # noqa


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "trigger" type setting to the given CLI arguments parser.

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
