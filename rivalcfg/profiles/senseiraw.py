senseiraw = {
    "name": "SteelSeries Sensei RAW (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1369,
    "interface_number": 0,

    "commands": {

        "set_logo_light_effect": {
            "description": "Set the logo light effect",
            "cli": ["-e", "--logo-light-effect"],
            "command": [0x07, 0x01],
            "value_type": "choice",
            "choices": {
                "steady": 0x01,
                "breath": 0x03,
                "off": 0x05,
                0: 0x00,
                1: 0x01,
                2: 0x02,
                3: 0x03,
                4: 0x04,
                5: 0x05,
            },
            "default": "steady",
        },

    },

}
