from optparse import OptionParser, OptionGroup, OptionValueError

from . import helpers
from .version import VERSION


def _command_name_to_metavar(command_name):
    """Transforms a command name to a better metaname (used for -h)."""
    return command_name.replace("set_", "").upper()


def _check_color(option, opt_str, value, parser):
    """OptionParser callback to check if the given color is valid."""
    if not helpers.is_color(value):
        raise OptionValueError("option %s: invalid color: '%s'" % (opt_str, value))  # noqa
    setattr(parser.values, option.dest, value)


def _check_colorshift(option, opt_str, values, parser):
    """OptionParser callback to check if the given colors are valid.
    Also transfroms a little bit the args to make it works:
    [color1, color2, speed] -> [[color1, color2], speed]
    """
    colors = values[:-1]
    speed = values[-1]
    for color in colors:
        if not helpers.is_color(color):
            raise OptionValueError("option %s: invalid color: '%s'" % (opt_str, color))  # noqa
    if not speed.isdigit():
        raise OptionValueError("option %s: invalid speed: '%s'" % (opt_str, speed))  # noqa
    setattr(parser.values, option.dest, [colors, int(speed)])


def _add_choice_option(group, command_name, command):
    description = "%s (values: %s, default: %s)" % (
            command["description"],
            helpers.choices_to_string(command["choices"]),
            str(command["default"])
            )
    group.add_option(
            *command["cli"],
            help=description,
            dest=command_name,
            choices=helpers.choices_to_list(command["choices"]),
            metavar=_command_name_to_metavar(command_name)
            )


def _add_rgbcolor_option(group, command_name, command):
    description = "%s (e.g. red, #ff0000, ff0000, #f00, f00, default: %s)" % (
            command["description"],
            str(command["default"])
            )
    group.add_option(
            *command["cli"],
            dest=command_name,
            help=description,
            type="string",
            action="callback",
            callback=_check_color,
            metavar=_command_name_to_metavar(command_name)
            )


def _add_rgbcolorshift_option(group, command_name, command):
    description = "%s (e.g. red aqua 200, ff0000 00ffff 200, default: %s %s)" % (  # noqa
            command["description"],
            " ".join(command["default"][0]),
            " ".join((str(v) for v in command["default"][1:]))
            )
    group.add_option(
            *command["cli"],
            dest=command_name,
            help=description,
            type="string",
            action="callback",
            callback=_check_colorshift,
            nargs=3,
            metavar="COLOR1 COLOR2 SPEED"
            )


def _add_range_option(group, command_name, command):
    description = "%s (from %i to %i in increments of %i, default: %i)" % (
            command["description"],
            command["range_min"],
            command["range_max"],
            command["range_increment"],
            command["default"]
            )
    group.add_option(
            *command["cli"],
            dest=command_name,
            help=description,
            metavar=_command_name_to_metavar(command_name),
            choices=[str(i) for i in range(
                command["range_min"],
                command["range_max"] + 1,
                command["range_increment"])]
            )


def _add_hotsbtnmap_option(group, command_name, command):
    description = command["description"]
    group.add_option(
            *command["cli"],
            dest=command_name,
            help=description,
            metavar=_command_name_to_metavar(command_name)
            )


def _add_standard_options(parser):
    parser.add_option(
            "-l", "--list",
            help="print compatible mice and exit",
            action="store_true"
            )


def _add_mouse_options(parser, profile):
    group = OptionGroup(parser, "%s Options" % profile["name"])
    command_names = sorted(profile["commands"].keys())
    for command_name in command_names:
        if command_name == "save":
            continue
        command = profile["commands"][command_name]
        adder_name = "_add_%s_option" % command["value_type"]
        if adder_name not in globals():
            raise Exception("Unable to create a CLI option for value type '%s'" % command["value_type"])  # noqa
        globals()[adder_name](group, command_name, command)
    group.add_option(
            "-r", "--reset",
            help="Reset all options to their factory values",
            action="store_true"
            )
    parser.add_option_group(group)


def generate_cli(profile=None):
    parser = OptionParser(
            "Usage: rivalcfg [options]",
            version=VERSION,
            epilog="Please report any bug on Github: https://github.com/flozz/rivalcfg/issues"  # noqa
            )
    _add_standard_options(parser)
    if profile:
        _add_mouse_options(parser, profile)
    return parser
