from __future__ import print_function

import os
import re
import collections


DEBUG = (
        "RIVALCFG_DEBUG" in os.environ or
        "RIVALCFG_DRY" in os.environ or
        "RIVALCFG_PROFILE" in os.environ or
        "RIVALCFG_DEVICE" in os.environ)

DRY = "RIVALCFG_DRY" in os.environ


MouseId = collections.namedtuple(
        "MouseId", ("vendor_id", "product_id"))


def _get_mouse_id_from_env(env_name):
    if env_name not in os.environ:
        return None
    env_value = os.environ[env_name]
    if not re.match(r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{4}$", env_value):
        raise ValueError("%s='%s' is not a valid mouse identifier" % (
            env_name, env_value))
    vendor_id, product_id = env_value.split(":")
    return MouseId(
            vendor_id=int(vendor_id, 16),
            product_id=int(product_id, 16))


def get_debug_profile():
    """Get the profile to debug from the RIVALCFG_PROFILE environment variable,
    if any.

    This profile should be selected as if the corresponding mouse was
    physically plugged to the computer.
    """
    return _get_mouse_id_from_env("RIVALCFG_PROFILE")


def get_debug_device():
    """Get the profile to debug from the RIVALCFG_DEVICE environment variable,
    if any.

    This device should be selected as the one where the commands will be
    written, regardless of the selected profile. This is usefull to debug a
    mouse that have the same command set than an other one but with a different
    product_id.

    If the RIVALCFG_PROFILE is defined but the RIVALCFG_DEVICE is not, this
    function returns the same output that get_debug_profile()."""
    mouse_id = _get_mouse_id_from_env("RIVALCFG_DEVICE")
    if mouse_id:
        return mouse_id
    return _get_mouse_id_from_env("RIVALCFG_PROFILE")


def log(*args):
    """Logs given arguments to stdout if the debug mode is enabled.

    Arguments:
    *args -- the things to log.
    """
    if not DEBUG:
        return
    print("[DEBUG]", *args)


def log_bytes_hex(message, bytes_):
    """Logs given message and bytes converted into hexadecimal to stdout if
    debug mod is enabled.

    Arguments:
    message -- the message to log
    bytes_ -- the bytes to log as hexadecimal numbers
    """
    if not DEBUG:
        return
    print("[DEBUG]", "%s:" % message, " ".join(["%02X" % int(b) for b in bytes_]))  # noqa
