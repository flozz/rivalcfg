"""
The "multidpi_range" type alows to pick values in an input range and transforms
it into values from an output range. If the input values do not correspond to
one of the input range step, they are rounded to match the nearest step.

This type is used to support devices where we can configure from ``1`` to ``n``
DPI settings in a single command, like the Rival 3.

For example with an input range like ``[0, 1000, 100]`` and an output range
like ``[0, 10, 1]``, you can have the following pair:

* ``0`` -> ``0``
* ``100`` -> ``1``
* ``110`` -> ``1`` (``110`` rounded to ``100``)
* ``190`` -> ``2`` (``190`` rounded to ``200``)
* ``200`` -> ``2``
* ``300`` -> ``3``
* ...
* ``1000`` -> ``10``


Device Profile
--------------

Example of a multidpi_range value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "sensitivity1": {
                "label": "Sensitivity presets",
                "description": "Set sensitivity presets (DPI)",
                "cli": ["-s", "--sensitivity"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x0B, 0x00],
                "value_type": "multidpi_range",
                "input_range": [200, 7200, 100],
                "output_range": [0x04, 0xA7, 2],
                "dpi_length_byte": 1,     # Little endian
                "first_preset": 1,
                "count_mode": "number",   # number, flag
                "max_preset_count": 5,
                "default": "800, 1600",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -s SENSITIVITY, --sensitivity SENSITIVITY
                        Set sensitivity preset (DPI) (up to 5 settings, from 200 dpi to 8500
                        dpi, default: '800, 1600')

Example of CLI usage::

    rivalcfg --sensitivity 1600
    rivalcfg --sensitivity "800,1600"
    rivalcfg --sensitivity "200, 400, 800, 1600, 8000"


Functions
---------
"""


import re
import argparse

from ..helpers import merge_bytes, uint_to_little_endian_bytearray
from .range import process_range


def process_value(setting_info, value, selected_preset=None):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "range" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param value: The input value.
    :param int selected_preset: The DPI preset to select (0 is always the
                                first preset).
    :rtype: list[int]
    """
    dpis = []

    if type(value) in (int, float):
        dpis = [int(value)]
    elif type(value) in (list, tuple):
        dpis = [int(dpi) for dpi in value]
    else:
        dpis = [int(dpi) for dpi in value.replace(" ", "").split(",")]

    # Selected preset

    if selected_preset is None:
        selected_preset = setting_info["first_preset"]
    else:
        selected_preset += setting_info["first_preset"]

    # checks

    if len(dpis) == 0:
        raise ValueError("you must provide at least one preset")

    if len(dpis) > setting_info["max_preset_count"]:
        raise ValueError(
            "you provided %i preset but the device accepts a maximum of %i presets"
            % (len(dpis), setting_info["max_preset_count"])
        )

    if "first_preset" not in setting_info:
        raise ValueError(
            "Missing 'first_preset' parameter for 'multidpi_range' handler"
        )

    if (
        not setting_info["first_preset"]
        <= selected_preset
        < len(dpis) + setting_info["first_preset"]
    ):
        raise ValueError("the selected preset is out of range")

    if "dpi_length_byte" not in setting_info:
        raise ValueError(
            "Missing 'dpi_length_byte' parameter for 'multidpi_range' handler"
        )

    if "count_mode" not in setting_info:
        raise ValueError("Missing 'count_mode' parameter for 'multidpi_range' handler")

    if setting_info["count_mode"] not in ("number", "flag"):
        raise ValueError(
            "Invalid 'count_mode' parameter '%s'" % setting_info["count_mode"]
        )

    dpi_length = setting_info["dpi_length_byte"]
    count_mode = setting_info["count_mode"]

    # DPIs

    output_values = []

    for dpi in dpis:
        value = process_range(setting_info, dpi)
        value = uint_to_little_endian_bytearray(value, dpi_length)
        output_values = merge_bytes(output_values, value)

    # Count

    dpi_count = len(dpis)

    if count_mode == "flag":
        dpi_count = 0b11111111 >> (8 - dpi_count)

    #

    return merge_bytes(dpi_count, selected_preset, output_values)


def cli_multirange_validator(max_preset_count):
    class CheckMultiDpiRange(argparse.Action):
        """Validate value from CLI"""

        def __call__(self, parser, namespace, value, option_string=None):
            if not re.match(
                r"^ *[0-9]+( *, *[0-9]+){0,%i} *$" % (max_preset_count - 1),
                value,
            ):
                raise argparse.ArgumentError(self, "invalid DPI list: '%s'" % value)
            setattr(namespace, self.dest.upper(), value)

    return CheckMultiDpiRange


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "range" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (up to %i settings, from %i dpi to %i dpi, default: '%s')" % (
        setting_info["description"],
        setting_info["max_preset_count"],
        setting_info["input_range"][0],
        setting_info["input_range"][1],
        str(setting_info["default"]),
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        help=description,
        dest=setting_name.upper(),
        metavar=setting_name.upper(),
        action=cli_multirange_validator(setting_info["max_preset_count"]),
    )
