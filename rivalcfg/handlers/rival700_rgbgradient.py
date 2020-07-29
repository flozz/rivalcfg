"""
The "rgbgradient" type handles RGB color gradients. Simple RGB color can also
be used.

RGB gradient syntax example::

    rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)
    rgbgradient(colors=0%: red, 33%: lime, 66%: blue)

It supports both hexadecimal colors:

* ``#FF0000``
* ``FF0000``
* ``#F00``
* ``F00``

and named colors:

+------------+------------+-----------+-------------+
| ``white``  | ``red``    | ``lime``  | ``blue``    |
+------------+------------+-----------+-------------+
| ``silver`` | ``maroon`` | ``green`` | ``navy``    |
+------------+------------+-----------+-------------+
| ``gray``   | ``yellow`` | ``aqua``  | ``fuchsia`` |
+------------+------------+-----------+-------------+
| ``black``  | ``olive``  | ``teal``  | ``purple``  |
+------------+------------+-----------+-------------+

----

A Python ``dict`` can also be used (Python API only)::

    {
        "duration": 1000,  # ms
        "colors": [
            {"pos": 0, "color": "red"},
            {"pos": 33, "color": "#00FF00"},
            {"pos": 66, "color": (0, 0, 255)},
        ]
    }

.. NOTE::

   A maximum of 14 color stops can be defined in a gradient.


Device Profile
--------------

Example of a rgbgradient value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "logo_color": {
                "label": "Logo LED colors and effects",
                "description": "Set the colors and the effects of the logo LED",
                "cli": ["-c", "--logo-color"],
                "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
                "command": [0x05, 0x00],
                "value_type": "rgbgradient",
                "rgbgradient_header": {
                    "header_length": 28,       # Length of the header excuding command / LED ID
                    "led_id_offsets": [0, 5],  # Offset of the "led_id" fields
                    "duration_offset": 6,      # Offset of the "duration" field
                    "duration_length": 2,      # Length of the "duration" field (in Bytes)
                    "repeat_offset": 22,       # Offset of the "repeat" flag
                    "triggers_offset": 23,     # Offset of the "triggers" field (buttons mask)
                    "color_count_offset": 27,  # Offset of the "color_count" field
                },
                "led_id": 0x01,
                "default": "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            },

        },

        # ...

    }


CLI
---

Example of CLI option generated with this handler::

   -c LOGO_COLOR, --logo-color LOGO_COLOR
                         Set the colors and the effects of the logo LED (default:
                         rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff))

Example of CLI usage::

    rivalcfg --logo-color="rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
    rivalcfg --logo-color=red
    rivalcfg --logo-color=FF1800


Functions
---------
"""  # noqa


from ..helpers import uint_to_little_endian_bytearray, merge_bytes
from ..helpers import bytes_to_high_low_nibbles, nibbles_to_byte
from ..color_helpers import is_color
from .rgbgradient import _handle_color_tuple, _handle_color_string
from .rgbgradient import _handle_rgbgradient_dict, _handle_rgbgradient_string
from .rgbgradient import is_rgbgradient, CheckGradientAction


# Compatibility with Python 2.7.
# On Python 2 the type is 'unicode'
# On Python 3 the type is 'str'
_unicode_type = type(u"")

_default_duration = 1000


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    color_field_length = setting_info["rival700_rgbgradient_header"]["color_field_length"] # noqa
    duration_length = setting_info["rival700_rgbgradient_header"]["duration_length"]       # noqa
    maxgradient = setting_info["rival700_rgbgradient_header"]["maxgradient"]               # noqa
    duration = _default_duration
    gradient = []

    # Color tuple
    if type(colors) in (tuple, list):
        gradient = _handle_color_tuple(colors)

    # Simple color string
    elif type(colors) in [str, _unicode_type] and is_color(colors):
        gradient = _handle_color_string(colors)

    # Color gradient as dict
    elif type(colors) is dict:
        duration, gradient = _handle_rgbgradient_dict(colors)

    # Color gradient as string
    elif is_rgbgradient(colors)[0]:
        duration, gradient = _handle_rgbgradient_string(colors)
    else:
        raise ValueError("Not a valid color or rgbgradient %s" % str(colors))

    # -- Check

    if len(gradient) == 0:
        raise ValueError("no color: %s" % str(colors))

    # Sse allowes a maximun of 14 rgbgradient patterns but there is room in the
    # command for up to 16 rgbgradient patterns and it will take 16 arguments.
    gradient_length = len(gradient)
    if gradient_length > maxgradient:
        raise ValueError("a maximum of %i color stops are allowed" %
                         (maxgradient))

    # Sse limits minimum duration depening the the amount of gradient arguments
    minimum_duration = -(-(gradient_length * 33.3) // 1)
    if duration < minimum_duration:
        raise ValueError("a duration of %i or above is need for %i gradient" %
                         (minimum_duration, gradient_length))

    # See allows a max duration of 30.00 sec
    if duration > 30000:
        raise ValueError("a maximum duration of 30000ms is allowed")

    # -- Generate header

    start_header = [0x1d, 0x01, 0x02, 0x31, 0x51, 0xff, 0xc8, 0x00]
    #              [0xff, 0x3c, 0x00, 0xff, 0x32, 0xc8, 0xc8, 0x00]
    # [WIP] header command
    header = merge_bytes(setting_info["led_id"], start_header)

    # 8 bytes in a stage, first byte is index, 2nd is padding,
    # 3-5 is signed bytes depecting color increase/decrease, 6 bytes
    # is padding, the 7-8 is time since last stage in ms
    # Process colors and positions in shift array, appending each stage
    # to the previous one

    last_real_pos = gradient[0]["pos"]
    start_color = gradient[0]["color"]
    del gradient[0]

    index = 0
    stage = []
    oldcolor = list(start_color)
    for pos, color in [(item["pos"], item["color"]) for item in gradient]:
        if pos <= last_real_pos:
            raise ValueError("Incorrect order for gradient or duplicate order found please check position order") # noqa
        stage.append(index)  # Stage index number
        stage.append(00)  # Padding
        time = int((duration / 100) * (pos - last_real_pos))
        last_real_pos = pos
        if time == 0:
            raise ValueError("Incompatble timings set, please set different timings") # noqa
        rgb_index = 0
        for rgb in color:
            diff = rgb - oldcolor[rgb_index]
            ramp = int(diff / time * 16)
            oldcolor[rgb_index] = rgb
            stage = merge_bytes(stage, ramp & 255)
            rgb_index = rgb_index + 1
        stage.append(00)  # Padding
        time = uint_to_little_endian_bytearray(time, 2)
        stage = merge_bytes(stage, time)
        index = index + 1

    header = merge_bytes(header, stage)
    # Pad the rest of the command so we can place start color, end suffix and
    # cycle time at the correct offset in the command

    padding = [0] * (color_field_length - len(header))
    header = merge_bytes(header, padding)

    # Split start color into high low nibbles
    split_color = []
    for i in range(len(start_color)):
        high, low = bytes_to_high_low_nibbles(start_color[i])
        left_byte = nibbles_to_byte(low, 00)
        right_byte = high & 0x0F
        split_color.append(left_byte)
        split_color.append(right_byte)

    end_suffix = [0xff, 0x00]
    # Need to fully test these values
    focal_x = uint_to_little_endian_bytearray(1500, 2)
    focal_y = uint_to_little_endian_bytearray(650, 2)
    end_suffix2 = [0x00, 0x00, 0x00, 0x00, 0x01, 0x00]
    # Amount of colors in gradient (command still work if value is incorrect)
    num_color = uint_to_little_endian_bytearray(gradient_length - 1, 2)
    duration = uint_to_little_endian_bytearray(duration, duration_length)
    suffix = merge_bytes(split_color, end_suffix, focal_x, focal_y, 
                         end_suffix2, num_color, duration)

    return merge_bytes(header, suffix)


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
            action=CheckGradientAction,
            metavar=setting_name.upper()
            )
