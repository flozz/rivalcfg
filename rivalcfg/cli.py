"""
This module generates rivalcfg's CLI.
"""


import os
import sys
import types
import platform
import argparse

from . import handlers
from . import devices
from . import udev
from . import debug
from .version import VERSION


def normalize_cli_option_name(name):
    """Helper function to transform a setting name to a cli option.

    :param str name: The setting name.
    :rtype: str

    >>> normalize_cli_option_name("My_Test_Setting1")
    'my-test-setting1'
    """
    return name.lower().replace("_", "-")


class PrintSupportedDevicesAction(argparse.Action):
    """Print supported devices and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        for item in [getattr(devices, name) for name in dir(devices)]:
            if not isinstance(item, types.ModuleType):
                continue
            if not hasattr(item, "profile"):
                continue
            print("%s:" % item.profile["name"])
            print()
            for model in item.profile["models"]:
                print(
                    "  %04x:%04x | %s"
                    % (
                        model["vendor_id"],
                        model["product_id"],
                        model["name"],
                    )
                )
            print()
        sys.exit(0)


class UpdateUdevRulesAction(argparse.Action):
    """Updates udev rules and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        if platform.system() != "Linux":
            print("E: The --update-udev option can only be used on Linux.")
            sys.exit(2)
        if os.getuid() != 0:
            print("E: You must run rivalcfg as root to use the --update-udev option.")
            sys.exit(2)
        udev.write_rules_file()
        udev.reload_rules()
        udev.trigger()
        sys.exit(0)


class PrintUdevRulesAction(argparse.Action):
    """Prints udev rules and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        print(udev.generate_rules())
        sys.exit(0)


class PrintDebugAction(argparse.Action):
    """Prints debug informations and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        print(debug.get_debug_info())
        sys.exit(0)


def add_main_cli(cli_parser):
    """Adds the main CLI options.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    """
    cli_parser.add_argument(
        "--list",
        help="List supported devices and exit",
        nargs=0,
        action=PrintSupportedDevicesAction,
    )

    cli_parser.add_argument(
        "--version",
        action="version",
        version=VERSION,
    )

    cli_parser.add_argument(
        "--no-save",
        help="Do not persist settings in the internal device memory",
        dest="SAVE",
        action="store_false",
        default=True,
    )

    cli_parser.add_argument(
        "--update-udev",
        help="Updates udev rules (Linux only, requires to be run as root)",
        nargs=0,
        action=UpdateUdevRulesAction,
    )

    cli_parser.add_argument(
        "--print-udev",
        help="Prints udev rules and exit",
        nargs=0,
        action=PrintUdevRulesAction,
    )

    cli_parser.add_argument(
        "--print-debug",
        help="Prints debug informations and exit",
        nargs=0,
        action=PrintDebugAction,
    )


def add_mouse_cli(cli_parser, mouse_profile):
    """Adds the CLI options for the given mouse profile.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param mouse_profile: One of the rivalcfg mouse profile (provided by
                            :func:`rivalcfg.devices.get_profile`).
    """
    cli_group = cli_parser.add_argument_group("%s Options" % mouse_profile["name"])

    for setting_name, setting_info in mouse_profile["settings"].items():
        handler = getattr(handlers, setting_info["value_type"])
        handler.add_cli_option(cli_group, setting_name, setting_info)

    cli_group.add_argument(
        "-r",
        "--reset",
        help="Reset all settings to their factory default",
        dest="RESET",
        action="store_true",
    )

    if "firmware_version" in mouse_profile:
        cli_group.add_argument(
            "--firmware-version",
            help="Print the firmware version of the mouse and exit",
            dest="FIRMWARE_VERSION",
            action="store_true",
        )

    if "battery_level" in mouse_profile:
        cli_group.add_argument(
            "--battery-level",
            help="Print the battery level of the mouse and exit",
            dest="BATTERY_LEVEL",
            action="store_true",
        )
