from .. import usbhid


# fmt: off
_RGBGRADIENT_HEADER = {
    "header_length": 26,       # Length of the header excuding command / LED ID
    "led_id_offsets": [0],     # Offset of the "led_id" fields
    "duration_offset": 1,      # Offset of the "duration" field
    "duration_length": 2,      # Length of the "duration" field (in Bytes)
    "repeat_offset": 17,       # Offset of the "repeat" flag
    "triggers_offset": 21,     # Offset of the "triggers" field (buttons mask)
    "color_count_offset": 25,  # Offset of the "color_count" field
}
# fmt: on

_DEFAULT_RGBGRADIENT = (
    "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
)


profile = {
    "name": "SteelSeries Rival 310",
    "models": [
        {
            "name": "SteelSeries Rival 310",
            "vendor_id": 0x1038,
            "product_id": 0x1720,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 310 CS:GO Howl Edition",
            "vendor_id": 0x1038,
            "product_id": 0x171E,
            "endpoint": 0,
        },
        {
            "name": "SteelSeries Rival 310 PUBG Edition",
            "vendor_id": 0x1038,
            "product_id": 0x1736,
            "endpoint": 0,
        },
    ],
    "settings": {
        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x53, 0x00, 0x01],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 800,
        },
        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x53, 0x00, 0x02],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 1600,
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x54, 0x00],
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },
        "logo_color": {
            "label": "Logo LED colors and effects",
            "description": "Set the colors and the effects of the logo LED",
            "cli": ["-c", "--logo-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x5B, 0x00],
            "value_type": "rgbgradient",
            "rgbgradient_header": _RGBGRADIENT_HEADER,
            "led_id": 0x00,
            "default": _DEFAULT_RGBGRADIENT,
        },
        "wheel_color": {
            "label": "Wheel LED colors and effects",
            "description": "Set the colors and the effects of the wheel LED",
            "cli": ["-C", "--wheel-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x5B, 0x00],
            "value_type": "rgbgradient",
            "rgbgradient_header": _RGBGRADIENT_HEADER,
            "led_id": 0x01,
            "default": _DEFAULT_RGBGRADIENT,
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
                "Button2": {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3": {"id": 0x03, "offset": 0x0A, "default": "button3"},
                "Button4": {"id": 0x04, "offset": 0x0F, "default": "button4"},
                "Button5": {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6": {"id": 0x06, "offset": 0x19, "default": "dpi"},
            },
            # fmt: off
            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,
            # fmt: on
            "button_field_length": 5,
            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; layout=qwerty)",
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x59, 0x00],
    },
    "firmware_version": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x90, 0x00],
        "response_length": 2,
    },
}
