"""
The "reactive" type handles RGB colors. Simple RGB color can also
be used.

RGB reactive syntax example::

    reactive(duration=1000; colors=#ff0000, #00ff00)
    reactive(colors=red, lime)

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
            {"color": "red"},
            {"color": "#00FF00"},
            {"color": (0, 0, 255)},
        ]
    }

.. NOTE::

   Only 2 color stops can be defined in a reactive profile.


Device Profile
--------------

Example of a reactive value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "logo_reactive": {
                "label": "Logo LED reactive illumination",
                "description": "Set the logo reactive colors",
                "cli": ["-r", "--logo-reactive"],
                "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
                "command": [0x05, 0x00],
                "command_suffix": [0x00, 0x08, 0x00, 0x00],
                "value_type": "reactive",
                "led_id": 0x0,
                "default": [["#FF3C00", "#FF32C8"], 2000]
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -t LOGO_RECATIVE, --logo-reactive LOGO_COLOR
                         Set the colors and the effects of the logo LED (default:
                         reactive(duration=1000; colors=#ff0000, #00ff00, #0000ff))

Example of CLI usage::

    rivalcfg --logo-reactive="reactive(duration=1000; colors=#ff0000, #00ff00, #0000ff)"


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


def _handle_reactive_dict(colors):
    duration = _default_duration
    color_array = []

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
            color_array.append({
                "color": color
            })

    return duration, color_array


def _handle_reactive_string(colors):
    reactive_dict = parse_param_string(colors, value_parsers={
            "reactive": {
                "duration": int,
                "colors": parse_multi_color_string,
            }
        })

    return _handle_reactive_dict(reactive_dict["reactive"])


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "reactive" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    duration_length = 2

    duration = _default_duration
    color_array = []

    # Color tuple
    if type(colors) in (tuple, list):
        color_array = _handle_color_tuple(colors)

    # Simple color string
    elif type(colors) in [str, _unicode_type] and is_color(colors):
        color_array = _handle_color_string(colors)

    # Color reactive as dict
    elif type(colors) is dict:
        duration, color_array = _handle_reactive_dict(colors)

    # Color reactive as string
    elif is_reactive(colors)[0]:
        duration, color_array = _handle_reactive_string(colors)
    else:
        raise ValueError("Not a valid color or reactive %s" % str(colors))

    # -- Check
    reactive_length = len(color_array)

    if reactive_length == 0:
        raise ValueError("no color: %s" % str(colors))

    if reactive_length != 2:
        raise ValueError("2 color stops are needed")

    minimum_duration = 1000
    if duration < minimum_duration:
        raise ValueError("a duration of %i or above" %
                         (minimum_duration))

    # See allows a max duration of 9.99 sec
    if duration > 9990:
        raise ValueError("a maximum duration of 9990ms is allowed")

    # -- Generate header
    duration = uint_to_little_endian_bytearray(duration, duration_length)

    # -- Generate body
    body = []
    for color in [item["color"] for item in color_array]:
        body = merge_bytes(body, color)

    return merge_bytes(setting_info["led_id"], body, duration)


def is_reactive(string):
    """Check if the reactive expression is valid.

    :param str string: The string to validate.
    :rtype: (bool, str)

    >>> is_reactive("foo(colors=0:red)")
    (False, "... It must looks like 'reactive(<PARAMS>)'...")
    >>> is_reactive("reactive(duration=1000)")
    (False, "... You must provide at least one color: ...")
    >>> is_reactive("reactive(colors=red, foo=bar)")
    (False, "invalid parameter string 'reactive(colors=red, foo=bar)'")
    """
    try:
        reactive_dict = parse_param_string(string, value_parsers={
            "reactive": {
                "duration": int,
                "colors": parse_multi_color_string,
            }
        })
    except ValueError as e:
        return False, str(e)

    if "reactive" not in reactive_dict:
        reason = ""
        reason += "invalid reactive expression. "
        reason += "It must looks like 'reactive(<PARAMS>)'."
        return False, reason

    if "colors" not in reactive_dict["reactive"] \
            or len(reactive_dict["reactive"]) == 0:
        reason = ""
        reason += "invalid reactive expression. "
        reason += "You must provide at least one color: "
        reason += "'reactive(colors=<COLOR>)'."
        return False, reason

    _allowed_params = ["colors", "duration"]
    for key in reactive_dict["reactive"].keys():
        if key not in _allowed_params:
            reason = ""
            reason += "unknown parameter '%s'. " % key
            reason += "Allowed parameters are %s." % ", ".join(
                    ["'%s'" % p for p in _allowed_params])
            return False, reason

    return True, ""


class CheckReactiveAction(argparse.Action):
    """Validate colors reactive from CLI"""

    def __call__(self, parser, namespace, value, option_string=None):
        if is_color(value):
            setattr(namespace, self.dest.upper(), value)
            return

        if REGEXP_PARAM_STRING.match(value):
            is_valid, reason = is_reactive(value)

            if is_valid:
                setattr(namespace, self.dest.upper(), value)
                return

            raise argparse.ArgumentError(self, "%s" % reason)

        else:
            raise argparse.ArgumentError(self, "not a valid color or reactive: '%s'" % value)  # noqa


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "reactive" type setting to the given CLI arguments parser.

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
            action=CheckReactiveAction,
            metavar=setting_name.upper()
            )
