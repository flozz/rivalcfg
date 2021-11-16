from .. import usbhid


profile = {
    "name": "SteelSeries Rival 3",
    "models": [
        {
            "name": "SteelSeries Rival 3",
            "vendor_id": 0x1038,
            "product_id": 0x1824,
            "endpoint": 3,
        },
        {
            "name": "SteelSeries Rival 3 (firmware v0.37.0.0)",
            "vendor_id": 0x1038,
            "product_id": 0x184C,
            "endpoint": 3,
        },
    ],
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
            "dpi_length_byte": 1,
            "first_preset": 1,
            "count_mode": "number",
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
            "default": "red",
        },
        "z2_color": {
            "label": "Strip middle LED color",
            "description": "Set the color of the middle LED of the strip",
            "cli": ["--strip-middle-color", "--z2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x02],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "lime",
        },
        "z3_color": {
            "label": "Strip bottom LED color",
            "description": "Set the color of the bottom LED of the strip",
            "cli": ["--strip-bottom-color", "--z3"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x03],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "blue",
        },
        "logo_color": {
            "label": "Logo LED color",
            "description": "Set the color of the logo LED",
            "cli": ["-c", "--logo-color", "--z4"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x05, 0x00, 0x04],
            "command_suffix": [0x64],
            "value_type": "rgbcolor",
            "default": "purple",
        },
        "light_effect": {
            "label": "Light effect",
            "description": "Set the light effect",
            "cli": ["-e", "--light-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x06, 0x00],
            "value_type": "choice",
            "choices": {
                "rainbow-shift": 0x00,
                "breath-fast": 0x01,
                "breath": 0x02,
                "breath-slow": 0x03,
                "steady": 0x04,
                "rainbow-breath": 0x05,
                "disco": 0x06,
            },
            "default": "steady",
        },
        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x07, 0x00],
            "value_type": "buttons",
            # fmt: off
            "buttons": {
                "Button1":    {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2":    {"id": 0x02, "offset": 0x02, "default": "button2"},
                "Button3":    {"id": 0x03, "offset": 0x04, "default": "button3"},
                "Button4":    {"id": 0x04, "offset": 0x06, "default": "button4"},
                "Button5":    {"id": 0x05, "offset": 0x08, "default": "button5"},
                "Button6":    {"id": 0x06, "offset": 0x0A, "default": "dpi"},
                "ScrollUp":   {"id": 0x31, "offset": 0x0C, "default": "scrollup"},
                "ScrollDown": {"id": 0x32, "offset": 0x0E, "default": "scrolldown"},
            },
            "button_disable":     0x00,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,
            "button_keyboard":    0x33,
            "button_multimedia":  0x34,
            # fmt: on
            "button_field_length": 2,
            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; scrollup=scrollup; scrolldown=scrolldown; layout=qwerty)",
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },
    "firmware_version": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x10, 0x00],
        "response_length": 2,
    },
}
