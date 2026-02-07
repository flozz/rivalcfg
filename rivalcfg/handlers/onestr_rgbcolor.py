"""
The "onestr_rgbcolor" type handles semicolon-separated RGB color strings.

It supports the same color formats as the "rgbcolor" handler, but allows
multiple colors in a single string, separated by ";". It also supports a
single color which is applied to all LEDs.
"""

import argparse

from ..color_helpers import is_color, parse_color_string


def _split_colors(color_string):
    parts = [part.strip() for part in str(color_string).split(";")]
    return [part for part in parts if part]


def _normalize_colors(setting_info, colors):
    led_count = setting_info.get("led_count")
    if not led_count:
        return colors

    if len(colors) == 1:
        return colors * led_count

    if len(colors) != led_count:
        raise ValueError("expected %d colors (or 1), got %d" % (led_count, len(colors)))

    return colors


def process_value(setting_info, color_string):
    """Process a semicolon-separated color string.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str color_string: The color string.
    :rtype: list[int]
    """
    colors = _split_colors(color_string)
    if not colors:
        raise ValueError("no colors provided")

    colors = _normalize_colors(setting_info, colors)

    rgb_bytes = []
    for color in colors:
        if not is_color(color):
            raise ValueError("Not a valid color %s" % str(color))
        rgb_bytes.extend(parse_color_string(color))

    return rgb_bytes


class CheckColorsAction(argparse.Action):
    """Validate multiple colors from CLI."""

    def __call__(self, parser, namespace, value, option_string=None):
        colors = _split_colors(value)
        if not colors:
            raise argparse.ArgumentError(self, "no colors provided")

        try:
            colors = _normalize_colors(self._setting_info, colors)
        except ValueError as exc:
            raise argparse.ArgumentError(self, str(exc))

        for color in colors:
            if not is_color(color):
                raise argparse.ArgumentError(self, "invalid color: '%s'" % color)

        setattr(namespace, self.dest.upper(), value)


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "onestr_rgbcolor" type setting to the given CLI parser."""
    led_count = setting_info.get("led_count")
    if led_count:
        count_hint = " (1 or %d colors)" % led_count
    else:
        count_hint = ""

    description = "%s (colors separated by ';'%s, default: %s)" % (
        setting_info["description"],
        count_hint,
        str(setting_info["default"]),
    )

    cli_parser.add_argument(
        *setting_info["cli"],
        dest=setting_name,
        help=description,
        type=str,
        action=type(
            "CheckOnestrColorsAction",
            (CheckColorsAction,),
            {"_setting_info": setting_info},
        ),
        metavar=setting_name.upper(),
    )
