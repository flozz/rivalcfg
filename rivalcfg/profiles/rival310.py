from .. import usbhid

rival310 = {
    "name": "SteelSeries Rival 310 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1720,
    "interface_number": 0,

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
            "command": [0x53, 0x00, 0x01],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int(x / 100),
            "default": 800,
        },

        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
            "command": [0x53, 0x00, 0x02],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int(x / 100),
            "default": 1600,
        },

        "set_logo_color": {
            "description": "Set the logo backlight color(s) and effects",
            "cli": ["-c", "--logo-color"],
            "command": [0x5B, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x00,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "set_wheel_color": {
            "description": "Set the wheel backlight color(s) and effects",
            "cli": ["-C", "--wheel-color"],
            "command": [0x5B, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbuniversal",
            "led_id": 0x01,
            "default": (["red", "green", "blue"], ["0", "54", "54"], "x", "x")
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x59, 0x00],
            "value_type": None,
        },

    },

}
