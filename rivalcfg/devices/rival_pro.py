from .dpi import truemove_42k_pro
from .. import usbhid

# Polling rate codes, shared by the polling rate and low power mode settings
_POLLING_RATES = {
    125: 0x06,
    250: 0x05,
    500: 0x04,
    1000: 0x03,
    2000: 0x02,
    4000: 0x01,
    8000: 0x00,
}

# Low power mode activation threshold (battery %), not configurable yet
_LOW_POWER_THRESHOLD = 5


def _parse_firmware_version(data):
    # 90 00 "2.14.2" 00 00 ...
    return [int(n) for n in bytes(data[2:]).split(b"\0")[0].split(b".")]


profile = {
    "name": "SteelSeries Rival Pro",
    "models": [
        {
            "name": "SteelSeries Rival Pro",
            "vendor_id": 0x1038,
            "product_id": 0x1880,
            "endpoint": 2,
        },
    ],
    "settings": {
        # 0x34 <COUNT> <SELECTED> (<X:u16> <Y:u16> <LIFT-OFF> <LANDING>)*COUNT
        # Lift-off and landing distances: (mm - 0.7) * 10, 0x03 = 1.0 mm
        "sensitivity": {
            "label": "Sensitivity presets",
            "description": "Set sensitivity presets (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x34],
            "value_type": "multidpi_range_choice_xy",
            "input_range": [1, 65000, 1],
            "output_choices": truemove_42k_pro.choices,
            "xy_mapping": "xyxy",
            "dpi_length_byte": 2,
            "preset_suffix": [0x03, 0x03],
            "first_preset": 0,
            "max_preset_count": 5,
            "default": "400, 800, 1600, 2400, 3200",
        },
        # 0x2D <COUNT> <SELECTED> (<SENSOR_RATE> <UWB_RATE>)*COUNT
        # Only one polling rate level is configured, with the same sensor and
        # UWB rates.
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2D, 0x01, 0x00],
            "value_type": "choice",
            "choices": {rate: [code, code] for rate, code in _POLLING_RATES.items()},
            "default": 1000,
        },
        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2A],
            "value_type": "buttons",
            # fmt: off
            "buttons": {
                "Button1":    {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2":    {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3":    {"id": 0x03, "offset": 0x0A, "default": "button3"},
                "Button4":    {"id": 0x04, "offset": 0x0F, "default": "button4"},
                "Button5":    {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6":    {"id": 0x06, "offset": 0x19, "default": "dpi"},
                "ScrollUp"  : {"id": 0x31, "offset": 0x1E, "default": "scrollup"},
                "ScrollDown": {"id": 0x32, "offset": 0x23, "default": "scrolldown"},
            },
            "button_field_length": 5,
            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   None,
            "button_scroll_down": None,
            # fmt: on
            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; scrollup=scrollup; scrolldown=scrolldown; layout=qwerty)",
        },
        "sleep_timer": {
            "label": "Sleep timer",
            "description": "Set the IDLE time before the mouse goes to sleep mode (minutes)",
            "cli": ["-t", "--sleep-timer"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x29],
            "value_type": "range",
            "input_range": [1, 20, 1],
            "output_range": [60000, 1200000, 60000],
            "range_length_byte": 3,
            "default": 5,
        },
        "click_response": {
            "label": "Click response",
            "description": "Set the click response time (debounce, ms)",
            "cli": ["--click-response"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x1C],
            "value_type": "range",
            "input_range": [0, 20, 1],
            "output_range": [0, 20, 1],
            "default": 8,
        },
        # 0x16 <ENABLED> <COOLDOWN_MS:u16>
        "scroll_jump_protection": {
            "label": "Scroll jump protection",
            "description": "Ignore the first scroll input after a cooldown period (ms)",
            "cli": ["--scroll-jump-protection"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x16],
            "value_type": "choice",
            "choices": {
                "off": [0x00, 0xF4, 0x01],
                **{ms: [0x01, ms & 0xFF, ms >> 8] for ms in range(100, 1501, 100)},
            },
            "default": "off",
        },
        "motion_sync": {
            "label": "Motion sync",
            "description": "Enable motion sync (smoother tracking for slow movements)",
            "cli": ["--motion-sync"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x18],
            "value_type": "choice",
            "choices": {
                "on": 0x01,
                "off": 0x00,
            },
            "default": "off",
        },
        "lan_mode": {
            "label": "LAN mode",
            "description": "Enable LAN mode (when multiple UWB mice are nearby, must be enabled on all mice)",
            "cli": ["--lan-mode"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x1A],
            "value_type": "choice",
            "choices": {
                "on": 0x01,
                "off": 0x00,
            },
            "default": "off",
        },
        "max_performance": {
            "label": "Max performance",
            "description": "Run the sensor in its highest performance mode all the time",
            "cli": ["--max-performance"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x1B],
            "value_type": "choice",
            "choices": {
                "on": 0x01,
                "off": 0x00,
            },
            "default": "off",
        },
        "led_indicator": {
            "label": "LED indicator",
            "description": "Set what the receiver LED indicates",
            "cli": ["--led-indicator"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x25],
            "value_type": "choice",
            "choices": {
                "polling-rate": 0x00,
                "battery": 0x01,
                "off": 0x02,
            },
            "default": "polling-rate",
        },
        # 0x19 0x00 <THRESHOLD_%> <POLLING_RATE>
        "low_power_polling_rate": {
            "label": "Low power mode polling rate",
            "description": "Set the polling rate used when the battery is low (Hz, or 'led-only' to only warn using the LED)",
            "cli": ["--low-power-polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x19, 0x00, _LOW_POWER_THRESHOLD],
            "value_type": "choice",
            "choices": {
                **{rate: code for rate, code in _POLLING_RATES.items() if rate <= 1000},
                "led-only": 0x07,
            },
            "default": 1000,
        },
    },
    # 0x92 -> 0x92 0x00 <MOUSE_%> <FLAG> <SPARE_BATTERY_%>
    "battery_level": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x92],
        "response_length": 5,
        "level": lambda data: data[2],
    },
    "firmware_version": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x90],
        "response_length": 32,
        "parse": _parse_firmware_version,
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09],
    },
}
