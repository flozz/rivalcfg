from .. import usbhid


profile = {

    "name": "SteelSeries Rival 100 / SteelSeries Rival 105",

    "models": [{
        "name": "SteelSeries Rival 100",
        "vendor_id": 0x1038,
        "product_id": 0x1702,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 100 (Dell China)",
        "vendor_id": 0x1038,
        "product_id": 0x170a,
        "endpoint": 0,
        "override_defaults": {
            "color": "#FF0000",
        },
    }, {
        "name": "SteelSeries Rival 100 Dota 2 Edition (retail)",
        "vendor_id": 0x1038,
        "product_id": 0x170b,
        "endpoint": 0,
        "override_defaults": {
            "color": "#FF0000",
        },
    }, {
        "name": "SteelSeries Rival 100 Dota 2 Edition (Lenovo)",
        "vendor_id": 0x1038,
        "product_id": 0x170c,
        "endpoint": 0,
        "override_defaults": {
            "color": "#FF0000",
        },
    }, {
        "name": "SteelSeries Rival 105",
        "vendor_id": 0x1038,
        "product_id": 0x1814,
        "endpoint": 0,
    }],

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

        "color": {
            "label": "LED color",
            "description": "Set the mouse LED color",
            "cli": ["-c", "--color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "light_effect": {
            "label": "Light effect",
            "description": "Set the light effect",
            "cli": ["-e", "--light-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x07, 0x00],
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
