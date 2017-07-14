from __future__ import print_function
import sys
import platform

from . import cli
from . import debug
from .version import VERSION
from . import list_supported_mice, list_available_mice, get_mouse


def get_first_available_mouse():
    available_mice = list(list_available_mice())
    if not available_mice:
        return None
    mouse = available_mice[0]
    try:
        return get_mouse(
                mouse.vendor_id,
                mouse.product_id
                )
    except IOError as error:
        print("W: The following mouse was found but rivalcfg was not able to open it:")  # noqa
        print("  * mouse: %s (%4X:%4X)" % mouse)
        print("  * error: %s" % error)
        print("\nPlease check that no other application is controlling this mouse and try to:")  # noqa
        print("  * unplug the mouse from the USB port,")
        print("  * wait few seconds,")
        print("  * and plug the mouse to the USB port again.\n")
        return None


def _print_debug_info():
    debug.log("Rivalcfg %s" % VERSION)
    debug.log("Python version: %s" % platform.python_version())
    debug.log("OS: %s" % platform.system())
    if platform.system() == "Linux":
        debug.log("Linux distribution: %s" % " ".join(platform.linux_distribution()))  # noqa
    if debug.DRY:
        debug.log("Dry run enabled")
    if debug.get_debug_profile():
        debug.log("Forced profile: %04X:%04X" % debug.get_debug_profile())
        debug.log("Targeted device: %04X:%04X" % debug.get_debug_device())


def _print_compatible_mice():
    """Prints mice currently supported by this software."""
    print("\n".join(["%-50s %04X:%04X   %s" % (
            mouse.name,
            mouse.vendor_id,
            mouse.product_id,
            "(plugged)" if mouse in list_available_mice() else ""
        ) for mouse in list_supported_mice()]))


def main(argv=sys.argv[1:]):
    _print_debug_info()

    mouse = get_first_available_mouse()
    debug.log("Selected mouse: %s" % mouse)

    profile = mouse.profile if mouse else None
    parser = cli.generate_cli(profile)
    options, args = parser.parse_args(argv)

    if len(argv) == 0:
        parser.print_help()
        sys.exit(1)

    # Standard options

    if options.list:
        _print_compatible_mice()
        sys.exit(0)

    # Mouse specific options

    if not mouse:
        print("Error: no compatible mouse found.")
        sys.exit(1)

    if hasattr(options, "reset") and options.reset:
        mouse.set_default()

    for option, value in list(options.__dict__.items()):
        if option in ["list", "reset"] or value is None:
            continue
        if (profile["commands"][option]["value_type"] in ["choice", "range"]
                and value.isdigit()):
            value = int(value)
        if not type(value) in (list, tuple):
            value = [value]
        getattr(mouse, option)(*value)

    if hasattr(mouse, "save"):
        mouse.save()


if __name__ == "__main__":
    main(sys.argv[1:])
