import os

from . import devices
from . import mouse


def get_first_mouse():
    """Get the first plugged mouse that can befound. As there is only one mouse
    plugged to a computer most of the time, it should return the right one. ;)

    :rtype: rivalcfg.mouse.Mouse
    :return: The mouse if one supported device is found, else returns ``None``.

    Always return ``None`` when ``RIVALCFG_PROFILE=0000:0000`` is defined in
    the environment.

    >>> import rivalcfg
    >>> rivalcfg.get_first_mouse()  # doctest: +SKIP
    <Mouse ...>
    """
    if (
        "RIVALCFG_PROFILE" in os.environ
        and os.environ["RIVALCFG_PROFILE"] == "0000:0000"
    ):
        return None
    plugged_devices = list(devices.list_plugged_devices())
    if not plugged_devices:
        return None
    return mouse.get_mouse(
        vendor_id=plugged_devices[0]["vendor_id"],
        product_id=plugged_devices[0]["product_id"],
    )
