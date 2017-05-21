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
    if not env_name in os.environ:
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
    return _get_mouse_id_from_env("RIVALCFG_PROFILE")


def get_debug_device():
    mouseId = _get_mouse_id_from_env("RIVALCFG_DEVICE")
    if mouseId:
        return mouseId
    return _get_mouse_id_from_env("RIVALCFG_PROFILE")
