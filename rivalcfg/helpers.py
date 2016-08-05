import re

import pyudev


NAMED_COLORS = {
      "white": (0x00, 0x00, 0x00),
     "silver": (0xC0, 0xC0, 0xC0),
       "gray": (0x80, 0x80, 0x80),
      "black": (0x00, 0x00, 0x00),
        "red": (0xFF, 0x00, 0x00),
     "maroon": (0x80, 0x00, 0x00),
     "yellow": (0xFF, 0xFF, 0x00),
      "olive": (0x80, 0x80, 0x00),
       "lime": (0x00, 0xFF, 0x00),
      "green": (0x00, 0x80, 0x00),
       "aqua": (0x00, 0xFF, 0xFF),
       "teal": (0x00, 0x80, 0x80),
       "blue": (0x00, 0x00, 0xFF),
       "navy": (0x00, 0x00, 0x80),
    "fuchsia": (0xFF, 0x00, 0xFF),
     "purple": (0x80, 0x00, 0x80),
}


def usb_device_is_connected(vendor_id, product_id):
    """Checks if the given device is connected to the USB bus.

    Arguments:
    vendor_id -- the vendor id of the device
    product_id -- the product id of the device
    """
    ctx = pyudev.Context()
    devices = ctx.list_devices(ID_VENDOR_ID=vendor_id)

    for device in devices:
        if (device["ID_MODEL_ID"] == product_id):
            return True
    return False


def find_hidraw_device_path(vendor_id, product_id, interface_num=0):
    """
    Find the first HID interface for the given USB vendor id and product id.

    Arguments:
    vendor_id -- the vendor id of the device
    product_id -- the product id of the device
    interface_num -- the interface number (default: 0)
    """
    ctx = pyudev.Context()
    devices = ctx.list_devices(ID_VENDOR_ID=vendor_id)

    for device in devices:
        if (device["ID_MODEL_ID"] != product_id):
            continue
        if (device["SUBSYSTEM"] != "hidraw"):
            continue
        if int(device["ID_USB_INTERFACE_NUM"]) != interface_num:
            continue

        return device["DEVNAME"]

    # Old Kernels...
    devices = ctx.list_devices(SUBSYSTEM="hidraw")
    deviceMatcher = re.compile(r"^.*/usb./[0-9/.-]+:[0-9]+\.%i/[0-9]+:%s:%s.*$" % (
        interface_num,
        vendor_id,
        product_id
        ))
    for device in devices:
        if not deviceMatcher.match(device["DEVPATH"]):
            continue

        return device["DEVNAME"]



def is_color(string):
    """Checks if the given string is a valid color.

    Arguments:
    string -- the string to check
    """
    return string in NAMED_COLORS or bool(re.match(r"^#?[0-9a-f]{3}([0-9a-f]{3})?$", string, re.IGNORECASE))


def color_string_to_rgb(color_string):
    """Converts the color string into an RGB tuple.

    Arguments:
    color_string -- the string to converts

    Returns:
    an (R, G, B) tuple
    """
    # Named color
    if color_string in NAMED_COLORS:
        return NAMED_COLORS[color_string]
    # #f00 or #ff0000 -> f00 or ff0000
    if color_string.startswith("#"):
        color_string = color_string[1:]
    # f00 -> ff0000
    if len(color_string) == 3:
        color_string = color_string[0] * 2 + color_string[1] * 2 + color_string[2] * 2
    # ff0000 -> (255, 0, 0)
    return (
        int(color_string[0:2], 16),
        int(color_string[2:4], 16),
        int(color_string[4:], 16)
        )


def choices_to_list(choices):
    """Transforms choices dict to an ordered string list.

    Arguments:
    choices -- the dict containing available choices
    """
    return list(map(str, sorted(choices.keys(), key=lambda v: v if type(v) == int else -1)))


def choices_to_string(choices):
    """Transforms choices dict to a printable string.

    Arguments:
    choices -- the dict containing available choices
    """
    return ", ".join(choices_to_list(choices))


def merge_bytes(*args):
    """Merge byte and list of byte into a single list of byte."""
    result = []
    for arg in args:
        if type(arg) in [list, tuple]:
            result.extend(arg)
        else:
            result.append(arg)
    return result

