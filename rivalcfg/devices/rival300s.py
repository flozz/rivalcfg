from . import rival110


# This device looks like a Rival 300 but works like a Rival 110
profile = {
    "name": "SteelSeries Rival 300S",
    "models": [
        {
            "name": "SteelSeries Rival 300S",
            "vendor_id": 0x1038,
            "product_id": 0x1810,
            "endpoint": 0,
        }
    ],
    "settings": rival110.profile["settings"],
    "save_command": rival110.profile["save_command"],
}
