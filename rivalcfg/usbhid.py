import hid

from . import debug


def is_mouse_plugged(vendor_id, product_id):
    """Returns True if the given mouse is plugged to the computer.

    Arguments:
    vendor_id -- the mouse vendor id (e.g. 0x1038)
    product_id -- the mouse product id (e.g. 0x1710)
    """
    if debug.DEBUG:
        mouse_id = debug.get_debug_profile()
        if mouse_id:
            return mouse_id.vendor_id == vendor_id and mouse_id.product_id == product_id
    return len(hid.enumerate(vendor_id=vendor_id, product_id=product_id)) > 0
