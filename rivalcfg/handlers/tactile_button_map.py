"""
The "tactile" type handles feedback on the rival 700 family of mice.


Device Profile
--------------

Example of a tactile value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "feedback": {
                "label": "Feedback",
                "description": "Feedback type",
                "command": [0x92, 0x00],
                "value_type": "tactile_button_map",
            },
        },

        # ...

    }


CLI
---

tactile is a none cli command

LUA API
-------

Todo

Functions
---------
"""

from ..helpers import parse_param_string


NAMED_HAPTIC = {
    "none":                 0x00,
    "strongclick":          0x04,
    "softbump":             0x07,
    "doubleclick":          0x0a,
    "shortdoubleclick":     0x1b,
    "tripleclick":          0x03,
    "buzz":                 0x2f,
    "longbuzz":             0x0f,
    "sharptick":            0x18,
    "pulsing":              0x35,
}

# Button offset in command stream
BUTTON_OFFSETS = {
    "button1":              0x01,
    "leftclick":            0x01,
    "button2":              0x05,
    "rightclick":           0x05,
    "button3":              0x09,
    "button4":              0x0d,
    "backwards":            0x0d,
    "button5":              0x11,
    "forwards":             0x11,
    "button6":              0x15,
    "button7":              0x19,
    "cpi":                  0x19,
    "cpitoggle":            0x19,
}


def split_table(table):
    buttons = []
    feedback = []
    tact = []
    for keys, args in table.items():
        for bn, fb in args.items():
            buttons.append(bn)
            feedback.append(fb)
            tact = keys
    return tact, buttons, feedback


def is_button(string):
    if string.lower() in BUTTON_OFFSETS:
        return True


def is_feedback(string):
    if string.lower() in NAMED_HAPTIC:
        return True


def is_valid_mapping(mapping):
    tact, buttons, feedbacks = split_table(parse_param_string(mapping))
    if tact == "tactile":
        for keys in buttons:
            if not is_button(keys):
                raise ValueError("Unable to parse button type %s" % (keys))
                return False
        for keys in feedbacks:
            if not is_feedback(keys):
                raise ValueError("Unable to parse feedback type %s" % (keys))
                return False
        return True
    else:
        raise ValueError("Unable to parse key tactile")
        return False


def process_value(setting_info, mapping):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "tactile_button_map" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    """Converts a list of buttons and feeback types to a list of command bytes.
    """
    if is_valid_mapping(mapping):
        command_field = [0x00] * 28
        tact, buttons, feedbacks = split_table(parse_param_string(mapping))
        for index in range(len(buttons)):
            feedback = feedbacks[index]
            button = buttons[index]
            offset = BUTTON_OFFSETS[button]
            haptic = NAMED_HAPTIC[feedback]
            command_field[offset] = haptic
        return (command_field)


def add_cli_option(cli_parser, setting_name, setting_info):

    description = setting_info["description"] + (
                 ", Buttons 1-7 are avilable for mapping, to clear a"
                 " setting use feedback type none, syntax: "
                 "tactile(button1=strongclick; button2=shortdoubleclick)")

    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            metavar=setting_name.upper()
            )
