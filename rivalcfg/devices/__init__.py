"""This module provides access to the profile of each supported device.

Profile spec
------------

A profile is just a ``dict`` that contains information about one or more mouse.
There is one profile file in ``rivalcfg/devices/`` by mouse familly (the "Rival
100" and the "Rival 100 Dota 2 Edition" are mouse of the same familly).

Here is what a profile file looks like::

    from .. import usbhid

    profile = {

        # The name of the mouse familly
        "name": "SteelSeries Rival 100",

        # List of all devices of the familly
        "models": [{
            # The name of a specific device of the familly
            "name": "SteelSeries Rival 100",
            # The vendor ID of the USB device (should always be 0x1038)
            "vendor_id": 0x1038,
            # The product ID of the USB device
            "product_id": 0x1702,
            # The control endpoint of the device (probably 0)
            "endpoint": 0,
        }, {
            "name": "SteelSeries Rival 100 (Dell China)",
            "vendor_id": 0x1038,
            "product_id": 0x170a,
            "endpoint": 0,
        }],

        # All available settings for the mice
        "settings": {

            # A setting of the mouse. The key name is important, it will
            # be used to generates the Mouse class API and in the CLI
            "polling_rate": {
                # A label that will be used one day to build a GUI
                "label": "Polling rate",
                # A short description of the option. Used to generate the CLI
                # help (rivalcfg --help)
                "description": "Set polling rate (Hz)",
                # The name of the CLI options to change this setting.
                "cli": ["-p", "--polling-rate"],
                # The repport type (rivalcfg.usbhid.HID_REPORT_TYPE_OUTPUT most
                # of the time)
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                # The command that should be sent to the USB device to update
                # this setting.
                "command": [0x04, 0x00],
                # A fixed amount of data to send to the mouse (optional).
                # This is required by some mice like the Rival 110.
                "packet_length": 32,
                # If greater that 0, the number of bytes to read from the
                # device after the command. This is required by some wireless
                # mice like the Aerox 3 Wireless in wireless mode.
                "readback_length": 0,
                # The type of value supported by this setting.
                # See the `rivalcfg.handlers` documentation for more
                # information.
                "value_type": "choice",
                # This parameter is specific to the `choice` handler.
                # Look at its documentation for more information.
                "choices": {
                    125: 0x04,
                    250: 0x03,
                    500: 0x02,
                    1000: 0x01,
                },
                # The factory default value of this setting.
                "default": 1000,
            },

            "color": {
                "label": "LED color",
                "description": "Set the mouse backlight color",
                "cli": ["-c", "--color"],
                "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
                "command": [0x05, 0x00],
                "value_type": "rgbcolor",
                "default": "#FF1800"
            },

            # ...

        },

        # The command that allows to persist data in the internal memory
        # of the device
        "save_command": {
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x09, 0x00],
        },

        # (optional) The command to get the firmware version from the device
        "firmware_version": {
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x90, 0x00],
            # The length of the response (bytes)
            "response_length": 2,
        },

    }

At runtime, a separated profile will be generated for each device of a mouse
familly. The profiles will then look like this::

    {

        "name": "SteelSeries Rival 100 (Dell China)",
        "vendor_id": 0x1038,
        "product_id": 0x170a,
        "endpoint": 0,

        "settings": {
            # ...
        },

        "save_command": {
            #...
        },

    }


Module API
----------

.. data:: rivalcfg.devices.PROFILES

    Profiles of each supported devices::

       {
           (vendor_id, product_id): {
               # profile data ...
           },
       }
"""

import os

from .. import usbhid

PROFILES = None


class UnsupportedDevice(Exception):
    """Exception raised when the requested device is not supported by rivalcfg."""


def list_plugged_devices():
    """List all plugged devices that are supported by rivalcfg.

    :rtype: generator

    ::

       [
           {"vendor_id": ..., "product_id": ..., "name": ...},
       ]

    If the ``RIVALCFG_PROFILE=vendor_id:product_id`` environment varialbe is
    defined, only the corresponding profile will be listed.
    """
    if "RIVALCFG_PROFILE" in os.environ:
        debug_vendor_id = int(os.environ["RIVALCFG_PROFILE"].split(":")[0], 16)
        debug_product_id = int(os.environ["RIVALCFG_PROFILE"].split(":")[1], 16)
        profile = PROFILES[(debug_vendor_id, debug_product_id)]
        yield {
            "vendor_id": profile["vendor_id"],
            "product_id": profile["product_id"],
            "name": profile["name"],
        }
    for profile in PROFILES.values():
        if usbhid.is_device_plugged(profile["vendor_id"], profile["product_id"]):
            yield {
                "vendor_id": profile["vendor_id"],
                "product_id": profile["product_id"],
                "name": profile["name"],
            }


def get_profile(vendor_id=0x1038, product_id=None):
    """Get the profile of the requested device.

    :param int vendor_id: The vendor id of the device (optional, by default
                          this is set to the SteelSeries vendor id
                          (``0x1038``)).
    :param int product_id: The product id of one of the supported device (e.g.
                           ``0x1702``).
    :raise UnsupportedDevice: The requested device is not supported by
                              rivalcfg.
    :rtype: dict

    >>> from rivalcfg import devices
    >>> devices.get_profile(vendor_id=0x1038, product_id=0x1702)
    {...'name': 'SteelSeries Rival 100'...}
    """
    if not product_id:
        raise ValueError("You must provide a product_id")
    profile_name = (vendor_id, product_id)
    if profile_name not in PROFILES:
        raise UnsupportedDevice(
            "The requested device is not supported (%x:%x)" % profile_name
        )
    return PROFILES[profile_name]


def _generate_profiles():
    """List devices imported in the current module and generates a separated
    profile for each device variation.

    :rtype: dict
    """
    from . import (  # noqa: F401
        aerox3,
        aerox3_wireless_wired,
        aerox3_wireless_wireless,
        aerox5,
        aerox5_wireless_wired,
        aerox5_wireless_wireless,
        aerox9_wireless_wired,
        aerox9_wireless_wireless,
        kanav2,
        kinzuv2,
        prime,
        prime_mini,
        prime_wireless_wired,
        prime_wireless_wireless,
        rival3,
        rival3_wireless,
        rival95,
        rival100,
        rival110,
        rival300,
        rival300s,
        rival310,
        rival500,
        rival600,
        rival650,
        rival700,
        sensei310,
        sensei_raw,
        sensei_ten,
    )

    profile_modules = locals()
    profiles = {}
    for item in profile_modules.values():
        for model in item.profile["models"]:
            profile = item.profile.copy()
            profile_name = (model["vendor_id"], model["product_id"])
            del profile["models"]
            for k, v in model.items():
                profile[k] = v
            profiles[profile_name] = profile
    return profiles


PROFILES = _generate_profiles()
