"""
The "range_choice" type alows to pick a value in an input range and transforms
it into a value from a fixed output list. If the input value do not correspond to
one of the available output choices, it is rounded to match the nearest DPI.

For example with an input range like ``[0, 1000, 100]`` and an output range
like ``{0: 0, 100: 1, 200: 2, 300: 4,...}``, you can have the following pair:

* ``0`` -> ``0``
* ``100`` -> ``1``
* ``110`` -> ``1`` (``110`` rounded to ``100``)
* ``190`` -> ``2`` (``190`` rounded to ``200``)
* ``200`` -> ``2``
* ``300`` -> ``3``
* ...


Device Profile
--------------

Example of a range_choice value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "sensitivity1": {
                "label": "Sensitivity preset 1",
                "description": "Set sensitivity preset 1 (DPI)",
                "cli": ["-s", "--sensitivity1"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x03, 0x01],
                "value_type": "range_choice",
                "input_range": [200, 7200, 100],
                "output_choices": {
                    200: 0x04,
                    300: 0x06,
                    400: 0x08,
                    ...
                    7200: 0xA7,
                },
                "range_length_byte": 1,  # optional, little endian
                "default": 1000,
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    -s SENSITIVITY1, --sensitivity1 SENSITIVITY1
                          Set sensitivity preset 1 (DPI) (from 200 to 7200,
                          default: 1000)

Example of CLI usage::

    rivalcfg --sensitivity1=1000


Functions
---------
"""

from ..helpers import uint_to_little_endian_bytearray


def find_nearest_choice(choices, value):
    """Find the nearest value from choice list.

    :param list[int] choices: List of allowed values.
    :param int value: the value to match with the ones of choices.

    :rtype: int
    :returns: The nearest value from choices.
    """
    nearest_delta = None
    nearest_choice = None

    for choice in sorted(choices):
        delta = abs(choice - value)
        if nearest_delta is None or delta < nearest_delta:
            nearest_delta = delta
            nearest_choice = choice

    return nearest_choice


def process_range_choice(setting_info, value):
    """Called by the "range_choice" functions to process 'value' with the
    specified range settings in 'setting_info'.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param value: The input value.
    :rtype: int
    """

    # Checks

    _first, _last, _step = setting_info["input_range"]

    if len(setting_info["output_choices"]) != (_last - _first + _step) / _step:
        raise ValueError("Input range and output choices mismatch: not the same length")

    if min(setting_info["output_choices"].keys()) != _first:
        raise ValueError(
            "Input range and output choices mismatch: not the same min value"
        )

    if max(setting_info["output_choices"].keys()) != _last:
        raise ValueError(
            "Input range and output choices mismatch: not the same max value"
        )

    #

    matched_dpi = find_nearest_choice(setting_info["output_choices"].keys(), int(value))
    return setting_info["output_choices"][matched_dpi]


def process_value(setting_info, value):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "range" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param value: The input value.
    :rtype: list[int]
    """
    range_length = 1
    if "range_length_byte" in setting_info:
        range_length = setting_info["range_length_byte"]
    return uint_to_little_endian_bytearray(
        process_range_choice(setting_info, value), range_length
    )


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "range" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (from %i to %i, default: %i)" % (
        setting_info["description"],
        setting_info["input_range"][0],
        setting_info["input_range"][1],
        setting_info["default"],
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        help=description,
        dest=setting_name.upper(),
        type=int,
        metavar=setting_name.upper(),
    )
