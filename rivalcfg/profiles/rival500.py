from .. import usbhid


rival500 = {
    "name": "SteelSeries Rival 500",

    "vendor_id": 0x1038,
    "product_id": 0x170e,
    "interface_number": 0,

    "commands": {

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

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
