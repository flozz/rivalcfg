from .. import usbhid


profile = {

    "name": "SteelSeries Rival 300 / SteelSeries Rival",

    "models": [{
        "name": "SteelSeries Rival",
        "vendor_id": 0x1038,
        "product_id": 0x1384,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300",
        "vendor_id": 0x1038,
        "product_id": 0x1710,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 Fallout 4 Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1712,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 Evil Geniuses Edition",
        "vendor_id": 0x1038,
        "product_id": 0x171c,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 CS:GO Fade Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1394,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 CS:GO Hyper Beast Edition",
        "vendor_id": 0x1038,
        "product_id": 0x171a,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 CS:GO Fade Edition (stm32)",
        "vendor_id": 0x1038,
        "product_id": 0x1716,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 Acer Predator Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1714,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 300 HP OMEN Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1718,
        "endpoint": 0,
    }],

    "settings": {

        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x01],
            "value_type": "range",
            "input_range": [50, 6500, 50],
            "output_range": [0x01, 0x82, 1],
            "default": 800,
        },

        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x02],
            "value_type": "range",
            "input_range": [50, 6500, 50],
            "output_range": [0x01, 0x82, 1],
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
            "label": "Logo LED color",
            "description": "Set the color of the logo LED",
            "cli": ["-c", "--logo-color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x08, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "wheel_color": {
            "label": "Wheel LED color",
            "description": "Set the color of the wheel LED",
            "cli": ["-C", "--wheel-color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x08, 0x02],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "logo_light_effect": {
            "label": "Logo light effect",
            "description": "Set the light effect of the logo",
            "cli": ["-e", "--logo-light-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x07, 0x01],
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

        "wheel_light_effect": {
            "label": "Wheel light effect",
            "description": "Set the light effect of the wheel",
            "cli": ["-E", "--wheel-light-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x07, 0x02],
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

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
