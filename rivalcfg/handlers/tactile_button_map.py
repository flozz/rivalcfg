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
                "command": [0x59, 0x01, 0x00],
                "value_type": "unknown",
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

# Button position in command stream
BUTTON_POSITION = {
    "mouse1":           2,
    "leftclick":        2,
    "mouse2":           6,
    "rightclick":       6,
    "mouse3":           10,
    "mouse4":           14,
    "backwards":        14,
    "mouse5":           18,
    "forwards":         18,
    "mouse6":           22,
    "mouse7":           26,
    "cpi":              26,
    "cpitoggle":        26,
}


def process_value(setting_info, choices):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "frame" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    """Converts a list of buttons and feeback types to a list of command bytes.
    """
    result = [0x00] * 28
    choices = choices.split(",")
    for x in range(len(choices)):
        options = choices[x].lower()
        selection = options.split("=")
        if selection[0] in BUTTON_POSITION:
            position = BUTTON_POSITION[selection[0]]-1
            if selection[1] in NAMED_HAPTIC:
                haptic = NAMED_HAPTIC[selection[1]]
                result[position] = haptic
            else:
                raise ValueError("Invalid entry set for tactile feedback!")
        else:
            raise ValueError("Invalid entry set for mouse button")
        print("feedback command is", result)
    return (result)


def add_cli_option(cli_parser, setting_name, setting_info):

    description = "(Button 1-7 are avilable to clear a setting use feeback none, syntax: button1=softpulse,button2=lightbump...)"

    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            metavar=setting_name.upper()
            )
