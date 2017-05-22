from functools import partial

from . import usbhid
from . import debug
from . import helpers


class Mouse:

    """Generic class to handle any supported mouse."""

    def __init__(self, profile):
        """Contructor.

        Arguments:
        profile -- the mouse profile (rivalcfg.profiles.*)
        """
        self.profile = profile
        self._device = usbhid.open_device(
                profile["vendor_id"],
                profile["product_id"],
                profile["interface_number"])

    def set_default(self):
        """Set all option to their factory values."""
        for command in self.profile["commands"]:
            if "default" in self.profile["commands"][command]:
                getattr(self, command)(self.profile["commands"][command]["default"])

    def _device_write(self, *bytes_):
        """Write bytes to the device file.

        Arguments:
        *bytes_ -- bytes to write
        """
        pbytes = [0x00]
        pbytes.extend(bytes_)  # XXX fixes issue with Rival 300 new firmware (#5, #25, #28)
        if debug.DEBUG:
            debug.log_bytes_hex("_device_write", pbytes)
        self._device.write(bytearray(pbytes))

    def _handler_choice(self, command, value):
        """Handle commands with value picked from a dict."""
        if not value in command["choices"]:
            raise ValueError("value must be one of [%s]" % choices_to_string(command["choices"]))
        if "value_transform" in command:
            self._device_write(*helpers.merge_bytes(command["command"], command["value_transform"](value)))
        else:
            self._device_write(*helpers.merge_bytes(command["command"], command["choices"][value]))

    def _handler_rgbcolor(self, command, *args):
        """Handle commands with RGB color values."""
        color = (0x00, 0x00, 0x00)
        if len(args) == 3:
            for value in args:
                if type(value) != int or value < 0 or value > 255:
                    raise ValueError()
            color = args
        elif len(args) == 1 and type(args[0]) == str and helpers.is_color(args[0]):
            color = helpers.color_string_to_rgb(args[0])
        else:
            raise ValueError()
        if "value_transform" in command:
            self._device_write(*helpers.merge_bytes(command["command"], command["value_transform"](*args)))
        else:
            self._device_write(*helpers.merge_bytes(command["command"], color))

    def _handler_range(self, command, value):
        """Handle commands with value from a range."""
        if not command["range_min"] <= value <= command["range_max"]:
            raise ValueError("Value %i not in range (%i, %i)" % (
                value,
                command["range_min"],
                command["range_max"]
                ))
        if value % command["range_increment"] != 0:
            raise ValueError("Value %i is not an increment of %i" % (
                value,
                command["range_increment"]
                ))
        if "value_transform" in command:
            self._device_write(*helpers.merge_bytes(command["command"], command["value_transform"](value)))
        else:
            self._device_write(*helpers.merge_bytes(command["command"], value))


    def _handler_none(self, command):
        """Handle commands with no values."""
        self._device_write(*command["command"])

    def __getattr__(self, name):
        if not name in self.profile["commands"]:
            raise AttributeError("There is no command named '%s'" % name)
        command = self.profile["commands"][name]
        handler = "_handler_%s" % str(command["value_type"]).lower()
        if not hasattr(self, handler):
            raise Exception("There is not handler for the '%s' value type" % command["value_type"])
        return partial(getattr(self, handler), command)

    def __repr__(self):
        return "<Mouse %s (%04X:%04X:%02X)>" % (
                self.profile["name"],
                self.profile["vendor_id"],
                self.profile["product_id"],
                self.profile["interface_number"])

    def __str__(self):
        return self.__repr__()

    def __del__(self):
        self._device.close()

