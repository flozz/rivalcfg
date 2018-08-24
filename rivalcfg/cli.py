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


def _check_rgbuniversal(option, opt_str, value, parser):
    """OptionParser callback to check and process inputs for rgbuniversal.
    Accepts 2 formats:
        -x color
        -x time,triggers,color1,pos1[,...,colorn,posn]
    In both cases, it sets option.dest to a 4tuple:
        (colors, positions, time, triggers)
    Note that time and triggers can be "x" for "don't care", and gets assigned
    a default value later on.
    """
    args = value.split(",")
    if len(args) == 1:
        if not helpers.is_color(value):
            raise OptionValueError("option %s: invalid color: '%s'" % (opt_str, value))  # noqa
        setattr(parser.values, option.dest, ([value], ["0"], "x", "x"))

    elif len(args) >= 4 and len(args) & 1 == 0:
        time = args[0]
        if not (time.isdigit() or time.lower() == "x"):
            raise OptionValueError("option %s: invalid time: '%s'" % (opt_str, time))  # noqa

        triggers = args[1]
        if not (helpers.is_hex(triggers) or triggers.lower() == "x"):
            raise OptionValueError("option %s: invalid triggers: '%s'" % (opt_str, triggers))  # noqa

        colors = args[2::2]
        for color in colors:
            if not helpers.is_color(color):
                raise OptionValueError("option %s: invalid color: '%s'" % (opt_str, color))  # noqa

        positions = args[3::2]
        for position in positions:
            if not helpers.is_hex(position):
                raise OptionValueError("option %s: invalid color position: '%s'" % (opt_str, position))  # noqa

        setattr(parser.values, option.dest,
                (colors, positions, time, triggers))
    else:
        raise OptionValueError("option %s: invalid number of values" % (opt_str))  # noqa


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


def _add_rgbuniversal_option(group, command_name, command):
    description = (command["description"] +
                   " (e.g. red, #ff0000, ff0000, #f00, f00). "
                   "If more than one value is specified, "
                   "a color shifting effect is set "
                   "(e.g. x,x,red,0,green,54,blue,54) "
                   "syntax: time(ms),trigger_mask,color1,pos1,...,colorn,posn")
    group.add_option(
            *command["cli"],
            dest=command_name,
            help=description,
            type="string",
            action="callback",
            callback=_check_rgbuniversal,
            metavar=_command_name_to_metavar(command_name)
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
