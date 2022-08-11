"""
The "buttons" type handles buttons mapping on device that supports it.

Buttons syntax example::

    default
    buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; layout=qwerty)
    buttons(Button6=DPI)  # all other buttons will be reset to their default values


Buttons values
--------------

Buttons can be mapped to different kind of values:

* ``default`` (to explicitly set the button to its default value)
* Special actions,
* Mouse buttons,
* Multimedia keys,
* Keyboard keys.


Special actions
~~~~~~~~~~~~~~~

* ``disabled``: disable this button,
* ``dpi``: use this button to switch between DPI presets,
* ``ScrollUp`` (not available on all devices)
* ``ScrollDown`` (not available on all devices)

Example::

    buttons(button6=dpi; button5=disabled)


Mouse buttons
~~~~~~~~~~~~~

Mouse buttons can be remapped using an other mouse button.

For example, this swap the button 1 and 2 of the mouse::

    buttons(button1=button2; button2=button1)

.. WARNING::

    Be careful to map the ``button1`` somewhere, else you will not be able to
    click! ;)


Multimedia keys
~~~~~~~~~~~~~~~

Example::

    buttons(button8=PlayPause)

List of the available multimedia keys:

* https://github.com/flozz/rivalcfg/blob/master/rivalcfg/handlers/buttons/layout_multimedia.py


Keyboard keys
~~~~~~~~~~~~~

Keyboard keys depends on the selected layout.

Examples::

    buttons(layout=QWERTY; button2=A)

.. NOTE::

    Due to some syntax limitation, some keys cannot be mapped used their own
    symbols. For example, if you want to bind ``;`` to the third button, you
    will have to use an alias::

        buttons(layout=QWERTY; button3=semicolon)

    More examples::

        buttons(layout=QWERTY; button3=semi; button4=equal)


Layouts
-------

The layout used for mapping keyboard keys can be specified using the ``layout``
parameter::

    buttons(layout=QWERTY)

Currently, the following layouts are supported:

* ``QWERTY`` (`see available keys <https://github.com/flozz/rivalcfg/blob/master/rivalcfg/handlers/buttons/layout_qwerty.py>`_)

If not specified, the ``QWERTY`` layout is used.


Device Profile
--------------

Example of a buttons value type in a device profile:

::

    profile = {

        # ...

        "settings": {

        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x31, 0x00],
            "value_type": "buttons",

            "buttons": {
                "Button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2": {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3": {"id": 0x03, "offset": 0x0A, "default": "button3"},
                "Button4": {"id": 0x04, "offset": 0x0F, "default": "button4"},
                "Button5": {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6": {"id": 0x06, "offset": 0x19, "default": "dpi"},
            },

            "button_field_length": 5,

            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,

            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; layout=qwerty)",
        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

  -b BUTTONS_MAPPING, --buttons BUTTONS_MAPPING
                        Set the mapping of the buttons (default: buttons(button1=button1;
                        button2=button2; button3=button3; button4=button4; button5=button5;
                        button6=dpi; layout=qwerty))

Example of CLI usage::

    rivalcfg --buttons="buttons(layout=qwerty; button1=button1; button6=DPI)"


Functions
---------
"""


import argparse

from ...helpers import parse_param_string, REGEXP_PARAM_STRING
from . import layout_multimedia
from . import layout_qwerty


#: Available layouts
LAYOUTS = {
    "qwerty": layout_qwerty,
    # TODO azerty
}


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
            raise ValueError(
                "Wrong alias: '%s' aliases '%s' but '%s' is not in the layout"
                % (alias, ref, ref)
            )
        full_layout[alias.lower()] = layout.layout[ref]

    return full_layout


def is_buttons(string, setting_info):
    """Checks if the regbradient expression is valid.

    :param str string: The string to validate.
    :param dict setting_info: the settings info from the mouse profile.
    :rtype: (bool, str)
    """
    available_buttons = {k.lower(): v for k, v in setting_info["buttons"].items()}

    try:
        buttons_dict = parse_param_string(string)
    except ValueError as e:
        return False, str(e)

    if "buttons" not in buttons_dict:
        return (
            False,
            "Buttons expression must looks like buttons(<BUTTON>=<VALUE>; <BUTTON_N>=<VALUE_N>)",
        )

    for key, value in [
        (k.lower(), v.lower()) for k, v in buttons_dict["buttons"].items()
    ]:
        if key == "layout":
            if value not in LAYOUTS:
                return False, "Unknown layout '%s'" % value
        else:
            if key not in available_buttons:
                return False, "This mouse have no button named '%s'" % key

    return True, ""


def process_value(setting_info, mapping):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "buttons" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,dict mapping: The mapping of the mouse buttons.
    :rtype: [int]
    """
    # -- Parse input values

    if type(mapping) is str and REGEXP_PARAM_STRING.match(mapping):
        is_valid, reason = is_buttons(mapping, setting_info)
        if not is_valid:
            raise ValueError(reason)
        mapping = parse_param_string(mapping)
    elif type(mapping) is str and mapping.lower() == "default":
        mapping = {"buttons": {}}
    elif type(mapping) is dict:
        pass
    else:
        raise ValueError("Invalid input value '%s'" % str(mapping))

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

    packet_length = len(buttons) * setting_info["button_field_length"]
    packet = [0x00] * packet_length

    for button, value in [(k.lower(), v) for k, v in mapping["buttons"].items()]:
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


def cli_buttons_validator(setting_info):
    class CheckButtonsAction(argparse.Action):
        """Validate buttons from CLI"""

        def __call__(self, parser, namespace, value, option_string=None):
            if value.lower() == "default":
                setattr(namespace, self.dest.upper(), value)
                return

            if REGEXP_PARAM_STRING.match(value):
                is_valid, reason = is_buttons(value, setting_info)

                if is_valid:
                    setattr(namespace, self.dest.upper(), value)
                    return

                raise argparse.ArgumentError(self, "%s" % reason)

            else:
                raise argparse.ArgumentError(
                    self, "not a valid buttons mapping param: '%s'" % value
                )

    return CheckButtonsAction


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "buttons" type setting to the given CLI arguments parser.

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
        action=cli_buttons_validator(setting_info),
        metavar=setting_name.upper(),
    )
