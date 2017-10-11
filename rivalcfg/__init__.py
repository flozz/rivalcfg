"""
This module contains functions to get information about mice and to get an
object to manipulate a specific mouse.

Usage and examples
------------------

Changing the color of the first mouse found::

    import rivalcfg

    mouse = rivalcfg.get_first_mouse()
    mouse.set_color("red")

Listing all available mice and changing their color::

    import rivalcfg

    mice_info = rivalcfg.list_available_mice()

    for mouse_info in mice_info:
        mouse = rivalcfg.get_mouse(mouse_info.vendor_id, mouse_info.product_id)
        mouse.set_color(red)

.. NOTE::

    In previous examples, we assumed that only Rival 100 mice were connected to
    the computer: the methods available on the ``mouse`` object depends on the
    mouse model.


Public API
----------
"""


import collections

from . import usbhid
from .version import VERSION
from .profiles import mice_profiles
from .mouse import Mouse


#: Tuple containing information about a specific mouse
MouseInfo = collections.namedtuple(
        "MouseInfo", ("name", "vendor_id", "product_id"))


def list_supported_mice():
    """Returns the list of all mice supported by this software.

    :rtype: list of :py:class:`rivalcfg.MouseInfo`
    """
    return (MouseInfo(
            name=profile["name"],
            vendor_id=profile["vendor_id"],
            product_id=profile["product_id"],
            ) for profile in mice_profiles)


def list_available_mice():
    """Return the list of supported mice currently availale (plugged to the
    computer).

    :rtype: list of :py:class:`rivalcfg.MouseInfo`
    """
    for mouse in list_supported_mice():
        if usbhid.is_device_plugged(mouse.vendor_id, mouse.product_id):
            yield mouse


def get_mouse_profile(vendor_id, product_id):
    """Returns the profile (informations and list of available commands) of the
    given mouse.

    :param int vendor_id: The vendor id (currenlty this should be set to
                          0x1038)
    :param int product_id: The product id of the mouse (e.g. 0x1710 for the
                           Rival 300)

    :rtype: dict
    """
    for profile in mice_profiles:
        if (profile["vendor_id"] == vendor_id
                and profile["product_id"] == product_id):
            return profile
    return None


def get_mouse(vendor_id, product_id):
    """Returns a class that allows you to manipulaite the given mouse if it is
    available, else returns None.

    :param int vendor_id: The vendor id (currenlty this should be set to
                          0x1038)
    :param int product_id: The product id of the mouse (e.g. 0x1710 for the
                           Rival 300)

    :rtype: :py:class:`rivalcfg.mouse.Mouse`
    """
    profile = get_mouse_profile(vendor_id, product_id)
    if not profile:
        return None
    return Mouse(profile)


def get_first_mouse():
    """Returns the first available mouse if any mouse is connected, else
    returns None.

    :rtype: :py:class:`rivalcfg.mouse.Mouse`
    """
    for mouse in list_available_mice():
        return get_mouse(mouse.vendor_id, mouse.product_id)
    return None


__all__ = [
        "VERSION",
        "list_supported_mice",
        "list_available_mice",
        "get_mouse_profile",
        "get_mouse",
        "get_first_mouse",
        ]
