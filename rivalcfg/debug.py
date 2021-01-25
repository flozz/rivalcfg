import sys
import os.path
import platform

from pkg_resources import get_distribution
from .version import VERSION
from . import udev


def _make_title(text):
    separator = "=" * len(text)
    return "\n%s\n%s\n" % (text.upper(), separator)


def _get_os_info():
    result = _make_title("Operating System")
    if platform.system() == "Linux":
        result += _get_os_linux_info()
    else:
        result += "OS: %s" % platform.system()
    return result


def _get_os_linux_info():
    result = ""
    result += "OS: %s\n" % platform.system()
    result += "Platform: %s\n" % platform.platform()
    result += "Version: %s\n" % platform.version()
    if os.path.isfile("/etc/issue"):
        try:
            # TODO use context (sinon HS pas content è_é)
            distro = open("/etc/issue", "r").read().strip()
            result += "Distribution issue: %s\n" % distro
        except Exception:
            pass
    return result


def _get_rivalcfg_info():
    result = _make_title("Rivalcfg")
    result += "Version: %s\n" % VERSION
    if platform.system() == "Linux":
        result += "udev rules installed: %a\n" % \
            os.path.isfile(udev.RULES_FILE_PATH)
        result += "udev rules up to date: %a\n" % \
            udev.is_rules_file_up_to_date()
    result += "Installation path: %s\n" % os.path.dirname(__file__)
    return result


def _get_python_info():
    result = _make_title("Python")
    result += "Python version: %d.%d.%d\n" % sys.version_info[:3]
    result += "HIDAPI version: %s\n" % get_distribution("hidapi").version
    return result


def get_debug_info():
    result = ""
    result += _get_rivalcfg_info()
    result += _get_os_info()
    result += _get_python_info()
    return result
