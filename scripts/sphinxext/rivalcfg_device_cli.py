import os
import subprocess
from importlib import import_module

from docutils.parsers.rst import Directive
from docutils import nodes


class RivalcfgDeviceCLI(Directive):
    required_arguments = 1
    has_content = False

    def run(self):
        device_family = self.arguments[0]

        if device_family.lower() == "none":
            device_id = "0000:0000"
        else:
            profile = import_module("rivalcfg.devices.%s" % device_family).profile
            device_id = "%04x:%04x" % (
                profile["models"][0]["vendor_id"],
                profile["models"][0]["product_id"],
            )

        os.environ["RIVALCFG_DRY"] = "1"
        os.environ["RIVALCFG_PROFILE"] = device_id
        usage = subprocess.check_output(["python", "-m", "rivalcfg", "--help"])
        usage = usage.decode("utf-8")

        return [nodes.literal_block(text=usage, language="text")]


def setup(app):
    app.add_directive("rivalcfg_device_cli", RivalcfgDeviceCLI)
