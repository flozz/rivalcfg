from .. import usbhid


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
            "command": [0x55, 0x00, 0x1F],  # <SELECTED> <S1> <S2> ... <S5>
            "value_type": "multidpi_range",
            # "input_range": [200, 8500, 100],
            # "output_range": [4, 0xC5, 2.33],
            "dpi_length_byte": 2,
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

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x59, 0x00],
    },

}
