from .. import usbhid

profile = {

    "name": "SteelSeries Rival 700",

    "models": [{
        "name": "SteelSeries Rival 700",
        "vendor_id": 0x1038,
        "product_id": 0x1700,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 710",
        "vendor_id": 0x1038,
        "product_id": 0x1730,
        "endpoint": 0,
    }],

    "settings": {

        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x00, 0x01],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 800,
        },

        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x00, 0x02],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 1600,
        },

        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
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

        "wheel_color": {
            "label": "Wheel LED colors and effects",
            "description": "Set the colors and the effects of the wheel LED",
            "cli": ["-C", "--wheel-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x00],
            "command_suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x00, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "logo_color": {
            "label": "Logo LED colors and effects",
            "description": "Set the colors and the effects of the logo LED",
            "cli": ["-c", "--logo-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x01],
            "command_suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x01, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_logo_trigger": {
            "description": "Set the wheel backlight color",
            "cli": ["-t", "--logo-trigger"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x00],
            "command_suffix": [0xc8, 0x00, 0x00, 0x08, 0x00],
            "value_type": "multi_rgbcolor",
            "color_count": 2,
            "default": [["#FF1800", "#FF1800"], 200]
        },

        "set_wheel_trigger": {
            "description": "Set the wheel backlight color",
            "cli": ["-T", "--wheel-trigger"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x01],
            "command_suffix": [0xc8, 0x00, 0x00, 0x08, 0x00],
            "value_type": "multi_rgbcolor",
            "color_count": 2,
            "default": [["#FF1800", "#FF1800"], 200]
        },
    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
