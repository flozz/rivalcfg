from .. import usbhid


profile = {

    "name": "SteelSeries Sensei [RAW]",

    "models": [{
        "name": "SteelSeries Sensei [RAW]",
        "vendor_id": 0x1038,
        "product_id": 0x1369,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei [RAW] Diablo III Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1362,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei [RAW] Guild Wars 2 Edition",
        "vendor_id": 0x1038,
        "product_id": 0x136d,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei [RAW] CoD Black Ops II Edition",
        "vendor_id": 0x1038,
        "product_id": 0x136f,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei [RAW] World of Tanks Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1380,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei [RAW] Heroes of the Storm Edition",
        "vendor_id": 0x1038,
        "product_id": 0x1390,
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
            "input_range": [90, 5670, 90],
            "output_range": [0x01, 0x3F, 1],
            "default": 1620,
        },

        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x02],
            "value_type": "range",
            "input_range": [90, 5670, 90],
            "output_range": [0x01, 0x3F, 1],
            "default": 3240,
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

        "led_brightness": {
            "label": "LED Brightness",
            "description": "Set the brightness of the LEDs",
            "cli": ["-l", "--led-brightness"],
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

        "light_effect": {
            "label": "Light effect",
            "description": "Set the light effect",
            "cli": ["-e", "--light-effect"],
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
                "trigger": 0x05,
            },
            "default": "breath",
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
                "Button2": {"id": 0x02, "offset": 0x03, "default": "button2"},
                "Button3": {"id": 0x03, "offset": 0x06, "default": "button3"},
                "Button4": {"id": 0x04, "offset": 0x09, "default": "button4"},
                "Button5": {"id": 0x05, "offset": 0x0c, "default": "button5"},
                "Button6": {"id": 0x06, "offset": 0x12, "default": "PageDown"},
                "Button7": {"id": 0x07, "offset": 0x0f, "default": "PageUp"},
                "Button8": {"id": 0x08, "offset": 0x15, "default": "dpi"},
            },

            "button_field_length": 3,

            "button_disable":     0x00,
            "button_keyboard":    0x10,
            "button_multimedia":  0x11,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   None,
            "button_scroll_down": None,

            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=PageDown; button7=PageUp; button8=dpi; layout=qwerty)",  # noqa
        },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
