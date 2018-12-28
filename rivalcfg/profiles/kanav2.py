kanav2 = {
    "name": "SteelSeries Kana V2",

    "vendor_id": 0x1038,
    "product_id": 0x137a,
    "interface_number": 0,

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
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

        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
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

        "set_polling_rate": {
            "description": "Set polling rate in Hz",
            "cli": ["-p", "--polling-rate"],
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

        "set_led_intensity1": {
            "description": "Set LED intensity preset 1",
            "cli": ["-i", "--intensity1"],
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

        "set_led_intensity2": {
            "description": "Set LED intensity preset 2",
            "cli": ["-I", "--intensity2"],
            "command": [0x05, 0x02],
            "value_type": "choice",
            "choices": {
                "off": 0x01,
                "low": 0x02,
                "medium": 0x03,
                "high": 0x04,
            },
            "default": "high",
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
