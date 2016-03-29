VENDOR_ID = "1038"
PRODUCT_ID = "1702"

class Rival100:

    EFFECT_STATIC = 0x01
    EFFECT_BREATH = 0x03

    BTN_ACTION_DEFAULT = 0x00
    BTN_ACTION_OS = 0x01

    def __init__(self, device_path):
        pass

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
        pass

    def set_light_effect(self, effect):
        pass

    def set_btn6_action(self, action):
        pass

    def save(self):
        pass

    def _device_open(self):
        pass

    def _device_write(self, bytes_):
        pass

    def _device_close(self):
        pass

    def __del__(self):
        self._device_close()
