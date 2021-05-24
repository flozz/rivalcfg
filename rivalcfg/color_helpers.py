"""
This module contains varous helper functions related to color.
"""


import re


# fmt: off
NAMED_COLORS = {
    "white":   (0xFF, 0xFF, 0xFF),
    "silver":  (0xC0, 0xC0, 0xC0),
    "gray":    (0x80, 0x80, 0x80),
    "black":   (0x00, 0x00, 0x00),
    "red":     (0xFF, 0x00, 0x00),
    "maroon":  (0x80, 0x00, 0x00),
    "yellow":  (0xFF, 0xFF, 0x00),
    "olive":   (0x80, 0x80, 0x00),
    "lime":    (0x00, 0xFF, 0x00),
    "green":   (0x00, 0x80, 0x00),
    "aqua":    (0x00, 0xFF, 0xFF),
    "teal":    (0x00, 0x80, 0x80),
    "blue":    (0x00, 0x00, 0xFF),
    "navy":    (0x00, 0x00, 0x80),
    "fuchsia": (0xFF, 0x00, 0xFF),
    "purple":  (0x80, 0x00, 0x80),
}
# fmt: on


def is_color(string):
    """Checks if the given string is a valid color.

    :param str string: The string to check.
    :rtype: bool

    >>> from rivalcfg.color_helpers import is_color
    >>> is_color("#FF0000") # hexadecimal colors are supported
    True
    >>> is_color("#F00")  # short format allowed
    True
    >>> is_color("FF0000")  # "#" is optionnal
    True
    >>> is_color("#ff0000")  # case insensitive
    True
    >>> is_color("#FF00")  # not a valid color
    False
    >>> is_color("red")  # named color are supported
    True
    >>> is_color("RED")  # named color are case insensitive
    True
    >>> is_color("hello")  # not a valid color name
    False
    """
    if string.lower() in NAMED_COLORS:
        return True
    if re.match(r"^#?[0-9a-f]{3}([0-9a-f]{3})?$", string, re.IGNORECASE):
        return True
    return False


def parse_color_string(color):
    """Converts a color string into an RGB tuple.

    :param str color: The string to convert.
    :return: (r, g, b)

    >>> from rivalcfg.color_helpers import parse_color_string
    >>> parse_color_string("#FF0000") # hexadecimal colors are supported
    (255, 0, 0)
    >>> parse_color_string("#F00")  # short format allowed
    (255, 0, 0)
    >>> parse_color_string("FF0000")  # "#" is optionnal
    (255, 0, 0)
    >>> parse_color_string("#ff0000")  # case insensitive
    (255, 0, 0)
    >>> parse_color_string("red")  # named color are supported
    (255, 0, 0)
    >>> parse_color_string("RED")  # named color are case insensitive
    (255, 0, 0)
    """
    # Named color
    if color.lower() in NAMED_COLORS:
        return NAMED_COLORS[color.lower()]

    # #f00 or #ff0000 -> f00 or ff0000
    if color.startswith("#"):
        color = color[1:]

    # f00 -> ff0000
    if len(color) == 3:
        color = color[0] * 2 + color[1] * 2 + color[2] * 2

    # ff0000 -> (255, 0, 0)
    return (
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:], 16),
    )


def parse_color_gradient_string(gradient):
    """Parse a color gradient string.

    :param str gradient: The gradient string.
    :rtype: list

    >>> parse_color_gradient_string("0%: red, 33%: #00ff00, 66: 00f")
    [{'pos': 0, 'color': (255, 0, 0)}, {'pos': 33, 'color': (0, 255, 0)}, {'pos': 66, 'color': (0, 0, 255)}]
    >>> parse_color_gradient_string("-1%: red")
    Traceback (most recent call last):
        ...
    ValueError: invalid color stop position '-1%'
    >>> parse_color_gradient_string("150: red")
    Traceback (most recent call last):
        ...
    ValueError: invalid color stop position '150%'
    >>> parse_color_gradient_string("42%: hello")
    Traceback (most recent call last):
        ...
    ValueError: invalid color 'hello'
    >>> parse_color_gradient_string("hello")
    Traceback (most recent call last):
        ...
    ValueError: invalid color gradient 'hello'. ...
    """
    gradient = gradient.replace(" ", "").replace("%", "")

    if not re.match(r"[0-9-]+:[a-zA-Z0-9#]+(,[0-9]+:[a-zA-Z0-9#]+)*", gradient):
        raise ValueError(
            "invalid color gradient '%s'. It must looks like '<POS1>:<COLOR1>,<POS2>:<COLOR2>,...'"
            % gradient
        )

    result = []
    for pos, color in [s.split(":") for s in gradient.split(",")]:
        pos = int(pos)

        if not 0 <= pos <= 100:
            raise ValueError("invalid color stop position '%i%%'" % pos)

        if not is_color(color):
            raise ValueError("invalid color '%s'" % color)

        result.append(
            {
                "pos": pos,
                "color": parse_color_string(color),
            }
        )

    return result
