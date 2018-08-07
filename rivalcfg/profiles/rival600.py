from .. import usbhid

# TODO: the color transform functions are ugly and lacking R&D

""" Function: solid_color_transformer
Replicates solid color commands of official tool:
      led            led                                               solid          length
|cmd--|^^|unkown1----|^^|speed|unknown2---------------------------------|^^|unknown3---|^^|color---|--clr1--|p1|--clr2--|p2|
|05:00:04:2d:00:b4:00:04:10:27:00:00:00:00:00:00:00:00:00:00:00:00:00:00:01:00:00:00:00:02:ff:4d:00:ff:4d:00:00:ff:4d:00:ff|
      |partial-------------------------------------------------------------------------|this function----------------------|

This function should not be called outside of make_transform()
"""
def solid_color_transformer(partial):
    def transform(r, g, b):
        length = [0x02]
        color = [r, g, b]
        color_chain = color + color + [0x0] + color + [0xff]
        return partial + length + color_chain
    return transform

""" Function: make_transform
Arguments:
    led   (int)         : The led id to change color.
    solid (boolean)     : Wether it should be a solid color or color shifting.
    aux_builder (fn(x)) : A function which returns a "value_transform"-compliant 
                        : fn, for completing the partial data made by this fn.
    speed               : The rate of change when using color shift.
    u1..3               : Data segments of unknown meaning. Needs more R&D.
"""
def make_transform(led, solid, aux_builder, speed=[0x10, 0x27], u1=[0]*4, \
                    u2=[0]*14, u3=[0]*4):
    solid = [1] if solid else [0]
    led = [led]
    partial = led + u1 + led + speed + u2 + solid + u3
    return aux_builder(partial)

rival600 = {
    "name": "SteelSeries Rival 600 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1724,
    "interface_number": 0,

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
            "command": [0x03, 0x00, 0x01],
            "suffix": [0x00, 0x42],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int((x / 100) - 1),
            "default": 800,
        },
        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
            "command": [0x03, 0x00, 0x02],
            "suffix": [0x00, 0x42],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int((x / 100) - 1),
            "default": 1600,
        },

        "set_polling_rate": {
            "description": "Set polling rate in Hz",
            "cli": ["-p", "--polling-rate"],
            "command": [0x04, 0x00],
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },

        "set_wheel_color": {
            "description": "Set the wheel backlight color",
            "cli": ["-C", "--wheel-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(0, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_logo_color": {
            "description": "Set the logo backlight color",
            "cli": ["-c", "--logo-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(1, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_left_strip_top_color": {
            "description": "Set the color of the left LED strip upper section",
            "cli": ["-0", "--lstrip-top-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(2, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_left_strip_mid_color": {
            "description": "Set the color of the left LED strip middle section",
            "cli": ["-1", "--lstrip-mid-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(4, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_left_strip_bottom_color": {
            "description": "Set the color of the left LED strip bottom section",
            "cli": ["-2", "--lstrip-bottom-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(6, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_right_strip_top_color": {
            "description": "Set the color of the right LED strip upper section",
            "cli": ["-3", "--rstrip-top-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(3, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_right_strip_mid_color": {
            "description": "Set the color of the right LED strip mid section",
            "cli": ["-4", "--rstrip-mid-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(5, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "set_right_strip_bottom_color": {
            "description": "Set the color of the right LED strip bottom section",
            "cli": ["-5", "--rstrip-bottom-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbcolor",
            "value_transform": make_transform(7, True, solid_color_transformer),
            "default": "#FF5200"
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },
    }
}
