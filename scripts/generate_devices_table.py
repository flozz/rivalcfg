#!/usr/bin/env python

import sys
import types
import csv
import itertools

from rivalcfg import devices

DOC_DEVICES_BASE_URL = "https://flozz.github.io/rivalcfg/devices/"


def list_all_devices():
    devices = {}
    missing_pid_devices = []

    for dbname in ["other", "sse2.db", "sse3.db"]:
        with open("./ssdb/%s.csv" % dbname, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                device = {
                    "vid": row["vendor_id"].upper(),
                    "pid": row["product_id"].upper(),
                    "name": row["full_name"],
                }
                device_id = "%s:%s" % (device["vid"], device["pid"])
                if device["pid"]:
                    devices[device_id] = device
                else:
                    missing_pid_devices.append(device)
                if "dongle_product_id" in row and row["dongle_product_id"]:
                    device = {
                        "vid": row["vendor_id"].upper(),
                        "pid": row["dongle_product_id"].upper(),
                        "name": "%s (dongle)" % row["full_name"],
                    }
                    device_id = "%s:%s" % (device["vid"], device["pid"])
                    if device["pid"]:
                        devices[device_id] = device
                    else:
                        missing_pid_devices.append(device)

    return sorted(
        list(devices.values()) + missing_pid_devices,
        key=lambda item: item["name"],
    )


def list_supported_devices_by_families():
    supported_devices = {}
    for item in [getattr(devices, name) for name in dir(devices)]:
        if not isinstance(item, types.ModuleType):
            continue
        if not hasattr(item, "profile"):
            continue

        doc_name = (
            item.__name__.split(".")[-1]
            .replace("_wireless_wireless", "_wireless")
            .replace("_wired", "")
        )

        if item.profile["name"] not in supported_devices:
            supported_devices[item.profile["name"]] = []
        for model in item.profile["models"]:
            supported_devices[item.profile["name"]].append(
                {
                    "name": model["name"],
                    "vid": "%4X" % model["vendor_id"],
                    "pid": "%4X" % model["product_id"],
                    "url": DOC_DEVICES_BASE_URL + doc_name + ".html",
                }
            )
    for familly in supported_devices:
        supported_devices[familly] = sorted(
            supported_devices[familly],
            key=lambda item: item["name"],
        )
    return supported_devices


def generate_table_by_families(devices, indent=2, indent_level=0):
    result = '<table class="rivalcfg_devices">\n'
    for familly in devices:
        result += '\t<tr class="rivalcfg_devices_family">\n'
        result += '\t\t<td colspan="2"><strong>%s</strong></td>\n' % familly
        result += "\t</tr>\n"
        for device in devices[familly]:
            result += '\t<tr class="rivalcfg_devices_device">\n'
            result += '\t\t<td><a href="%s">%s</a></td>\n' % (
                device["url"],
                device["name"],
            )
            result += "\t\t<td><code>%s:%s</code></td>\n" % (
                device["vid"],
                device["pid"],
            )
            result += "\t</tr>\n"
    result += "</table>\n"
    result = result.replace("\t", " " * indent)
    return "\n".join(
        ["".join([" " * indent * indent_level, line]) for line in result.split("\n")]
    )


def generate_table(devices, indent=2, indent_level=0):
    result = '<table class="rivalcfg_devices">\n'
    for device in devices:
        result += '\t<tr class="rivalcfg_devices_device">\n'
        result += "\t\t<td>%s</td>\n" % device["name"]
        result += "\t\t<td><code>%s:%s</code></td>\n" % (
            device["vid"],
            device["pid"] or "????",
        )
        result += "\t</tr>\n"
    result += "</table>\n"
    result = result.replace("\t", " " * indent)
    return "\n".join(
        ["".join([" " * indent * indent_level, line]) for line in result.split("\n")]
    )


def main_supported():
    supported_devices = list_supported_devices_by_families()
    html = generate_table_by_families(supported_devices, indent=4, indent_level=1)
    print(".. raw:: HTML\n")
    print(html)


def main_unsupported():
    all_devices = list_all_devices()
    supported_devices = [
        "%s:%s" % (d["vid"].upper(), d["pid"].upper())
        for d in itertools.chain(*list_supported_devices_by_families().values())
    ]
    unsupported_devices = []
    for device in all_devices:
        device_id = "%s:%s" % (device["vid"], device["pid"])
        if device_id not in supported_devices:
            unsupported_devices.append(device)
    html = generate_table(unsupported_devices, indent=4, indent_level=1)
    print(".. raw:: HTML\n")
    print(html)


def main(args=sys.argv[1:]):
    if not args or args[0] not in ("supported", "unsupported"):
        print("USAGE:")
        print("  ./scripts/generate_devices_table.py <supported|unsuported>")
        sys.exit(1)

    if args[0] == "supported":
        main_supported()
    else:
        main_unsupported()


if __name__ == "__main__":
    main()
