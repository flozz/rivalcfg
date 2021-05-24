from .. import usbhid


# This mouse requires a minimal packet length of 9 Bytes to work, but we set it
# to 32 Bytes as this is the default with the SSE3 on Windows.
_PACKET_LENGTH = 32


profile = {
    "name": "SteelSeries Rival 110 / SteelSeries Rival 106",
    "models": [
        {
            "name": "SteelSeries Rival 110",
            "vendor_id": 0x1038,
            "product_id": 0x1729,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 106",
            "vendor_id": 0x1038,
            "product_id": 0x1816,
            "endpoint": 0,
        },
    ],
    "settings": {
        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x01],
            "packet_length": _PACKET_LENGTH,
            "value_type": "range",
            "input_range": [200, 7200, 100],
            "output_range": [0x04, 0xA7, 2.33],
            "default": 800,
        },
        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x02],
            "packet_length": _PACKET_LENGTH,
            "value_type": "range",
            "input_range": [200, 7200, 100],
            "output_range": [0x04, 0xA7, 2.33],
            "default": 1600,
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x04, 0x00],
            "packet_length": _PACKET_LENGTH,
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },
        "color": {
            "label": "LED color",
            "description": "Set the mouse LED color",
            "cli": ["-c", "--color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00],
            "packet_length": _PACKET_LENGTH,
            "value_type": "rgbcolor",
            "default": "#FF1800",
        },
        "light_effect": {
            "label": "Light effect",
            "description": "Set the light effect",
            "cli": ["-e", "--light-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x07, 0x00],
            "packet_length": _PACKET_LENGTH,
            "value_type": "choice",
            "choices": {
                "steady": 0x01,
                "breath": 0x03,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
            },
            "default": "steady",
        },
        "btn6_mode": {
            "label": "Button 6 mode",
            "description": "Set the mode of the button under the wheel",
            "cli": ["-b", "--btn6-mode"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x0B],
            "packet_length": _PACKET_LENGTH,
            "value_type": "choice",
            "choices": {
                "dpi": 0x00,
                "os": 0x01,
            },
            "default": "dpi",
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
        "packet_length": _PACKET_LENGTH,
    },
}
