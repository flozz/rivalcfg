#!/usr/bin/env python

import types

from rivalcfg import devices


def list_devices():
    result = ""
    for item in [getattr(devices, name) for name in dir(devices)]:
        if not isinstance(item, types.ModuleType):
            continue
        if not hasattr(item, "profile"):
            continue
        result += "\n%s:\n\n" % item.profile["name"]
        result += "+%s+%s+\n" % (
            "-" * 62,
            "-" * 11,
        )
        for model in item.profile["models"]:
            result += "| %-60s | %04x:%04x |\n" % (
                model["name"],
                model["vendor_id"],
                model["product_id"],
            )
            result += "+%s+%s+\n" % (
                "-" * 62,
                "-" * 11,
            )
    return result


def patch_readme(
    text="",
    readme="README.rst",
    start="devices-list-start",
    end="devices-list-end",
):
    result = ""
    in_marker = False

    with open(readme, "r") as file_:
        for line in file_:
            if end in line:
                result += "\n"
                in_marker = False
            if not in_marker:
                result += line
            if start in line:
                in_marker = True
                result += text

    return result


if __name__ == "__main__":
    lst = list_devices()
    readme = patch_readme(lst)
    with open("README.rst", "w") as file_:
        file_.write(readme)
