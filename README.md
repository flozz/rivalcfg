# rivalcfg: Configure SteelSeries Rival gaming mice

rivalcfg is a small CLI utility program that allows you to configure
SteelSeries Rival gaming mice on Linux.

Supported mice:

* SteelSeries Rival (experimental¹)
* SteelSeries Rival 100
* SteelSeries Rival 300 (experimental¹)

__experimental¹:__ I don't have this mouse so I am unable to test it. If you
have this mouse, please test all commands and report what is working or not by
openning an issue on Github: https://github.com/flozz/rivalcfg/issues


## Requirement

* Any Linux distribution that use `udev` (Debian, Ubuntu, ArchLinux,
  Fedora,...)
* [`pyudev`](https://pypi.python.org/pypi/pyudev)


## Installation

Clone the repositiory:

    git clone https://github.com/flozz/rivalcfg.git
    cd rivalcfg

Install rivalcfg (as root):

    pip install .

__NOTE:__ udev rules should be automatically installed, but if setup fails, you
should copy the rules manually: `cp rivalcfg/data/99-steelseries-rival.rules
/etc/udev/rules.d/` and then run the `udevadm trigger` command.


## CLI

    Usage: rivalcfg [options]

Main Options:

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -l, --list          print compatible mice and exit

SteelSeries Rival and Rival 300 Options:

    -c SET_LOGO_COLOR, --logo-color=SET_LOGO_COLOR
                        Set the logo backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -e SET_LOGO_LIGHT_EFFECT, --logo-light-effect=SET_LOGO_LIGHT_EFFECT
                        Set the logo light effect (values: 1, 2, 3, 4, breath,
                        steady, default: steady)
    -p SET_POLLING_RATE, --polling-rate=SET_POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SET_SENSITIVITY1, --sensitivity1=SET_SENSITIVITY1
                        Set sensitivity preset 1 (from 50 to 6500 in
                        increments of 50, default: 800)
    -S SET_SENSITIVITY2, --sensitivity2=SET_SENSITIVITY2
                        Set sensitivity preset 2 (from 50 to 6500 in
                        increments of 50, default: 1600)
    -C SET_WHEEL_COLOR, --wheel-color=SET_WHEEL_COLOR
                        Set the wheel backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -E SET_WHEEL_LIGHT_EFFECT, --wheel-light-effect=SET_WHEEL_LIGHT_EFFECT
                        Set the wheel light effect (values: 1, 2, 3, 4,
                        breath, steady, default: steady)
    -r, --reset         Reset all options to their factory values

SteelSeries Rival 100 Options:

    -b SET_BTN6_ACTION, --btn6-action=SET_BTN6_ACTION
                        Set the action of the button under the wheel (values:
                        default, os, default: default)
    -c SET_COLOR, --color=SET_COLOR
                        Set the mouse backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #00FFFF)
    -e SET_LIGHT_EFFECT, --light-effect=SET_LIGHT_EFFECT
                        Set the light effect (values: 1, 2, 3, 4, breath,
                        steady, default: steady)
    -p SET_POLLING_RATE, --polling-rate=SET_POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SET_SENSITIVITY1, --sensitivity1=SET_SENSITIVITY1
                        Set sensitivity preset 1 (values: 250, 500, 1000,
                        1250, 1500, 1750, 2000, 4000, default: 1000)
    -S SET_SENSITIVITY2, --sensitivity2=SET_SENSITIVITY2
                        Set sensitivity preset 2 (values: 250, 500, 1000,
                        1250, 1500, 1750, 2000, 4000, default: 2000)
    -r, --reset         Reset all options to their factory values


## Debug

* `DEBUG_DRY=true`: Dry run (simulate commands, do not write anything to the
  device).
* `DEBUG_MOUSE=<VendorID>:<ProductId>`: Force to load the corresponding
  profile.

Example:

    DEBUG_DRY=true DEBUG_MOUSE=1038:1384 rivalcfg -c ff3300

Result:

    [DEBUG] Debugging rivalcfg 2.0.0...
    [DEBUG] Dry run enabled
    [DEBUG] Debugging mouse profile 1038:1384
    [DEBUG] Mouse profile found: SteelSeries Rival
    [DEBUG] _device_write: 08 01 FF 33 00
    [DEBUG] _device_write: 09 00


## Changelog

* **2.2.0:** Experimental Rival 300 support
* **2.1.1:** Includes udev rules in the package and automatically install the
  rules (if possible)
* **2.1.0:** Experimental Original Rival support
* **2.0.0:** Refactored to support multiple mice
* **1.0.1:** Fixes the pypi package
* **1.0.0:** Initial release

