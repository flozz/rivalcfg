from .. import usbhid


rival500 = {
    "name": "SteelSeries Rival 500 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x170e,
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

        "set_logo_color": {
            "description": "Set the logo backlight color",
            "cli": ["-c", "--logo-color"],
            "command": [0x05, 0x00, 0x00],
            "suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x00, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_wheel_color": {
            "description": "Set the wheel backlight color",
            "cli": ["-C", "--wheel-color"],
            "command": [0x05, 0x00, 0x01],
            "suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x01, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_logo_colorshift": {
            "description": "Set the logo backlight color",
            "cli": ["-t", "--logo-colorshift"],
            "command": [0x05, 0x00, 0x00],
            "suffix": [0xC8, 0xC8, 0x00, 0x00, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolorshift",
            "default": [["#FF1800", "#FF1800"], 200]
        },

        "set_wheel_colorshift": {
            "description": "Set the wheel backlight color",
            "cli": ["-T", "--wheel-colorshift"],
            "command": [0x05, 0x00, 0x01],
            "suffix": [0xC8, 0xC8, 0x00, 0x01, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolorshift",
            "default": [["#FF1800", "#FF1800"], 200]
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
