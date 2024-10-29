from .. import usbhid


_BATTERY_CHARGING_FLAG = 0b10000000


profile = {
    "name": "SteelSeries Aerox 9 Wireless",
    "models": [
        {
            "name": "SteelSeries Aerox 9 Wireless (wired mode)",
            "vendor_id": 0x1038,
            "product_id": 0x185A,
            "endpoint": 3,
        },
        {
            "name": "SteelSeries Aerox 9 Wireless WOW Edition (wired mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1876,
            "endpoint": 3,
        },
    ],
    "settings": {
        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2D],
            "value_type": "multidpi_range",
            "input_range": [100, 18000, 100],
            "output_range": [0x00, 0xD6, 1.2],
            "dpi_length_byte": 1,
            "first_preset": 0,
            "count_mode": "number",
            "max_preset_count": 5,
            "default": "400, 800, 1200, 2400, 3200",
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2B],
            "value_type": "choice",
            "choices": {
                125: 0x03,
                250: 0x02,
                500: 0x01,
                1000: 0x00,
            },
            "default": 1000,
        },
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
            "command": [0x21, 0x01, 0x01],
            "value_type": "rgbcolor",
            "default": "lime",
        },
        "z3_color": {
            "label": "Strip bottom LED color",
            "description": "Set the color of the bottom LED",
            "cli": ["--bottom-color", "--z3"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x21, 0x01, 0x02],
            "value_type": "rgbcolor",
            "default": "blue",
        },
        "reactive_color": {
            "label": "Reactive color",
            "description": "Set the color of the LEDs in reaction to a button click",
            "cli": ["-a", "--reactive-color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x26],
            "value_type": "reactive_rgbcolor",
            "default": "off",
        },
        "sleep_timer": {
            "label": "Sleep timer",
            "description": "Set the IDLE time before the mouse goes to sleep mode (minutes, 0 = disable)",
            "cli": ["-t", "--sleep-timer"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x29],
            "value_type": "range",
            "input_range": [0, 20, 1],
            "output_range": [0x000000, 0x124F80, 60000],
            "range_length_byte": 3,
            "default": 5,
        },
        "dim_timer": {
            "label": "Dim timer",
            "description": "Set the IDLE time before the mouse light is dimmed (seconds, 0 = disable)",
            "cli": ["-T", "--dim-timer"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x23, 0x0F, 0x01, 0x00, 0x00],
            "value_type": "range",
            "input_range": [0, 1200, 1],
            "output_range": [0x000000, 0x124F80, 1000],
            "range_length_byte": 3,
            "default": 30,
        },
        "rainbow_effect": {
            "label": "rainbow effect",
            "description": "Enable the rainbow effect (can be disabled by setting a color)",
            "cli": ["-e", "--rainbow-effect"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x22, 0xFF],
            "value_type": "none",
        },
        "default_lighting": {
            "label": "Default lighting",
            "description": "Set default lighting at mouse startup",
            "cli": ["-d", "--default-lighting"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x27],
            "value_type": "choice",
            "choices": {
                "off": [0x00, 0x00],
                "reactive": [0x00, 0x01],
                "rainbow": [0x01, 0x00],
                "reactive-rainbow": [0x01, 0x01],
            },
            "default": "rainbow",
        },
    },
    "battery_level": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x92],
        "response_length": 2,
        "is_charging": lambda data: bool(data[1] & _BATTERY_CHARGING_FLAG),
        "level": lambda data: ((data[1] & ~_BATTERY_CHARGING_FLAG) - 1) * 5,
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x11, 0x00],
    },
}
