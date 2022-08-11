"""
The "choice" type alows to pick a value from a list and to match it with a
corresponding value in a dict.


Device Profile
--------------

Example of a choice value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "light_effect": {
                "label": "Light effect",
                "description": "Set the light effect",
                "cli": ["-e", "--light-effect"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x07, 0x00],
                "value_type": "choice",
                "choices": {
                    "steady": 0x01,
                    "breath": 0x03,
                    1: 0x01,
                    2: 0x02,
                    3: 0x03,
                    4: 0x04,
                },
                "default": "steady",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    -e LIGHT_EFFECT, --light-effect=LIGHT_EFFECT
                        Set the light effect (values: steady, breath, 1, 2, 3,
                        4, default: steady)

Example of CLI usage::

    rivalcfg --light-effet=steady


Functions
---------
"""


def choices_to_list(choices):
    """Helper function that transforms choices dict to an ordered string list.
    Numeric values are sorted and placed after string values.

    :param dict choices: The dict containing available choices.
    :rtype: list[str]

    >>> choices_to_list({0: 0, 1: 1, 2: 2, "foo": 2})
    ['foo', '0', '1', '2']
    """
    return list(
        map(
            str,
            sorted(choices.keys(), key=lambda v: v if type(v) == int else -1),
        )
    )


def choices_to_string(choices):
    """Helper function that transforms choices dict to a printable string.

    :param dict choices: The dict containing available choices.
    :rtype: str

    >>> choices_to_string({0: 0, 1: 1, 2: 2, "foo": 2})
    'foo, 0, 1, 2'
    """
    return ", ".join(choices_to_list(choices))


def process_value(setting_info, choice):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "choice" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param choice: The selected choice.
    :rtype: list[int]
    """
    choices = {str(k): v for k, v in setting_info["choices"].items()}
    choice = str(choice)
    if choice not in choices:
        raise ValueError(
            "value must be one of [%s]" % choices_to_string(setting_info["choices"])
        )
    value = choices[choice]
    return [value]


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "choice" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (values: %s, default: %s)" % (
        setting_info["description"],
        choices_to_string(setting_info["choices"]),
        str(setting_info["default"]),
    )
    cli_parser.add_argument(
        *setting_info["cli"],
        help=description,
        dest=setting_name.upper(),
        choices=choices_to_list(setting_info["choices"]),
        metavar=setting_name.upper(),
    )
