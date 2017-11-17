sensei310 = {
    "name": "SteelSeries Sensei 310 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1722,
    "interface_number": 0,

    "commands": {

        # TODO
        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
            "command": [0x53, 0x00, 0x01],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int(x / 100),
            "default": 800,
        },

        # TODO
        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
            "command": [0x53, 0x00, 0x02],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int(x / 100),
            "default": 1600,
        },

        "set_logo_light_effect": {
            "description": "Set the logo light effect",
            "cli": ["-e", "--logo-light-effect"],
            "command": [0x08, 0x02, 0x00],
            "value_type": "choice",
            "choices": {
                "steady": 0x01,
                "breathslow": 0x02,
                "breathmed": 0x03,
                "breathfast": 0x04,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
            },
            "default": "steady",
        },

        "set_wheel_light_effect": {
            "description": "Set the wheel light effect",
            "cli": ["-E", "--wheel-light-effect"],
            "command": [0x08, 0x02, 0x01],
            "value_type": "choice",
            "choices": {
                "steady": 0x01,
                "breathslow": 0x02,
                "breathmed": 0x03,
                "breathfast": 0x04,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
            },
            "default": "steady",
        },

        "set_wheel_color": {
            "description": "Set the logo backlight color",
            "cli": ["-c", "--logo-color"],
            "command": [0x07, 0x02, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF5200"
        },

        # Middle value seems ignored
        "set_logo_color": {
            "description": "Set the wheel backlight color",
            "cli": ["-C", "--wheel-color"],
            "command": [0x07, 0x02, 0x00],
            "value_type": "rgbcolor",
            "default": "#FF5200"
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x59, 0x00],
            "value_type": None,
        },

    },

}
