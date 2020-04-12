rival95 = {
    "name": "SteelSeries Rival 95 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1706,
    "interface_number": 0,

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
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

        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
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

        "set_btn6_action": {
            "description": "Set the action of the button under the wheel",
            "cli": ["-b", "--btn6-action"],
            "command": [0x0B],
            "value_type": "choice",
            "choices": {
                "default": 0x00,
                "os": 0x01,
            },
            "default": "default",
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
