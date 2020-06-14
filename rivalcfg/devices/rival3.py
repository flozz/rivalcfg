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

        # "sensitivity": {
        #     "label": "Sensibility presets",
        #     "description": "Set sensitivity preset (DPI). You can define up to 5 presets",  # noqa
        #     "cli": ["-s", "--sensitivity"],
        #     "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        #     "command": [TODO],
        #     "value_type": "TODO",
        #     "default": 800, 1600,
        # },

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

        # "colors": {
        #     "label": "LED colors",
        #     "description": "Set the color of the mouse LEDs (format: '<COLOR>' or '<COLOR_TOP>,<COLOR_MIDDLE>,<COLOR_BOTTOM>,<COLOR_LOGO>') ",  # noqa
        #     "cli": ["-c", "--colors"],
        #     "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        #     "command": [0x0A, 0x00, 0x0F],
        #                             # ^ zone_mask ?
        #     "value_type": "TODO",
        #     "default": "#FF1800"
        # },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
