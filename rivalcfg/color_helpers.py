"""
This module contains varous helper functions related to color.
"""


import re


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
        color = color[0] * 2 + color[1] * 2 + color[2] * 2  # noqa

    # ff0000 -> (255, 0, 0)
    return (
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:], 16)
        )
