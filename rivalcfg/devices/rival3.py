from .. import usbhid


profile = {

    "name": "SteelSeries Rival 3",

    "models": [{
        "name": "SteelSeries Rival 3",
        "vendor_id": 0x1038,
        "product_id": 0x1824,
        "endpoint": 3,
    }],

    "settings": {

        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x0B, 0x00],
            "value_type": "multidpi_range",
            "input_range": [200, 8500, 100],
            "output_range": [4, 0xC5, 2.33],
            "max_preset_count": 5,
            "default": "800, 1600",
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

        # 0x05 0x00 <LED_ID> <R> <G> <B> <BRIGHTNESS>
        # LED_ID: 0x00 all
        #         0x01 zone 1 (top)
        #         0x02 zone 2 (middle)
        #         0x03 zone 3 (bottom)
        #         0x04 zone 4 / logo
        # BRIGHTNESS 0x00 - 0x64 (0 - 100%)
        "z1_color": {
            "label": "Strip top LED color",
            "description": "Set the color of the top LED of the strip",
            "cli": ["--strip-top-color", "--z1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x01],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "red"
        },

        "z2_color": {
            "label": "Strip middle LED color",
            "description": "Set the color of the middle LED of the strip",
            "cli": ["--strip-middle-color", "--z2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x02],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "lime"
        },

        "z3_color": {
            "label": "Strip bottom LED color",
            "description": "Set the color of the bottom LED of the strip",
            "cli": ["--strip-bottom-color", "--z3"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x03],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "blue"
        },

        "logo_color": {
            "label": "Logo LED color",
            "description": "Set the color of the logo LED",
            "cli": ["-c", "--logo-color", "--z4"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x04],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "purple"
        },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
