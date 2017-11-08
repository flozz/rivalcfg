from io import BytesIO

import hid

from . import debug


HID_REPORT_TYPE_OUTPUT = 0x02
HID_REPORT_TYPE_FEATURE = 0x03


def is_device_plugged(vendor_id, product_id):
    """Returns True if the given HID device is plugged to the computer.

    Arguments:
    vendor_id -- the mouse vendor id (e.g. 0x1038)
    product_id -- the mouse product id (e.g. 0x1710)
    """
    if debug.DEBUG:
        mouse_id = debug.get_debug_profile()
        if mouse_id:
            return (mouse_id.vendor_id == vendor_id
                    and mouse_id.product_id == product_id)
    return len(hid.enumerate(vendor_id, product_id)) > 0


def open_device(vendor_id, product_id, interface_number):
    """Opens and returns the HID device (file-like object). Raise IOError if
    the device or interface is not available.

    Arguments:
    vendor_id -- the mouse vendor id (e.g. 0x1038)
    product_id -- the mouse product id (e.g. 0x1710)
    interface_number -- the interface number (e.g. 0x00)
    """
    # Dry run
    if debug.DEBUG and debug.DRY and is_device_plugged(vendor_id, product_id):
        device = BytesIO()  # Moke the device
        device.send_feature_report = device.write
        return device

    # Real device
    for interface in hid.enumerate(vendor_id, product_id):
        if interface["interface_number"] != interface_number:
            continue
        device = hid.device()
        device.open_path(interface["path"])
        return device

    raise IOError("Unable to find the requested device: %04X:%04X:%02X" % (
        vendor_id, product_id, interface_number))
