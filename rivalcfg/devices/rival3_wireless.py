from .. import usbhid


profile = {
    "name": "SteelSeries Rival 3 Wireless",
    "models": [
        {
            "name": "SteelSeries Rival 3 Wireless (2.4 GHz mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1830,
            "endpoint": 3,
        },
    ],
    "settings": {
        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x20],
            "value_type": "multidpi_range",
            "input_range": [100, 18000, 100],
            "output_range": [0x00, 0xD6, 1.2],
            "dpi_length_byte": 2,
            "first_preset": 1,
            "count_mode": "number",
            "max_preset_count": 5,
            "default": "400, 800, 1200, 2400, 3200",
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x17],
            "value_type": "choice",
            "choices": {
                125: 0x03,
                250: 0x02,
                500: 0x01,
                1000: 0x00,
            },
            "default": 1000,
        },
        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x19],
            "value_type": "buttons",
            # fmt: off
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
            # fmt: on
            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi)",
        },
    },
    "battery_level": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0xAA, 0x01],
        "response_length": 3,
        "is_charging": lambda data: bool(data[2]),
        "level": lambda data: int(data[0]),
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09],
    },
}
