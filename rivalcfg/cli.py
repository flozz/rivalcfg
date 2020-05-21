"""
This module generates rivalcfg's CLI.
"""


from . import handlers


def normalize_cli_option_name(name):
    """Helper function to transform a setting name to a cli option.

    :param str name: The setting name.
    :rtype: str

    >>> normalize_cli_option_name("My_Test_Setting1")
    'my-test-setting1'
    """
    return name.lower().replace("_", "-")


def add_main_cli(cli_parser):
    """Adds the main CLI options.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    """
    # TODO --list
    # TODO --print-info
    pass


def add_mouse_cli(cli_parser, mouse_profile):
    """Adds the CLI options for the given mouse profile.

    :param ArgumentParser cli_parser: An :class:`ArgumentParser` instance.
    :param mouse_profile: One of the rivalcfg mouse profile (provided by
                            :func:`rivalcfg.devices.get_profile`).
    """
    cli_group = cli_parser.add_argument_group(
            "%s Options" % mouse_profile["name"])
    for setting_name, setting_info in mouse_profile["settings"].items():
        handler = getattr(handlers, setting_info["value_type"])
        handler.add_cli_option(cli_group, setting_name, setting_info)
