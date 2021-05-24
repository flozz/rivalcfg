from .. import usbhid


profile = {
    "name": "SteelSeries Kinzu v2",
    "models": [
        {
            "name": "SteelSeries Kinzu v2",
            "vendor_id": 0x1038,
            "product_id": 0x1366,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Kinzu v2",
            "vendor_id": 0x1038,
            "product_id": 0x1378,
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
            "value_type": "choice",
            "choices": {
                400: 0x04,
                800: 0x03,
                1600: 0x02,
                3200: 0x01,
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
                400: 0x04,
                800: 0x03,
                1600: 0x02,
                3200: 0x01,
            },
            "default": 3200,
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
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },
}
