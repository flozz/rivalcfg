"""
The "range" type alows to pick a value in an input range and transforms it into
a value from an output range. If the input value do not correspond to one of
the input range step, it is rounded to match the nearest step.

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

Example of a range value type in a device profile:

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
                "value_type": "range",
                "input_range": [200, 7200, 100],
                "output_range": [0x04, 0xA7, 2],
                "range_length_byte": 1,  # optional
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


def matches_value_in_range(range_start, range_stop, range_step, value):
    """Helper function that matches the value with the nearest value in the
    given range.

    :param int range_start: The start of the range.
    :param int range_stop: The end of the range.
    :param int range_step: The gap between two value in the range.
    :param int value: The value to process.

    :rtype: int

    >>> matches_value_in_range(0, 100, 10, 40)
    40
    >>> matches_value_in_range(0, 100, 10, 42)
    40
    >>> matches_value_in_range(0, 1000, 100, 51)
    100
    >>> matches_value_in_range(42, 1000, 100, 150)
    142
    >>> matches_value_in_range(500, 1000, 100, 100)
    500
    >>> matches_value_in_range(500, 1000, 100, 4000)
    1000
    """
    if value <= range_start:
        return range_start

    if value >= range_stop:
        return range_stop

    delta = (value - range_start) % range_step
    if not delta:
        return value
    else:
        if delta < range_step / 2:
            return value - delta
        else:
            return value - delta + range_step


def custom_range(start, stop, step):
    """Helper function that generates a range of integers but allowing to have
    a float as step.

    I am not very proud of this but the Rival 110 requires a step of ~2.33...

    :param int start: The start of the range.
    :param int stop: The end of the range.
    :param float step: The gap between two value in the range.

    :rtype: generator(int)

    >>> list(custom_range(4, 168, 2.33))
    [4, 6, 8, 10, 13, 15, ...160, 162, 164, 167]
    """
    i = start
    while i < stop:
        yield int(i)
        i += step


def process_range(setting_info, value):
    """Called by the "range" functions to process 'value' with the specified
    range settings in 'setting_info'.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param value: The input value.
    :rtype: int
    """
    input_range = list(
        range(
            setting_info["input_range"][0],
            setting_info["input_range"][1] + 1,
            setting_info["input_range"][2],
        )
    )
    output_range = list(
        custom_range(
            setting_info["output_range"][0],
            setting_info["output_range"][1] + 1,
            setting_info["output_range"][2],
        )
    )

    if len(input_range) != len(output_range):
        raise ValueError("Input range and output range must have the same length")

    matched_value = matches_value_in_range(
        setting_info["input_range"][0],
        setting_info["input_range"][1],
        setting_info["input_range"][2],
        int(value),
    )
    return output_range[input_range.index(matched_value)]


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
        process_range(setting_info, value), range_length
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
