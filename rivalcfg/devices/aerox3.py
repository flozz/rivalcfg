from .. import usbhid


profile = {
    "name": "SteelSeries Aerox 3",
    "models": [
        {
            "name": "SteelSeries Aerox 3",
            "vendor_id": 0x1038,
            "product_id": 0x1836,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Aerox 3 Wireless (wired mode)",
            "vendor_id": 0x1038,
            "product_id": 0x183a,
            "endpoint": 0,
        },
    ],
    "settings": {
        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2d],
            "value_type": "multidpi_range",
            "input_range": [200, 8500, 100],
            "output_range": [0x04, 0xC5, 2.33],
            "dpi_length_byte": 1,
            "count_mode": "number",
            "max_preset_count": 5,
            "default": "800, 1600",
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2b],
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },
        # TODO: Followed instructions for the Aerox 3 Wireless (wired mode) here.
        # TODO: We need to confirm it works with the non-wireless Aerox 3 too!
        "z1_color": {
            "label": "Strip top LED color",
            "description": "Set the color of the top LED",
            "cli": ["--top-color", "--z1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x21, 0x01, 0x00],
            "value_type": "rgbcolor",
            "default": "red",
        },
        "z2_color": {
            "label": "Strip middle LED color",
            "description": "Set the color of the middle LED",
            "cli": ["--middle-color", "--z2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x21, 0x02, 0x00],
            "value_type": "rgbcolor",
            "default": "lime",
        },
        "z3_color": {
            "label": "Strip bottom LED color",
            "description": "Set the color of the bottom LED",
            "cli": ["--bottom-color", "--z3"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x21, 0x03, 0x00],
            "value_type": "rgbcolor",
            "default": "blue",
        },
        # XXX
        "led_brightness": {
            "label": "LED Brightness",
            "description": "Set the brightness of the LEDs",
            "cli": ["-l", "--led-brightness"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x23, 0x01],
            "value_type": "range",
            "input_range": [0, 100, 1],
            "output_range": [0x00, 0x64, 1],
            "default": 100,
        },
    },
    # TODO We must check that later
    # "save_command": {
    #     "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
    #     "command": [0x11, 0x00],
    # },
}
