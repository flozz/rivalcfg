#!/usr/bin/env python3

import sys

from rivalcfg.__main__ import main


def usage():
    print("Rivalcfg is a command-line application, you must run it from a terminal.")
    print("See the README.txt file for more information.")
    print()
    print("USAGE:")
    print("  .\\rivalcfg.exe --help")
    print()
    input("Press <Enter> to continue...")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    main()
