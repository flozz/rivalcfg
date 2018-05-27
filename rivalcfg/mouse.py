import time
from . import usbhid
from . import debug
from . import helpers
from . import command_handlers


REPORT_TYPE_TO_HIDAPI_FUNCTION = {
    0x02: "write",
    0x03: "send_feature_report"
    }


class Mouse:

    """Generic class to handle any supported mouse. The methods availabled on
    this class depends of the loaded profile.

    :param dict profile: the mouse profile to load (``rivalcfg.profiles.*``)
    """

    profile = None
    _device = None

    def __init__(self, profile):
        """Contructor."""
        self.profile = profile
        self._device = usbhid.open_device(
                profile["vendor_id"],
                profile["product_id"],
                profile["interface_number"])

    def set_default(self):
        """Sets all option to their factory values."""
        for command in self.profile["commands"]:
            if "default" in self.profile["commands"][command]:
                default = self.profile["commands"][command]["default"]
                if not type(default) in [list, tuple]:
                    default = [default]
                getattr(self, command)(*default)

    def _device_write(self, bytes_, report_type=usbhid.HID_REPORT_TYPE_OUTPUT):
        """Writes bytes to the device.

        :param bytes bytes_: bytes to write
        :param int report_type: the HID Repport Type (0x02: output (default),
                                0x03: feature)
        """
        report_id = 0x00
        if debug.DEBUG:
            debug.log_bytes_hex(
                    "Mouse._device_write [wValue]",
                    [report_type, report_id])
            debug.log_bytes_hex("Mouse._device_write   [data]", bytes_)
        bytes_ = helpers.merge_bytes(report_id, bytes_)
        report_function = getattr(
                self._device,
                REPORT_TYPE_TO_HIDAPI_FUNCTION[report_type])
        report_function(bytearray(bytes_))

    def __getattr__(self, name):
        if name not in self.profile["commands"]:
            raise AttributeError("There is no command named '%s'" % name)

        command = self.profile["commands"][name]
        handler = "%s_handler" % str(command["value_type"]).lower()

        report_type = usbhid.HID_REPORT_TYPE_OUTPUT
        if "report_type" in command:
            report_type = command["report_type"]

        suffix = []
        if "suffix" in command:
            suffix = command["suffix"]

        is_gradient = False
        if "is_gradient" in command:
            is_gradient = command['is_gradient']

        if not hasattr(command_handlers, handler):
            raise Exception("There is not handler for the '%s' value type" % command["value_type"])  # noqa

        def _exec_command(*args):
            if is_gradient:
                t = 0.01
                c = 1
                SLEEP = 0.02
                INCREMENT = 0.001
                while True:
                    bytes_ = getattr(command_handlers, handler)(command, *args, t=t)
                    bytes_ = helpers.merge_bytes(bytes_, suffix)
                    self._device_write(bytes_, report_type)
                    time.sleep(SLEEP)
                    t = t + c*(INCREMENT)
                    if t > 0.99 or t < 0.01:
                        c = -c

            else:
                bytes_ = getattr(command_handlers, handler)(command, *args)
                bytes_ = helpers.merge_bytes(bytes_, suffix)
                self._device_write(bytes_, report_type)

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
        if self._device:
            self._device.close()
