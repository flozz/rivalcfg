from .. import usbhid

# fmt: off
_RGBGRADIENTV2_HEADER = {
    "color_field_length": 139,  # Index of length of color field (used for padding)
    "duration_length": 2,       # Length of the "duration" field (in bytes)
    "maxgradient": 14,          # Max numbers of color stop (probably 14)
}
# fmt: on

_DEFAULT_RGBGRADIENTV2 = (
    "rgbgradient(duration=1000; colors=0%: #ff00e1, 33%: #ffea00, 66%: #00ccff)"
)

profile = {
    "name": "SteelSeries Rival 700 / SteelSeries Rival 710",
    "models": [
        {
            "name": "SteelSeries Rival 700",
            "vendor_id": 0x1038,
            "product_id": 0x1700,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 710",
            "vendor_id": 0x1038,
            "product_id": 0x1730,
            "endpoint": 0,
        },
    ],
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
        "logo_color": {
            "label": "Logo LED colors and effects",
            "description": "Set the logo colors and effects",
            "cli": ["-c", "--logo-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbgradientv2",
            "rgbgradientv2_header": _RGBGRADIENTV2_HEADER,
            "led_id": 0x0,
            "default": _DEFAULT_RGBGRADIENTV2,
        },
        "wheel_color": {
            "label": "Wheel LED colors and effects",
            "description": "Set the wheel colors and effects",
            "cli": ["-C", "--wheel-color"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rgbgradientv2",
            "rgbgradientv2_header": _RGBGRADIENTV2_HEADER,
            "led_id": 0x1,
            "default": _DEFAULT_RGBGRADIENTV2,
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },
    "firmware_version": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x10, 0x00],
        "response_length": 2,
    },
}
