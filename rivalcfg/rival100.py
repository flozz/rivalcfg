from helpers import is_color, color_string_to_rgb


VENDOR_ID = "1038"
PRODUCT_ID = "1702"


class Rival100:

    """Handle the Rival 100 gaming mouse."""

    EFFECT_STATIC = 0x01
    EFFECT_BREATH = 0x03

    BTN_ACTION_DEFAULT = 0x00
    BTN_ACTION_OS = 0x01

    def __init__(self, device_path):
        self._device = None
        self._device_path = device_path
        self._device_open()

    def set_default(self):
        """Set all option to their default values."""
        self.set_sensitivity(1, 1000)
        self.set_sensitivity(2, 2000)
        self.set_polling_rate(1000)
        self.set_color("#00ffff")
        self.set_light_effect(self.EFFECT_STATIC)
        self.set_btn6_action(self.BTN_ACTION_DEFAULT)

    def set_sensitivity(self, preset, value):
        """Defines a sensor sensitivity preset.

        Arguments:
        preset -- the preset to define (0 or 1)
        value -- the sensitivity (250, 500, 1000, 1250, 1500, 1750, 2000, 4000)
        """
        allowed_values = {
            250: 0x08,
            500: 0x07,
            1000: 0x06,
            1250: 0x05,
            1500: 0x04,
            1750: 0x03,
            2000: 0x02,
            4000: 0x01,
        }
        if preset not in (1, 2):
            raise ValueError()
        if value not in allowed_values:
            raise ValueError()
        self._device_write(0x03, preset, allowed_values[value])

    def set_polling_rate(self, rate):
        """Set the polling rate.

        Arguments:
        rate -- the polling rate (125, 250, 500, 1000)
        """
        rates = {
            125: 0x04,
            250: 0x03,
            500: 0x02,
            1000: 0x01,
        }
        if not rate in rates:
            raise ValueError()
        self._device_write(0x04, 0x00, rates[rate])

    def set_color(self, *args):
        """Set the back-light color.

        Arguments:
        *args -- the color (red, green, blue channel or hexadecimal color or color name)

        Examples:
        set_color(255, 0, 0)
        set_color("red")
        set_color("#ff0000")
        set_color("#f00")
        set_color("ff0000)
        set_color("f00")
        """
        color = (0xFF, 0x00, 0x00)
        if len(args) == 3:
            for value in args:
                if type(value) != int or value < 0 or value > 255:
                    raise ValueError()
            color = args
        elif len(args) == 1 and type(args[0]) == str and is_color(args[0]):
            color = color_string_to_rgb(args[0])
        else:
            raise ValueError()
        self._device_write(0x05, 0x00, *color)

    def set_light_effect(self, effect):
        """Set the light effect (static, breath,...).

        Arguments:
        effect -- the effect (1 or self.EFFECT_STATIC, 2, 3 or self.EFFECT_BREATH, 4)
        """
        if effect < 1 or effect > 4:
            raise ValueError()
        self._device_write(0x07, 0x00, effect)

    def set_btn6_action(self, action):
        """Set the action of the button under the wheel (toggle sensitivity
        presets or controlled by the os).

        Arguments:
        action -- the action (self.BTN_ACTION_DEFAULT, self.BTN_ACTION_OS)
        """
        if action not in (self.BTN_ACTION_DEFAULT, self.BTN_ACTION_OS):
            raise ValueError()
        self._device_write(0x0B, action)

    def save(self):
        """Save the current configuration to the mouse internal memory."""
        self._device_write(0x09, 0x00)

    def _device_open(self):
        """Open the device file"""
        self._device = open(self._device_path, "wb")

    def _device_write(self, *bytes_):
        """Write bytes to the device file.

        Arguments:
        *bytes_ -- bytes to write
        """
        if not self._device:
            return;
        self._device.write(bytearray(bytes_))
        self._device.flush()

    def _device_close(self):
        """Close the device file."""
        if self._device:
            self._device.close()
            self._device = None

    def __del__(self):
        self._device_close()

