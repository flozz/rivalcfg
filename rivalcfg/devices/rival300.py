from .. import usbhid


profile = {

    "name": "SteelSeries Rival 300 / SteelSeries Rival",

    "models": [{
        "name": "SteelSeries Rival",
        "vendor_id": 0x1038,
        "product_id": 0x1384,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival Dota 2 Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1392,
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

        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x31, 0x00],
            "value_type": "buttons",

            "buttons": {
                "Button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2": {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3": {"id": 0x03, "offset": 0x0A, "default": "button3"},
                "Button4": {"id": 0x04, "offset": 0x0F, "default": "button4"},
                "Button5": {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6": {"id": 0x06, "offset": 0x19, "default": "dpi"},
            },

            "button_field_length": 5,

            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,

            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; layout=qwerty)",  # noqa
        },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
