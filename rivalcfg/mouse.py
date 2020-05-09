# from . import usbhid
# from . import devices


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
    pass


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

    def set_default(self):
        """Sets all options to their factory values."""
        pass

    def save(self):
        """Save current config to the mouse internal memory."""
        pass

    def __repr__(self):
        return "<Mouse %s (%04x:%04x:%02x)>" % (
                self._mouse_profile["name"],
                self._mouse_profile["vendor_id"],
                self._mouse_profile["product_id"],
                self._mouse_profile["endpoint"])
