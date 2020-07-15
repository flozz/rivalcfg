"""
TODO
"""


# import argparse

from ...helpers import parse_param_string, REGEXP_PARAM_STRING
from . import layout_multimedia
from . import layout_qwerty


#: Available layouts
LAYOUTS = {
    "qwerty": layout_qwerty,
    # TODO azerty
}


# Compatibility with Python 2.7.
# On Python 2 the type is 'unicode'
# On Python 3 the type is 'str'
_unicode_type = type(u"")


def build_layout(layout):
    """Generates an usable layout from a layout module containing key mapping
    and aliases.

    :param module layout: The layour (e.g.
                          ``rivalcfg.handler.buttons.layout_qwerty``)
    :rtype dict:
    """
    full_layout = {k.lower(): v for k, v in layout.layout.items()}

    for alias, ref in layout.aliases.items():
        if ref not in layout.layout:
            raise ValueError("Wrong alias: '%s' aliases '%' but '%s' is not in the layout" % (  # noqa
                alias, ref, ref))
        full_layout[alias.lower()] = layout.layout[ref]

    return full_layout


def process_value(setting_info, mapping):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,dict mapping: The mapping of the mouse buttons.
    :rtype: [int]
    """
    # -- Parse input values

    if type(mapping) in [str, _unicode_type] and REGEXP_PARAM_STRING.match(mapping):  # noqa
        mapping = parse_param_string(mapping)
    elif type(mapping) in [str, _unicode_type] and mapping.lower() == "default":  # noqa
        mapping = {"buttons": {}}
    elif type(mapping) is dict:
        pass
    else:
        raise ValueError("Invalid input value '%s'" % str(mapping))

    # -- TODO Check input

    # -- Initialize mouse buttons

    buttons = {k.lower(): dict(v) for k, v in setting_info["buttons"].items()}

    # -- Initialise special values

    button_keyboard = setting_info["button_keyboard"]
    button_multimedia = setting_info["button_multimedia"]

    button_special = {}

    if setting_info["button_disable"] is not None:
        button_special["disable"] = setting_info["button_disable"]
        button_special["disabled"] = setting_info["button_disable"]

    if setting_info["button_dpi_switch"] is not None:
        button_special["dpi"] = setting_info["button_dpi_switch"]

    if setting_info["button_scroll_up"] is not None:
        button_special["scrollup"] = setting_info["button_scroll_up"]

    if setting_info["button_scroll_down"] is not None:
        button_special["scrolldown"] = setting_info["button_scroll_down"]
        button_special["scrolldwn"] = setting_info["button_scroll_down"]
        button_special["scrolldn"] = setting_info["button_scroll_down"]

    # -- Initialize keyboard layout

    keyboard_layout = {}
    keyboard_layout_name = "qwerty"

    if button_keyboard is not None:
        if "layout" in mapping["buttons"]:
            keyboard_layout_name = mapping["buttons"]["layout"].lower()

        if keyboard_layout_name not in LAYOUTS:
            raise ValueError("Unsupported layout '%s'" % keyboard_layout_name)

        keyboard_layout = build_layout(LAYOUTS[keyboard_layout_name])

    mm_layout = build_layout(layout_multimedia)

    # -- Craft packet

    packet_length = len(buttons) * 3
    packet = [0x00] * packet_length

    for button, value in [(k.lower(), v) for k, v in mapping["buttons"].items()]:  # noqa
        if button == "layout":
            continue
        if button not in buttons:
            raise ValueError("Unknown button name '%s'" % button)
        buttons[button]["value"] = value

    for button, data in buttons.items():
        value = data["default"]
        if "value" in data and data["value"].lower() != "default":
            value = data["value"]
        value = value.lower()

        if value in buttons:
            packet[data["offset"]] = buttons[value]["id"]
        elif value in button_special:
            packet[data["offset"]] = button_special[value]
        elif value in mm_layout:
            packet[data["offset"]] = button_multimedia
            packet[data["offset"] + 1] = mm_layout[value]
        elif value in keyboard_layout:
            packet[data["offset"]] = button_keyboard
            packet[data["offset"] + 1] = keyboard_layout[value]
        else:
            raise ValueError("Unknown button, key or action '%s'" % value)

    return packet


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "rgbgradient" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    description = "%s (default: %s)" % (
            setting_info["description"],
            str(setting_info["default"]).replace("%", "%%"),
            )
    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            # action=CheckButtonsAction,
            metavar=setting_name.upper()
            )
