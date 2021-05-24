from importlib import import_module

from docutils.parsers.rst import Directive
from docutils import nodes
from docutils.parsers.rst.directives.tables import ListTable


class RivalcfgDeviceFamily(ListTable, Directive):
    required_arguments = 1
    has_content = False

    def _generate_model_table(self, profile):
        table_data = []

        for model in profile["models"]:
            table_data.append(
                [
                    nodes.paragraph(text=model["name"]),
                    nodes.paragraph(
                        text="%04x:%04x" % (model["vendor_id"], model["product_id"])
                    ),
                ]
            )

        return self.build_table_from_list(table_data, [1] * 2, 0, 0)

    def run(self):
        device_family = self.arguments[0]
        profile = import_module("rivalcfg.devices.%s" % device_family).profile

        table = self._generate_model_table(profile)

        return [table]


def setup(app):
    app.add_directive("rivalcfg_device_family", RivalcfgDeviceFamily)
