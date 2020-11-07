from .. import usbhid


_RGBGRADIENT_HEADER = {
    "header_length": 26,       # Length of the header excuding command / LED ID
    "led_id_offsets": [0],     # Offset of the "led_id" fields
    "duration_offset": 1,      # Offset of the "duration" field
    "duration_length": 2,      # Length of the "duration" field (in Bytes)
    "repeat_offset": 17,       # Offset of the "repeat" flag
    "triggers_offset": 21,     # Offset of the "triggers" field (buttons mask)
    "color_count_offset": 25,  # Offset of the "color_count" field
}

_DEFAULT_RGBGRADIENT = "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"  # noqa


profile = {

    "name": "SteelSeries Sensei TEN",

    "models": [{
        "name": "SteelSeries Sensei TEN",
        "vendor_id": 0x1038,
        "product_id": 0x1832,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Sensei TEN CS:GO Neon Rider Editon",
        "vendor_id": 0x1038,
        "product_id": 0x1834,
        "endpoint": 0,
    }],

    "settings": {

        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x55, 0x00],  # <COUNT> <SELECTED> <S1> <S2> ... <S5>
            "value_type": "multidpi_range",
            "input_range": [50, 18000, 50],
            "output_range": [1, 0x0168, 1],
            "dpi_length_byte": 2,
            "count_mode": "flag",
            "max_preset_count": 5,
            "default": "800, 1600",
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

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x59, 0x00],
    },

}
