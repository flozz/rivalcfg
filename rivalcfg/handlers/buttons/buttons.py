"""
TODO
"""


# import argparse

# from ...helpers import merge_bytes
# from ...helpers import parse_param_string, REGEXP_PARAM_STRING
from . import layout_multimedia
from . import layout_qwerty


#: Available layouts
LAYOUTS = {
    "qwerty": layout_qwerty,
    # TODO azerty
}


# Compatibility with Python 2.7.
# On Python 2 the type is 'unicode'
# On Python 3 the type is 'str'
_unicode_type = type(u"")


def build_layout(layout):
    """Generates an usable layout from a layout module containing key mapping
    and aliases.

    :param module layout: The layour (e.g.
                          ``rivalcfg.handler.buttons.layout_qwerty``)
    :rtype dict:
    """
    full_layout = {k.lower(): v for k, v in layout.layout.items()}

    for alias, ref in layout.aliases.items():
        if ref not in layout.layout:
            raise ValueError("Wrong alias: '%s' aliases '%' but '%s' is not in the layout" % (  # noqa
                alias, ref, ref))
        full_layout[alias.lower()] = layout.layout[ref]

    return full_layout


def process_value(setting_info, colors):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "rgbcolor" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    :param str,tuple,list,dict colors: The color(s).
    :rtype: [int]
    """
    pass  # TODO


def add_cli_option(cli_parser, setting_name, setting_info):
    """Add the given "rgbgradient" type setting to the given CLI arguments parser.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param str setting_name: The name of the setting.
    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    print(build_layout(layout_qwerty))  # XXX
    description = "%s (default: %s)" % (
            setting_info["description"],
            str(setting_info["default"]).replace("%", "%%"),
            )
    cli_parser.add_argument(
            *setting_info["cli"],
            dest=setting_name,
            help=description,
            type=str,
            # action=CheckButtonsAction,
            metavar=setting_name.upper()
            )
