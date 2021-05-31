import time

from . import usbhid
from . import devices
from . import handlers
from . import helpers
from . import mouse_settings


def get_mouse(vendor_id=0x1038, product_id=None):
    """Get a :class:`Mouse` instance to manipulate requested device.

    :param int vendor_id: The vendor id of the device (optional, by default
                          this is set to the SteelSeries vendor id
                          (``0x1038``)).
    :param int product_id: The product id of one of the supported device (e.g.
                           ``0x1702``).
    :raise rivalcfg.devices.UnsupportedDevice: The requested device is not
                                               supported by rivalcfg.
    :rtype: Mouse

    >>> from rivalcfg.mouse import get_mouse
    >>> get_mouse(vendor_id=0x1038, product_id=0x1702)
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """
    if not product_id:
        raise ValueError("You must define the 'product_id' parameter")

    profile = devices.get_profile(vendor_id, product_id)
    settings = mouse_settings.get_mouse_settings(
        vendor_id,
        product_id,
        profile,
    )

    hid_device = usbhid.open_device(vendor_id, product_id, profile["endpoint"])

    return Mouse(hid_device, profile, settings)


class Mouse:

    """Generic class to handle any supported mouse.

    .. NOTE::

       Additional methods are available in this class depending on the loaded
       profile. Read device specific documentation for more information.

    .. WARNING::

       You should not instanciate this class yourself. Use the
       :func:`get_mouse` factory function instead.

    :param hid_device: The HID device to write in (provided by the
                        :func:`rivalcfg.usbhid.open_device`).
    :param mouse_profile: One of the rivalcfg mouse profile (provided by
                            :func:`rivalcfg.devices.get_profile`).

    >>> from rivalcfg import usbhid
    >>> from rivalcfg import devices
    >>> from rivalcfg.mouse import Mouse
    >>> from rivalcfg.mouse_settings import get_mouse_settings
    >>> profile = devices.get_profile(vendor_id=0x1038, product_id=0x1702)
    >>> settings = get_mouse_settings(0x1038, 0x1702, profile)
    >>> Mouse(
    ...     usbhid.open_device(vendor_id=0x1038, product_id=0x1702, endpoint=0),
    ...     profile,
    ...     settings,
    ... )
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """

    #: The mouse settings (``rivalcfg.devices.*``)
    mouse_profile = None

    #: The mouse settings (:class:`rivalcfg.mouse_settings.MouseSettings`)
    mouse_settings = None

    def __init__(self, hid_device, mouse_profile, mouse_settings):
        """Constructor."""
        self._hid_device = hid_device
        self.mouse_profile = mouse_profile
        self.mouse_settings = mouse_settings

    @property
    def name(self):
        """The mouse name."""
        return self.mouse_profile["name"]

    @property
    def vendor_id(self):
        """The mouse vendor id."""
        return self.mouse_profile["vendor_id"]

    @property
    def product_id(self):
        """The mouse product id."""
        return self.mouse_profile["product_id"]

    @property
    def firmware_version_tuple(self):
        """The firmware version of the device as a tuple (e.g.``(1, 33)``,
        ``(0,)`` if not available).
        """
        if "firmware_version" not in self.mouse_profile:
            return (0,)
        self._hid_write(
            usbhid.HID_REPORT_TYPE_OUTPUT,
            data=self.mouse_profile["firmware_version"]["command"],
        )
        version = self._hid_device.read(
            self.mouse_profile["firmware_version"]["response_length"],
            timeout_ms=200,
        )
        return tuple(version[::-1])

    @property
    def firmware_version(self):
        """The firmware version as an human readable string (e.g. ``"1.33"``,
        ``"0"`` if not available).
        """
        return ".".join([str(i) for i in self.firmware_version_tuple])

    def reset_settings(self):
        """Sets all settings to their factory default values."""
        for name, setting_info in self.mouse_profile["settings"].items():
            method_name = "set_%s" % name
            method = getattr(self, method_name)
            if "value_type" in setting_info and setting_info["value_type"]:
                method(setting_info["default"])
            else:
                method()

    def save(self):
        """Save current config to the mouse internal memory."""
        # This should never apand... But who knows...
        if (
            "save_command" not in self.mouse_profile
            or not self.mouse_profile["save_command"]
        ):
            raise Exception("This mouse does not provide any save command.")

        packet_length = 0
        if "packet_length" in self.mouse_profile["save_command"]:
            packet_length = self.mouse_profile["save_command"]["packet_length"]

        self._hid_write(
            report_type=self.mouse_profile["save_command"]["report_type"],
            data=self.mouse_profile["save_command"]["command"],
            packet_length=packet_length,
        )

        self.mouse_settings.save()

    def close(self):
        """Close the device.

        .. WARNING::

           Once called, any access of the Mouse class properties or function
           may raise an error.
        """
        self._hid_device.close()

    def _hid_write(
        self,
        report_type=usbhid.HID_REPORT_TYPE_OUTPUT,
        report_id=0x00,
        data=[],
        packet_length=0,
    ):
        """
        Write data to the device.

        :param int report_type: The HID report type
                                (:data:`rivalcfg.usbhid.HID_REPORT_TYPE_OUTPUT`
                                or
                                :data:`rivalcfg.usbhid.HID_REPORT_TYPE_FEATURE`).
        :param int report_id: The id of the report (always ``0x00``).
        :param list(int) data: The data to send to the mouse.
        :param int packet_length: The fixed length of the packet that will be
                                  sent to the device (default: ``0`` (no fixed
                                  length)).

        :raises ValueError: Invalid report type, or HID device not openned.
        """
        if packet_length:
            bytes_ = bytearray(
                helpers.merge_bytes(
                    report_id, data, [0x00] * (packet_length - len(data))
                )
            )
        else:
            bytes_ = bytearray(helpers.merge_bytes(report_id, data))
        if report_type == usbhid.HID_REPORT_TYPE_OUTPUT:
            self._hid_device.write(bytes_)
        elif report_type == usbhid.HID_REPORT_TYPE_FEATURE:
            self._hid_device.send_feature_report(bytes_)
        else:
            raise ValueError("Invalid HID report type: %2x" % report_type)

        # Avoids sending multiple commands to quickly
        time.sleep(0.01)

    def __getattr__(self, name):
        # Handle every set_xxx methods generated from device's profiles

        if not name.startswith("set_"):
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_name = name[4:]

        if setting_name not in self.mouse_profile["settings"]:
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_info = self.mouse_profile["settings"][setting_name]

        handler_name = None

        if "value_type" in setting_info and setting_info["value_type"]:
            handler_name = setting_info["value_type"]
            if handler_name not in helpers.module_ls(handlers):
                raise ValueError(
                    "Unknown handler '%s' for '%s' setting of the %s"
                    % (
                        handler_name,
                        setting_name,
                        self.mouse_profile["name"],
                    )
                )

        packet_length = 0
        if "packet_length" in setting_info:
            packet_length = setting_info["packet_length"]

        suffix = []
        if "command_suffix" in setting_info:
            suffix = setting_info["command_suffix"]

        def _exec_command(*args):
            data = []
            if handler_name:
                data = getattr(handlers, handler_name).process_value(
                    setting_info, *args
                )
            self._hid_write(
                report_type=setting_info["report_type"],
                data=helpers.merge_bytes(setting_info["command"], data, suffix),
                packet_length=packet_length,
            )
            if len(args) == 1:
                self.mouse_settings.set(setting_name, args[0])
            else:
                self.mouse_settings.set(setting_name, args)

        return _exec_command

    def __repr__(self):
        return "<Mouse %s (%04x:%04x:%02x)>" % (
            self.mouse_profile["name"],
            self.mouse_profile["vendor_id"],
            self.mouse_profile["product_id"],
            self.mouse_profile["endpoint"],
        )

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()
