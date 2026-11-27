from . import aerox5_wireless_wired

_READBACK_LENGTH = 64


def _patch_command(info):
    # Copy the info dict
    result = dict(info)
    # The mouse answers to every command: the response must be read to not
    # confuse it with the response of the next command
    result["readback_length"] = _READBACK_LENGTH
    return result


profile = {
    "name": "SteelSeries Aerox 5 Wireless",
    "models": [
        {
            "name": "SteelSeries Aerox 5 Wireless (Bluetooth mode)",
            # The mouse does not use the SteelSeries vendor id over Bluetooth
            "vendor_id": 0x0111,
            "product_id": 0x1854,
            # There is no endpoint number over Bluetooth, the device is
            # searched by usage page instead
            "endpoint": 0,
            "usage_page": 0xFFC0,
            "report_id": 0x04,
        },
    ],
    "settings": {
        name: _patch_command(info)
        for name, info in aerox5_wireless_wired.profile["settings"].items()
    },
    "battery_level": aerox5_wireless_wired.profile["battery_level"],
    "save_command": _patch_command(aerox5_wireless_wired.profile["save_command"]),
}
