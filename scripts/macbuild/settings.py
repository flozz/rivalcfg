import tomllib

_BUILD_DIR = "./build/rivalcfg.macbuild"
_MACBUILD_DIR = "./scripts/macbuild"
_VERSION = tomllib.load(open("pyproject.toml", "rb"))["project"]["version"]
_OUTPUT_DIR_NAME = "rivalcfg-cli_v%s" % _VERSION

format = "UDZO"
files = [
    "/".join([_BUILD_DIR, _OUTPUT_DIR_NAME]),
    "/".join([_BUILD_DIR, _OUTPUT_DIR_NAME, "README.txt"]),
]
badge_icon = "/".join([_MACBUILD_DIR, "rivalcfg_badge.icns"])
