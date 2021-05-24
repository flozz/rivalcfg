from .. import usbhid


profile = {
    "name": "SteelSeries Rival 95 / SteelSeries Rival 100 PC Bang",
    "models": [
        {
            "name": "SteelSeries Rival 95",
            "vendor_id": 0x1038,
            "product_id": 0x1706,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 95 MSI Edition",
            "vendor_id": 0x1038,
            "product_id": 0x1707,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 95 PC Bang",
            "vendor_id": 0x1038,
            "product_id": 0x1704,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 100 PC Bang",
            "vendor_id": 0x1038,
            "product_id": 0x1708,
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
                250: 0x08,
                500: 0x07,
                1000: 0x06,
                1250: 0x05,
                1500: 0x04,
                1750: 0x03,
                2000: 0x02,
                4000: 0x01,
            },
            "default": 1000,
        },
        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x02],
            "value_type": "choice",
            "choices": {
                250: 0x08,
                500: 0x07,
                1000: 0x06,
                1250: 0x05,
                1500: 0x04,
                1750: 0x03,
                2000: 0x02,
                4000: 0x01,
            },
            "default": 2000,
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
        "btn6_mode": {
            "label": "Button 6 mode",
            "description": "Set the mode of the button under the wheel",
            "cli": ["-b", "--btn6-mode"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x0B],
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
    },
}
