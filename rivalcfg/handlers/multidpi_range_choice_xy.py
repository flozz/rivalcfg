"""
The "multidpi_range_choice_xy" type alows to pick values in an input range and
transforms it into values from a fixed output list.  If the input values do not
correspond to one of the available output choices, they are rounded to match
the nearest DPI.

Unlike the "multidpi_range_choice" handler, "multidpi_range_choice_xy" allows
to set a different DPI on X and Y axis.

This type is used to support devices where we can configure from ``1`` to ``n``
DPI settings in a single command, like the Rival 3 Gen 2.

For example with an input range like ``[0, 1000, 100]`` and an output range
like ``{0: 0, 100: 1, 200: 2, 300: 4,...}``, you can have the following pair:

* ``0`` -> ``0``
* ``100`` -> ``1``
* ``110`` -> ``1`` (``1100`` rounded to ``100``)
* ``190`` -> ``2`` (``1900`` rounded to ``200``)
* ``200`` -> ``2``
* ``300`` -> ``4``
* ...


Device Profile
--------------

Example of a multidpi_range_choice value type in a device profile:

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
                "value_type": "multidpi_range_choice_xy",
                "input_range": [100, 18000, 100],
                "output_choices": {
                    100: 0x00,
                    200: 0x02,
                    300: 0x03,
                    400: 0x04,
                    ...
                    18000: 0xD6,
                },
                "xy_mapping": "xyxy",     # "xyxy" or "xxyy"
                "dpi_length_byte": 1,  # Little endian
                "first_preset": 1,
                "max_preset_count": 5,
                "default": "800:800, 1600:1600",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -s SENSITIVITY, --sensitivity SENSITIVITY
                        Set sensitivity preset (DPI) (up to 5 settings, from 200 dpi to 8500
                        dpi, default (x1:y1,x2:y2): '800:800, 1600:1600')

Example of CLI usage::

    rivalcfg --sensitivity 1600                         # 1 preset;  x1=1600dpi:y1=1600dpi
    rivalcfg --sensitivity 1600:1600                    # 1 preset;  x1=1600dpi:y1=1600dpi
    rivalcfg --sensitivity "800,1600"                   # 2 presets; x1=800dpi:y1=800dpi, x2=1600dpi:y2=1600dpi
    rivalcfg --sensitivity "800:1000, 1600:2000"        # 2 presets; x1=800dpi:y1=1000dpi, x2=1600dpi:y2=2000dpi
    rivalcfg --sensitivity "200, 400, 800, 1600, 8000"  # 5 presets; ...


Functions
---------
"""

import re
import argparse

from .range_choice import process_range_choice
from ..helpers import merge_bytes, uint_to_little_endian_bytearray


def normalize_value(value):
    """Normalize input value to the following format::

        [[x1: int, y1: int], [x2: int, y2: int], ...]

    >>> normalize_value(100)
    [[100, 100]]
    >>> normalize_value([100, 200])
    [[100, 100], [200, 200]]
    >>> normalize_value([[100]])
    [[100, 100]]
    >>> normalize_value([[100, 150], [200, 250]])
    [[100, 150], [200, 250]]
    >>> normalize_value([[100, 150], 200])
    [[100, 150], [200, 200]]
    >>> normalize_value("100")
    [[100, 100]]
    >>> normalize_value("100:100")
    [[100, 100]]
    >>> normalize_value("100,200")
    [[100, 100], [200, 200]]
    >>> normalize_value(" 100:150, 200: 250 ")
    [[100, 150], [200, 250]]
    >>> normalize_value("100:150, 200")
    [[100, 150], [200, 200]]
    """
    if isinstance(value, (int, float)):  # 100 -> [[100, 100]]
        normalized = [[int(value), int(value)]]
    elif isinstance(value, (list, tuple)):
        normalized = []
        for item in value:
            if isinstance(item, (int, float)):  # [100] -> [[100, 100]]
                item = [int(item), int(item)]
            elif isinstance(item, (list, tuple)):
                if len(item) == 1:  # [[100]] -> [[100, 100]]
                    item = [int(item[0]), int(item[0])]
                elif len(item) == 2:  # [[100, 100]]
                    item = [int(item[0]), int(item[1])]
                else:
                    ValueError("Too many items")
            else:
                ValueError("Unsuported type")
            normalized.append(item)
    else:  # "100:100,200:200"
        normalized = []
        for item in value.replace(" ", "").split(","):
            item = item.split(":")
            if len(item) == 1:  # "100" -> [[100, 100]]
                item = [int(item[0]), int(item[0])]
            elif len(item) == 2:  # 100:100 -> [[100, 100]]
                item = [int(item[0]), int(item[1])]
            else:
                ValueError("Too many items")
            normalized.append(item)
    return normalized


def process_value(setting_info, value, selected_preset=None):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "multidpi_range_choice" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param value: The input value.
    :param int selected_preset: The DPI preset to select (0 is always the
                                first preset).
    :rtype: list[int]
    """
    dpis = normalize_value(value)

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
            "Missing 'first_preset' parameter for 'multidpi_range_choice_xy' handler"
        )

    if (
        not setting_info["first_preset"]
        <= selected_preset
        < len(dpis) + setting_info["first_preset"]
    ):
        raise ValueError("the selected preset is out of range")

    if "xy_mapping" not in setting_info:
        raise ValueError(
            "Missing 'xy_mapping' parameter for 'multidpi_range_choice_xy' handler"
        )

    if setting_info["xy_mapping"] not in ["xyxy", "xxyy"]:
        raise ValueError(
            "Unsupported value for xy-mapping: %s" % setting_info["xy_mapping"]
        )

    xy_mapping = setting_info["xy_mapping"]

    if "dpi_length_byte" not in setting_info:
        raise ValueError(
            "Missing 'dpi_length_byte' parameter for 'multidpi_range_choice_xy' handler"
        )

    dpi_length = setting_info["dpi_length_byte"]

    # DPIs

    output_values = []

    for dpi_x, dpi_y in dpis:
        output_values.append(
            [
                uint_to_little_endian_bytearray(
                    process_range_choice(setting_info, dpi_x),
                    dpi_length,
                ),
                uint_to_little_endian_bytearray(
                    process_range_choice(setting_info, dpi_y),
                    dpi_length,
                ),
            ]
        )

    if xy_mapping == "xyxy":
        # Must be done twice as merge_bytes is not recursive
        output_values = merge_bytes(*output_values)
        output_values = merge_bytes(*output_values)
    else:  # xxyy
        output_values = merge_bytes(
            *[dx for dx, dy in output_values],
            *[dy for dx, dy in output_values],
        )

    # Count

    dpi_count = len(dpis)

    #

    return merge_bytes(dpi_count, selected_preset, output_values)


def cli_multirange_xy_validator(max_preset_count):
    class CheckMultiDpiRangeXY(argparse.Action):
        """Validate value from CLI"""

        def __call__(self, parser, namespace, value, option_string=None):
            if not re.match(
                r"^ *([0-9]+( *: *[0-9]+)?)( *, *([0-9]+( *: *[0-9]+)?)){0,%i} *$"
                % (max_preset_count - 1),
                value,
            ):
                raise argparse.ArgumentError(self, "invalid DPI list: '%s'" % value)
            setattr(namespace, self.dest.upper(), value)

    return CheckMultiDpiRangeXY


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
        action=cli_multirange_xy_validator(setting_info["max_preset_count"]),
    )
