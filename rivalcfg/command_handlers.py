from . import helpers


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
    if not choice in command["choices"]:
        raise ValueError("value must be one of [%s]" %
                helpers.choices_to_string(command["choices"]))
    value = command["choices"][choice]
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], value)


def rgbcolor_handler(command, *args):
    """Returns command bytes from RGB color commands.

    Arguments:
    command -- the command description dict
    *args -- the color as a string (color name or hexadecimal RGB), or as R, G
             and B int (e.g. fn(cmd, "red"), fn(cmd, "#ff0000"), fn(cmd, 255, 0, 0))
    """
    color = (0x00, 0x00, 0x00)
    if len(args) == 3:
        for value in args:
            if type(value) != int or value < 0 or value > 255:
                raise ValueError("Not a valid color")
        color = args
    elif len(args) == 1 and type(args[0]) == str and helpers.is_color(args[0]):
        color = helpers.color_string_to_rgb(args[0])
    else:
        raise ValueError("Not a valid color")
    color = _transform(command, *color)
    return helpers.merge_bytes(command["command"], color)


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
    if "range_increment" in command and value % command["range_increment"] != 0:
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

