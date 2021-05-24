from .. import usbhid


profile = {
    "name": "SteelSeries Kana v2",
    "models": [
        {
            "name": "SteelSeries Kana v2",
            "vendor_id": 0x1038,
            "product_id": 0x137A,
            "endpoint": 0,
        }
    ],
    "settings": {
        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x01],
            "value_type": "choice",
            "choices": {
                400: 0x08,
                800: 0x07,
                1200: 0x06,
                1600: 0x05,
                2000: 0x04,
                2400: 0x03,
                3200: 0x02,
                4000: 0x01,
            },
            "default": 800,
        },
        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x02],
            "value_type": "choice",
            "choices": {
                400: 0x08,
                800: 0x07,
                1200: 0x06,
                1600: 0x05,
                2000: 0x04,
                2400: 0x03,
                3200: 0x02,
                4000: 0x01,
            },
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
        "led_brightness1": {
            "label": "LED Brightness 1",
            "description": "Set the brightness of the LEDs while sensitivity preset 1 is selected",
            "cli": ["-l", "--led-brightness1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x01],
            "value_type": "choice",
            "choices": {
                "off": 0x01,
                "low": 0x02,
                "medium": 0x03,
                "high": 0x04,
            },
            "default": "off",
        },
        "led_brightness2": {
            "label": "LED Brightness 2",
            "description": "Set the brightness of the LEDs while sensitivity preset 2 is selected",
            "cli": ["-L", "--led-brightness2"],
            "command": [0x05, 0x02],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "value_type": "choice",
            "choices": {
                "off": 0x01,
                "low": 0x02,
                "medium": 0x03,
                "high": 0x04,
            },
            "default": "high",
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },
}
