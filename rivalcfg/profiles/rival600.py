from .. import usbhid


rival600 = {
    "name": "SteelSeries Rival 600 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1724,
    "interface_number": 0,

    "rgbuniversal_format": {
        "header_len": 28,   # Number of bytes in header excluding command bytes
        "led_id": [0, 5],   # Index(es) of LED ID (unsure why rival600 have 2)
        "speed": 6,         # Index of the colorshift speed field
        "speed_len": 2,     # How many bytes the speed field takes up
        "repeat": 22,       # Index of the repeat flag
        "triggers": 23,     # Index of the trigger button mask field
        "point_count": 27,  # Index of the color count field
    },

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
            "description": "Set the wheel backlight color(s) and effects",
            "cli": ["-C", "--wheel-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x0,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_logo_color": {
            "description": "Set the logo backlight color(s) and effects",
            "cli": ["-c", "--logo-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x1,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_left_strip_top_color": {
            "description": "Set the color(s) and effects of the left LED strip upper section", # noqa
            "cli": ["-0", "--lstrip-top-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x2,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_left_strip_mid_color": {
            "description": "Set the color(s) and effects of the left LED strip middle section", # noqa
            "cli": ["-1", "--lstrip-mid-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x4,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_left_strip_bottom_color": {
            "description": "Set the color(s) and effects of the left LED strip bottom section", # noqa
            "cli": ["-2", "--lstrip-bottom-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x6,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_right_strip_top_color": {
            "description": "Set the color(s) and effects of the right LED strip upper section", # noqa
            "cli": ["-3", "--rstrip-top-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x3,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_right_strip_mid_color": {
            "description": "Set the color(s) and effects of the right LED strip mid section", # noqa
            "cli": ["-4", "--rstrip-mid-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x5,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_right_strip_bottom_color": {
            "description": "Set the color(s) and effects of the right LED strip bottom section", # noqa
            "cli": ["-5", "--rstrip-bottom-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x7,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },
    }
}
