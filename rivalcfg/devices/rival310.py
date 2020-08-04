from .. import usbhid


_RGBGRADIENT_HEADER = {
    "header_length": 26,       # Length of the header excuding command / LED ID
    "led_id_offsets": [0],     # Offset of the "led_id" fields
    "duration_offset": 1,      # Offset of the "duration" field
    "duration_length": 2,      # Length of the "duration" field (in Bytes)
    "repeat_offset": 17,       # Offset of the "repeat" flag
    "triggers_offset": 21,     # Offset of the "triggers" field (buttons mask)
    "color_count_offset": 25,  # Offset of the "color_count" field
}

_DEFAULT_RGBGRADIENT = "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"  # noqa


profile = {

    "name": "SteelSeries Rival 310",

    "models": [{
        "name": "SteelSeries Rival 310",
        "vendor_id": 0x1038,
        "product_id": 0x1720,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 310 CS:GO Howl Edition",
        "vendor_id": 0x1038,
        "product_id": 0x171e,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 310 PUBG Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1736,
        "endpoint": 0,
    }],

    "settings": {

        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x53, 0x00, 0x01],
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
            "command": [0x53, 0x00, 0x02],
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
            "command": [0x54, 0x00],
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },

        "logo_color": {
            "label": "Logo LED colors and effects",
            "description": "Set the colors and the effects of the logo LED",
            "cli": ["-c", "--logo-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x5B, 0x00],
            "value_type": "rgbgradient",
            "rgbgradient_header": _RGBGRADIENT_HEADER,
            "led_id": 0x00,
            "default": _DEFAULT_RGBGRADIENT,
        },

        "wheel_color": {
            "label": "Wheel LED colors and effects",
            "description": "Set the colors and the effects of the wheel LED",
            "cli": ["-C", "--wheel-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x5B, 0x00],
            "value_type": "rgbgradient",
            "rgbgradient_header": _RGBGRADIENT_HEADER,
            "led_id": 0x01,
            "default": _DEFAULT_RGBGRADIENT,
        },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x59, 0x00],
    },

}
