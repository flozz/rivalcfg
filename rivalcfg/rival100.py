from helpers import is_color, color_string_to_rgb


VENDOR_ID = "1038"
PRODUCT_ID = "1702"


class Rival100:

    EFFECT_STATIC = 0x01
    EFFECT_BREATH = 0x03

    BTN_ACTION_DEFAULT = 0x00
    BTN_ACTION_OS = 0x01

    def __init__(self, device_path):
        self._device = None
        self._device_path = device_path
        self._device_open()

    def set_default(self):
        """Set all option to their default values"""
        self.set_sensitivity(1, 1000)
        self.set_sensitivity(2, 2000)
        self.set_polling_rate(1000)
        self.set_color("#00ffff")
        self.set_light_effect(self.EFFECT_STATIC)
        self.set_btn6_action(self.BTN_ACTION_DEFAULT)

    def set_sensitivity(self, preset, value):
        pass

    def set_polling_rate(self, rate):
        pass

    def set_color(self, *args):
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
        pass

    def set_btn6_action(self, action):
        pass

    def save(self):
        self._device_write(0x09, 0x00)

    def _device_open(self):
        self._device = open(self._device_path, "wb")

    def _device_write(self, *bytes_):
        if not self._device:
            return;
        self._device.write(bytearray(bytes_))
        self._device.flush()

    def _device_close(self):
        if self._device:
            self._device.close()
            self._device = None

    def __del__(self):
        self._device_close()

