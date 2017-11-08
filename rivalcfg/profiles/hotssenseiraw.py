hotssenseiraw = {
    "name": "SteelSeries Heroes of the Storm (Sensei Raw)",

    "vendor_id": 0x1038,
    "product_id": 0x1390,
    "interface_number": 0,

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
            "command": [0x03, 0x01],
            "value_type": "range",
            "range_min": 90,
            "range_max": 5400,
            "range_increment": 90,
            "value_transform": lambda x: int(x / 90),
            "default": 1530,
        },

        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
            "command": [0x03, 0x02],
            "value_type": "range",
            "range_min": 90,
            "range_max": 5400,
            "range_increment": 90,
            "value_transform": lambda x: int(x / 90),
            "default": 2520,
        },

        "set_logo_light_effect": {
            "description": "Set the logo light effect",
            "cli": ["-e", "--logo-light-effect"],
            "command": [0x07, 0x01],
            "value_type": "choice",
            "choices": {
                "steady": 0x01,
                "breathslow": 0x02,
                "breathmed": 0x03,
                "breathfast": 0x04,
                "trigger": 0x05,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
                5: 0x05,
            },
            "default": "breathmed",
        },

        "set_logo_light_brightness": {
            "description": "Set logo light brightness",
            "cli": ["-E", "--logo-light-brightness"],
            "command": [0x05, 0x01],
            "value_type": "choice",
            "choices": {
                "off": 0x01,
                "low": 0x02,
                "med": 0x03,
                "high": 0x04,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
            },
            "default": "high",
        },

        "set_mouse_btn_action": {
            "description": "Set mouse button actions",
            "cli": ["-z", "--set-btns"],
            "command": [0x31, 0x00],
            "value_type": "hotsbtnmap",
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
