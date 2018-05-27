from . import helpers
import colorsys


def _transform(command, *args):
    """Apply command's transformation function (if any) to given arguments.

    Arguments:
    command -- the command description dict
    *args -- command arguments
    """
    if "value_transform" in command:
        return command["value_transform"](*args)
    return args if len(args) > 1 else args[0]


def choice_handler(command, choice):
    """Returns command bytes from choices commands.

    Arguments:
    command -- the command description dict
    choice -- the choosen value
    """
    if choice not in command["choices"]:
        raise ValueError(
                "value must be one of [%s]" %
                helpers.choices_to_string(command["choices"]))
    value = command["choices"][choice]
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], value)


def rgbcolor_handler(command, *args):
    """Returns command bytes from RGB color commands.

    Arguments:
    command -- the command description dict
    *args -- the color as a string (color name or hexadecimal RGB), or as R, G
             and B int (e.g. fn(cmd, "red"), fn(cmd, "#ff0000"),
             fn(cmd, 255, 0, 0))
    """
    color = (0x00, 0x00, 0x00)
    if len(args) == 3:
        for value in args:
            if type(value) != int or value < 0 or value > 255:
                raise ValueError("Not a valid color %s" % str(args))
        color = args
    elif len(args) == 1 and type(args[0]) == str and helpers.is_color(args[0]):
        color = helpers.color_string_to_rgb(args[0])
    else:
        raise ValueError("Not a valid color %s" % str(args))
    color = _transform(command, *color)
    return helpers.merge_bytes(command["command"], color)


def hsvgradient_handler(command, h=0.1, s=1.0, v=255, max_h=1.0, t=0.0):
    """TODO write this.
    """
    color = [int(i) for i in colorsys.hsv_to_rgb(float(h)+(float(max_h)-float(h))*t,
                                                 float(s), float(v))]
    color = _transform(command, *color)
    return helpers.merge_bytes(command["command"], color)


def rgbcolorshift_handler(command, colors, speed=200):
    """Returns command bytes from RGB color commands.

    Arguments:
    command -- the command description dict
    colors -- the colors as an array of string (color name or hexadecimal RGB),
              or as an array of array of R, G and B int (e.g. fn(cmd, ["red"]),
              fn(cmd, ["#ff0000"]), fn(cmd, [[255, 0, 0]]))

    Keyword arguments:
    speed -- the color shift speed (default 200ms)
    """
    parsed_colors = []
    for color in colors:
        if type(color) in (list, tuple) and len(color) == 3:
            parsed_colors.extend(color)
        elif type(color) == str and helpers.is_color(color):
            parsed_colors.extend(helpers.color_string_to_rgb(color))
        else:
            raise ValueError("Not a valid color %s" % str(color))
    parsed_colors, speed = _transform(command, parsed_colors, speed)
    speed = helpers.uint_to_little_endian_bytearray(speed, 2)
    return helpers.merge_bytes(command["command"], parsed_colors, speed)


def range_handler(command, value):
    """Returns command bytes from range commands.

    Arguments:
    command -- the command description dict
    value -- the choosen value
    """
    if not command["range_min"] <= value <= command["range_max"]:
        raise ValueError("Value %i not in range [%i, %i]" % (
            value,
            command["range_min"],
            command["range_max"]
            ))
    if ("range_increment" in command
            and value % command["range_increment"] != 0):
        raise ValueError("Value %i is not a multiple of %i" % (
            value,
            command["range_increment"]
            ))
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], value)


def none_handler(command):
    """Returns command bytes for command with not arguments.

    Arguments:
    command -- the command description dict
    """
    return command["command"]


def hotsbtnmap_handler(command, value):
    """Returns command bytes for HotS button map.

    Arguments:
    command -- the command description dict
    value -- the choosen value
    """
    olist = helpers.hotsbtnmap_to_list(value)
    if len(olist) != 8:
        raise ValueError("Please provide 8 keys to be mapped.")
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], *olist)
