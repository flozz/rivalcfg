from . import usbhid
from . import debug
from . import helpers
from . import command_handlers


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
        """Sets all option to their factory values."""
        for command in self.profile["commands"]:
            if "default" in self.profile["commands"][command]:
                getattr(self, command)(self.profile["commands"][command]["default"])

    def _device_write(self, *bytes_):
        """Writes bytes to the device.

        Arguments:
        *bytes_ -- bytes to write
        """
        # XXX fixes issue with Rival 300 new firmware (#5, #25, #28)
        bytes_ = helpers.merge_bytes(0x00, *bytes_)
        if debug.DEBUG:
            debug.log_bytes_hex("Mouse._device_write", bytes_)
        self._device.write(bytearray(bytes_))

    def __getattr__(self, name):
        if not name in self.profile["commands"]:
            raise AttributeError("There is no command named '%s'" % name)

        command = self.profile["commands"][name]
        handler = "%s_handler" % str(command["value_type"]).lower()

        if not hasattr(command_handlers, handler):
            raise Exception("There is not handler for the '%s' value type" % command["value_type"])

        def _exec_command(*args):
            bytes_ = getattr(command_handlers, handler)(command, *args)
            self._device_write(bytes_)

        return _exec_command

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

