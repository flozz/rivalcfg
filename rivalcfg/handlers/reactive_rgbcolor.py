"""
The "reactive_rgbcolor" type handles RGB color effects in reaction to a button
click.

It can be disabled with the following values:

* ``None``
* ``"off"``
* ``"disable"``

It supports hexadecimal colors:

* ``#FF0000``
* ``FF0000``
* ``#F00``
* ``F00``

RGB tuples or list (only from Python API for this one):

* ``(255, 0, 0)``
* ``[255, 0, 0]``

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

            "reactive_color": {
                "label": "Reactive color",
                "description": "Set the color of the LED in reaction to a button click",
                "cli": ["-a", "--reactive-color"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x26],
                "value_type": "reactive_rgbcolor",
                "default": "off",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    -a REACTIVE_COLOR, --reactive-color REACTIVE_COLOR
                          Set the color of the LEDs in reaction to a button click
                          (e.g. off, disable, red, #ff0000, ff0000, #f00, f00,
                          default: off)

Example of CLI usage::

    rivalcfg --reactive-color=off
    rivalcfg --reactive-color=disable
    rivalcfg --reactive-color=red
    rivalcfg --reactive-color=ff0000
    rivalcfg --reactive-color=f00


Functions
---------
"""


import argparse

from ..color_helpers import is_color, parse_color_string


def process_value(setting_info, color):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "reactive_rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,None color: The reactive color.
    :rtype: [int, int, int]
    """
    # Disable the reactive color
    if color is None or str(color).lower() in ["off", "disable"]:
        return [0x00, 0x00, 0x00, 0x00, 0x00]

    # Color tuple
    if type(color) in (tuple, list):
        if len(color) != 3:
            raise ValueError("Not a valid color %s" % str(color))
        for channel in color:
            if type(channel) != int or channel < 0 or channel > 255:
                raise ValueError("Not a valid color %s" % str(color))
        return [0x01, 0x00] + list(color)
    if is_color(color):
        return [0x01, 0x00] + list(parse_color_string(color))

    raise ValueError("Not a valid color %s" % str(color))


class CheckColorAction(argparse.Action):
    """Validate reactive colors from CLI"""

    def __call__(self, parser, namespace, value, option_string=None):
        if not is_color(value) and value.lower() not in ["off", "disable"]:
            raise argparse.ArgumentError(self, "invalid reactive color: '%s'" % value)
        setattr(namespace, self.dest.upper(), value)


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "reactive_rgbcolor" type setting to the given CLI
    arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = (
        "%s (e.g. off, disable, red, #ff0000, ff0000, #f00, f00, default: %s)"
        % (
            setting_info["description"],
            str(setting_info["default"]),
        )
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        dest=setting_name,
        help=description,
        type=str,
        action=CheckColorAction,
        metavar=setting_name.upper(),
    )
