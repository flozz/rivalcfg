from . import usbhid
from . import devices
from . import handlers
from . import helpers


def get_mouse(vendor_id=0x1038, product_id=None):
    """Get a :class:`Mouse` instance to manipulate requested device.

    :param int vendor_id: The vendor id of the device (optional, by default
                          this is set to the SteelSeries vendor id
                          (``0x1038``)).
    :param int product_id: The product id of one of the supported device (e.g.
                           ``0x1702``).

    >>> from rivalcfg.mouse import get_mouse
    >>> get_mouse(vendor_id=0x1038, product_id=0x1702)
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """
    if not product_id:
        raise ValueError("You must define the 'product_id' parameter")

    profile = devices.get_profile(vendor_id, product_id)

    if not profile:
        pass  # TODO raise an error

    hid_device = usbhid.open_device(vendor_id, product_id, profile["endpoint"])

    return Mouse(hid_device, profile)


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
    >>> Mouse(
    ...     usbhid.open_device(vendor_id=0x1038, product_id=0x1702, endpoint=0),
    ...     devices.get_profile(vendor_id=0x1038, product_id=0x1702))
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """  # noqa

    def __init__(self, hid_device, mouse_profile):
        """Constructor."""
        self._hid_device = hid_device
        self._mouse_profile = mouse_profile

    def reset_settings(self):
        """Sets all settings to their factory default values."""
        pass

    def save(self):
        """Save current config to the mouse internal memory."""
        # This should never apand... But who knows...
        if "save_command" not in self._mouse_profile \
           or not self._mouse_profile["save_command"]:
            raise Exception("This mouse does not provide any save command.")
        self._hid_write(
                report_type=self._mouse_profile["save_command"]["report_type"],
                data=self._mouse_profile["save_command"]["command"])

    def _hid_write(self,
                   report_type=usbhid.HID_REPORT_TYPE_OUTPUT,
                   report_id=0x00,
                   data=[]):
        """
        Write data to the device.

        :param int report_type: The HID report type
                                (:data:`rivalcfg.usbhid.HID_REPORT_TYPE_OUTPUT`
                                or
                                :data:`rivalcfg.usbhid.HID_REPORT_TYPE_FEATURE`).
        :param int report_id: The id of the report (always ``0x00``).
        :param list(int) data: The data to send to the mouse.

        :raises ValueError: Invalid report type, or HID device not openned.
        """
        bytes_ = bytearray(helpers.merge_bytes(report_id, data))
        if report_type == usbhid.HID_REPORT_TYPE_OUTPUT:
            self._hid_device.write(bytes_)
        elif report_type == usbhid.HID_REPORT_TYPE_FEATURE:
            self._hid_device.send_feature_report(bytes_)
        else:
            raise ValueError("Invalid HID report type: %2x" % report_type)

    def __getattr__(self, name):
        # Handle every set_xxx methods generated from device's profiles

        if not name.startswith("set_"):
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_name = name[4:]

        if setting_name not in self._mouse_profile["settings"]:
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_info = self._mouse_profile["settings"][setting_name]

        handler_name = None

        if "value_type" in setting_info and setting_info["value_type"]:
            handler_name = setting_info["value_type"]
            if handler_name not in helpers.module_ls(handlers):
                raise ValueError("Unknown handler '%s' for '%s' setting of the %s" % (  # noqa
                    handler_name,
                    setting_name,
                    self._mouse_profile["name"]))

        def _exec_command(*args):
            data = []
            if handler_name:
                data = getattr(handlers, handler_name) \
                        .process_value(setting_info, *args)
            self._hid_write(
                    report_type=setting_info["report_type"],
                    data=helpers.merge_bytes(setting_info["command"], data))

        return _exec_command

    def __repr__(self):
        return "<Mouse %s (%04x:%04x:%02x)>" % (
                self._mouse_profile["name"],
                self._mouse_profile["vendor_id"],
                self._mouse_profile["product_id"],
                self._mouse_profile["endpoint"])
