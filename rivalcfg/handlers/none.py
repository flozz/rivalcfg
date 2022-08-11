"""
The "none" type is used for command with no arguments.


Device Profile
--------------

Example of a "none" value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "rainbow_effect": {
                "label": "rainbow effect",
                "description": "Enable the rainbow effect (can be disabled by setting a color)",
                "cli": ["-e", "--rainbow-effect"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x22, 0xFF],
                "value_type": "none",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

    -e, --rainbow-effect  Enable the rainbow effect (can be disabled by setting
                          a color)

Example of CLI usage::

    rivalcfg --rainbow-effect


Functions
---------
"""


def process_value(setting_info, *args):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "none" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :rtype: list[]
    """
    return []


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "none" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    cli_parser.add_argument(
        *setting_info["cli"],
        help=setting_info["description"],
        action="store_const",
        const=True,
    )
