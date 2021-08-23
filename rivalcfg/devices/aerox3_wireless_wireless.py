from . import aerox3_wireless_wired


_WIRELESS_FLAG = 0b01000000


def _patch_command(info):
    # Copy the info dict
    result = dict(info)
    # Copy the command list
    result["command"] = list(result["command"])
    # Patch the command
    result["command"][0] = result["command"][0] | _WIRELESS_FLAG
    return result


profile = {
    "name": "SteelSeries Aerox 3 Wireless",
    "models": [
        {
            "name": "SteelSeries Aerox 3 Wireless (2.4 GHz wireless mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1838,
            "endpoint": 3,
        },
    ],
    "settings": {
        name: _patch_command(info)
        for name, info in aerox3_wireless_wired.profile["settings"].items()
    },
    "save_command": _patch_command(aerox3_wireless_wired.profile["save_command"]),
}
