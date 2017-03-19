import sys
import re
from optparse import OptionParser, OptionGroup, OptionValueError

from . import mice
from .helpers import (usb_device_is_connected, find_hidraw_device_path,
        is_color, choices_to_list, choices_to_string)
from .rival_mouse import RivalMouse
from .version import VERSION
from .debug import *


def get_plugged_mouse_profile():
    """Returns the profile of the mouse plugged on the computer."""
    if DEBUG_PROFILE_VENDOR_ID:
        for profile in mice.mice_list:
            if profile["vendor_id"] == DEBUG_PROFILE_VENDOR_ID and profile["product_id"] == DEBUG_PROFILE_PRODUCT_ID:
                return profile
    for profile in mice.mice_list:
        if not DEBUG_PROFILE_VENDOR_ID and usb_device_is_connected(profile["vendor_id"], profile["product_id"]):
            return profile


def _print_compatible_mice():
    """Prints mice currently supported by this software."""
    print("\n".join(["%-45s %s:%s   %s" % (
        profile["name"],
        profile["vendor_id"],
        profile["product_id"],
        "(plugged)" if usb_device_is_connected(profile["vendor_id"], profile["product_id"]) else ""
        ) for profile in mice.mice_list]))


def _check_color(option, opt_str, value, parser):
    """OptionParser callback to check if the given color is valid."""
    if not is_color(value):
        raise OptionValueError("option %s: invalid color: '%s'" % (opt_str, value))
    setattr(parser.values, option.dest, value)


def _generate_default_cli_options(parser):
    """Add common cli options"""
    parser.add_option("-l", "--list",
        help="print compatible mice and exit",
        action="store_true"
        )

def _command_name_to_metavar(command_name):
    """Trnansforms a command name to a better metaname (used for -h)."""
    return command_name.replace("set_", "").upper()


def _generate_mouse_cli_options(parser, profile):
    """generate CLI specific to the plugged mouse."""
    group = OptionGroup(parser, "%s Options" % profile["name"])
    commands = sorted(profile["commands"].keys());
    for command in commands:
        cmd = profile["commands"][command]
        if not cmd["cli"]:
            continue
        if cmd["value_type"] == "choice":
            description = "%s (values: %s, default: %s)" % (
                    cmd["description"],
                    choices_to_string(cmd["choices"]),
                    str(cmd["default"])
                    )
            group.add_option(
                    *cmd["cli"],
                    help=description,
                    dest=command,
                    choices=choices_to_list(cmd["choices"]),
                    metavar=_command_name_to_metavar(command)
                    )
        elif cmd["value_type"] == "rgbcolor":
            description = "%s (e.g. red, #ff0000, ff0000, #f00, f00, default: %s)" % (
                    cmd["description"],
                    str(cmd["default"])
                    )
            group.add_option(
                    *cmd["cli"],
                    dest=command,
                    help=description,
                    type="string",
                    action="callback",
                    callback=_check_color,
                    metavar=_command_name_to_metavar(command)
                    )
        elif cmd["value_type"] == "range":
            description = "%s (from %i to %i in increments of %i, default: %i)" % (
                    cmd["description"],
                    cmd["range_min"],
                    cmd["range_max"],
                    cmd["range_increment"],
                    cmd["default"]
                    )
            group.add_option(
                    *cmd["cli"],
                    dest=command,
                    help=description,
                    metavar=_command_name_to_metavar(command),
                    choices=[str(i) for i in range(cmd["range_min"], cmd["range_max"] + 1, cmd["range_increment"])]
                    )
        else:
            raise NotImplementedError("Cannot generate CLI option for value_type '%s'" % cmd["value_type"])
    group.add_option("-r", "--reset",
            help="Reset all options to their factory values",
            action="store_true"
            )
    parser.add_option_group(group)


def main():
    """Run rivalcfg's CLI"""
    # Find the plugged mouse's profile
    profile = get_plugged_mouse_profile()

    # Debug infos
    if DEBUG:
        print("[DEBUG] Debugging rivalcfg %s..." % VERSION)
        print("[DEBUG] Python %i.%i.%i" % (
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
            ))
    if DEBUG_DRY:
        print("[DEBUG] Dry run enabled")

    if DEBUG_PROFILE_PRODUCT_ID:
        print("[DEBUG] Debugging mouse profile %s:%s" % (DEBUG_PROFILE_VENDOR_ID, DEBUG_PROFILE_PRODUCT_ID))
    if DEBUG and profile:
        print("[DEBUG] Mouse profile found: %s" % profile["name"])
    if DEBUG and not profile:
        print("[DEBUG] No mouse profile found")

    if DEBUG_DEVICE_PRODUCT_ID:
        print("[DEBUG] Debugging mouse device %s:%s" % (DEBUG_DEVICE_VENDOR_ID, DEBUG_DEVICE_PRODUCT_ID))

    # Generates CLI options
    parser = OptionParser("Usage: rivalcfg [options]",
            version=VERSION,
            epilog="Please report any bug on Github: https://github.com/flozz/rivalcfg/issues"
            )
    _generate_default_cli_options(parser);
    if profile:
        _generate_mouse_cli_options(parser, profile)

    options, args = parser.parse_args();

    # Mouse indep commands
    if options.list:
        _print_compatible_mice()
        sys.exit(0)

    # Check everything is ok
    if not profile:
        print("E: No compatible mouse found. Type 'rivalcfg --help' for more informations.")
        sys.exit(1);

    if not DEBUG and not find_hidraw_device_path(profile["vendor_id"], profile["product_id"], profile["hidraw_interface_number"]):
        print("E: The '%s' mouse is plugged in but the control interface is not available." % profile["name"])
        print("\nTry to:")
        print("  * unplug the mouse from the USB port,")
        print("  * wait fiew seconds,")
        print("  * and plug the mouse to the USB port again.")
        sys.exit(1)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    # Configure the mouse
    mouse = RivalMouse(profile)

    if profile["command_before"]:
        getattr(mouse, profile["command_before"])()

    if hasattr(options, "reset") and options.reset:
        mouse.set_default()

    for option, value in list(options.__dict__.items()):
        if option in ["list", "reset"] or value == None:
            continue
        if profile["commands"][option]["value_type"] in ["choice", "range"] and value.isdigit():
            value = int(value)
        getattr(mouse, option)(value)

    if profile["command_after"]:
        getattr(mouse, profile["command_after"])()

