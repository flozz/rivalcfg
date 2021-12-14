from .. import usbhid


profile = {
    "name": "SteelSeries Rival 3 Wireless",
    "models": [
        {
            "name": "SteelSeries Aerox 3 Wireless (wired mode)",
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
    },
    # "save_command": {
        # "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        # "command": [0x11, 0x00],
    # },
}
