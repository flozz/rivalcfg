import sys
from optparse import OptionParser, OptionGroup

from helpers import usb_device_is_connected, find_hidraw_device_path
from mice import mice_list
from rival_mouse import RivalMouse
from version import VERSION

def get_plugged_mouse_profile():
    """Returns the profile of the mouse plugged on the computer."""
    for profile in mice_list:
        if usb_device_is_connected(profile["vendor_id"], profile["product_id"]):
            return profile

def print_compatible_mice():
    """Prints mice currently supported by this software."""
    print("\n".join([profile["name"] for profile in mice_list]))

def print_software_version():
    """Prints the software version."""
    print("rivalcfg %s" % VERSION)

def _generate_default_cli_options(parser):
    parser.add_option("-l", "--list",
        help="print the mice compatible with this software",
        action="store_true"
        )
    parser.add_option("-v", "--version",
        help="print the rivalcfg version and exit",
        action="store_true"
        )

def _generate_mouse_cli_options(parser, profile):
    group = OptionGroup(parser, "%s Options" % profile["name"])
    # TODO
    parser.add_option_group(group)

def main():
    # Find the plugged mouse's profile
    profile = get_plugged_mouse_profile()

    # Generates CLI options
    parser = OptionParser("Usage: rivalcfg [options]")
    _generate_default_cli_options(parser);
    if profile:
        _generate_mouse_cli_options(parser, profile)

    options, args = parser.parse_args();

    # Check everything is ok
    if not profile:
        print("E: No compatible mouse found. Type 'rivalcfg --help' for more informations.")
        sys.exit(1);

    if not find_hidraw_device_path(profile["vendor_id"], profile["product_id"], profile["hidraw_interface_number"]):
        print("E: The '%s' mouse is plugged in but the control interface is not available." % profile["name"])
        print("\nTry to:")
        print("  * unplug the mouse from the USB port,")
        print("  * wait fiew seconds,")
        print("  * and plug the mouse to the USB port again.")
        sys.exit(1)

    # Configure the mouse
    mouse = RivalMouse(profile)

    for option, value in options.__dict__.items():
        if option == "list" and value:
            print_compatible_mice()
            sys.exit(0)
        elif option == "version" and value:
            print_software_version()
            sys.exit(0)
        else:
            pass  # TODO
