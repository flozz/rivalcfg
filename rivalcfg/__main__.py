import sys

from . import cli
from . import list_available_mice, get_mouse


def get_first_available_mouse():
    available_mice = list(list_available_mice())
    if not available_mice:
        return None
    return get_mouse(
            available_mice[0].vendor_id,
            available_mice[0].product_id
            )


def main(argv):
    mouse = get_first_available_mouse()
    profile = mouse.profile if mouse else None
    parser = cli.generate_cli(profile)
    options, args = parser.parse_args(argv)
    print options
    print args
    pass


if __name__ == "__main__":
    main(sys.argv)

