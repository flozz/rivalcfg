import sys
import argparse

from . import cli


def main(args):
    cli_parser = argparse.ArgumentParser(prog="rivalcfg")
    cli.add_main_cli(cli_parser)
    from . import devices  # FIXME
    mouse_profile = devices.get_profile(product_id=0x1702)  # FIXME
    cli.add_mouse_cli(cli_parser, mouse_profile)  # FIXME
    params = cli_parser.parse_args(args)
    print(params)


if __name__ == "__main__":
    main(sys.argv[1:])
