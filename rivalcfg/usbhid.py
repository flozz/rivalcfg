"""
This module contains low level functions to interact with USB HID devices. The
`hidapi <https://pypi.org/project/hidapi/>`_ module is used to abstract the
access to the devices across all different operating systems.

This module can also simulate devices:

* if you define the ``RIVALCFG_DRY`` environment variable, a fake device will
  be returned instead of a real one. This is useful for debugging and testing::

    RIVALCFG_DRY=1 rivalcfg -c ff0000

* If you define the ``RIVALCFG_PROFILE`` environment variable with a vendor id
  and a product id, this module will report the corresponding device as being
  plugged::

    RIVALCFG_PROFILE=1038:1702 rivalcfg -h
"""


import os
import struct
from io import BytesIO

import hid


#: HID output report
HID_REPORT_TYPE_OUTPUT = 0x02

#: HID feature report
HID_REPORT_TYPE_FEATURE = 0x03


def is_device_plugged(vendor_id, product_id):
    """Returns ``True`` if the given HID device is plugged to the computer.

    :param int vendor_id: The vendor id of the device (e.g. ``0x1038``)).
    :param int product_id: The product id of the device (e.g. ``0x1710``).

    :rtype: bool

    >>> from rivalcfg import usbhid
    >>> usbhid.is_device_plugged(0x1038, 0xbaad)
    False
    """
    if "RIVALCFG_PROFILE" in os.environ:
        debug_vendor_id = int(os.environ["RIVALCFG_PROFILE"].split(":")[0], 16)
        debug_product_id = int(os.environ["RIVALCFG_PROFILE"].split(":")[1], 16)
        if debug_vendor_id == vendor_id and debug_product_id == product_id:
            return True
    return len(hid.enumerate(vendor_id, product_id)) > 0


def open_device(vendor_id, product_id, endpoint):
    """Opens and returns the HID device

    :param int vendor_id: The vendor id of the device (e.g. ``0x1038``)).
    :param int product_id: The product id of the device (e.g. ``0x1710``).
    :param int endpoint: The number of the endpoint to open on the device (e.g.
                         ``0``).

    :raise DeviceNotFound: The requested device is not plugged to the computer
                           or it does not provide the requested endpoint.
    :raise IOError: The device or its interface cannot be opened (permission
                    issue, device busy,...).

    :rtype: hid.device

    >>> from rivalcfg import usbhid
    >>> usbhid.open_device(0x1038, 0x1702, 0)
    <hid.device at 0x...>
    """
    # Instanciate the device (real or fake depending of environment)
    if "RIVALCFG_DRY" in os.environ:
        # Setting a path allows the fake device to be opened even if requested
        # device is not plugged to the computer
        path = b"00:0000:0000"
        device = FakeDevice()
    else:
        path = None
        device = hid.device()

    # Search the device
    for interface in hid.enumerate(vendor_id, product_id):
        if interface["interface_number"] == endpoint:
            path = interface["path"]
            break

    # Open the found device. This can raise an IOError.
    if path:
        device.open_path(path)
        return device

    # No matching device found
    raise DeviceNotFound(
        "Requested device or endpoint not found: %04x:%04x:%02x"
        % (vendor_id, product_id, endpoint)
    )


class DeviceNotFound(Exception):
    """Exception raised when the requested device was not found (device not
    plugged to the computer) or when it does not provide the requested
    endpoint.
    """


class FakeDevice:

    """This class simulate an HID device as provided by the `hidapi
    <https://pypi.org/project/hidapi/>`_ module.

    Data sent to the fake device can be read-back from the :attr:`bytes`
    attribute of this class.
    """

    def __init__(self):
        """Constructor."""

        #: A BytesIO instance where every simulated write will be done.
        self.bytes = BytesIO()

    def open_path(self, path):
        """Simulate opening the device from given path.

        :param bytes path: The device path.
        """
        pass

    def write(self, data):
        """Simulate a write to an HID device.

        Given data will be writen to :attr:`bytes`, prefixed with the
        :data:`HID_REPORT_TYPE_OUTPUT` byte.

        :param bytes data: The data to send to the device.

        >>> from rivalcfg.usbhid import FakeDevice
        >>> dev = FakeDevice()
        >>> dev.write(b"\\x00\\xAA\\xBB\\xCC")
        >>> dev.bytes.seek(0)
        0
        >>> dev.bytes.read()
        b'\\x02\\x00\\xaa\\xbb\\xcc'
        """
        self.bytes.write(struct.pack("B", HID_REPORT_TYPE_OUTPUT))
        self.bytes.write(data)

    def send_feature_report(self, data):
        """Simulate a feature report write to an HID device.

        Given data will be writen to :attr:`bytes`, prefixed with the
        :data:`HID_REPORT_TYPE_FEATURE` byte.

        :param bytes data: The data to send to the device.

        >>> from rivalcfg.usbhid import FakeDevice
        >>> dev = FakeDevice()
        >>> dev.send_feature_report(b"\\x00\\xAA\\xBB\\xCC")
        >>> dev.bytes.seek(0)
        0
        >>> dev.bytes.read()
        b'\\x03\\x00\\xaa\\xbb\\xcc'
        """
        self.bytes.write(struct.pack("B", HID_REPORT_TYPE_FEATURE))
        self.bytes.write(data)

    def close(self):
        """Closes the simulated device."""
        self.bytes.close()

    def error(self):
        raise NotImplementedError()

    def get_feature_report(self):
        raise NotImplementedError()

    def get_manufacturer_string(self):
        raise NotImplementedError()

    def get_product_string(self):
        raise NotImplementedError()

    def get_serial_number_string(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def read(self, max_length, timeout_ms=0):
        return [0] * max_length

    def set_nonblocking(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<hid.device at 0xbadc0fee%x>" % id(self)
