# rivalcfg: Configure SteelSeries Rival gaming mice

[![Build Status](https://travis-ci.org/flozz/rivalcfg.svg?branch=master)](https://travis-ci.org/flozz/rivalcfg)
[![PYPI Version](https://img.shields.io/pypi/v/rivalcfg.svg)](https://pypi.python.org/pypi/rivalcfg)
[![License](https://img.shields.io/pypi/l/rivalcfg.svg)](https://github.com/flozz/rivalcfg/blob/master/LICENSE)

rivalcfg is a small CLI utility program that allows you to configure
SteelSeries Rival gaming mice on Linux.

Supported mice:

* SteelSeries Rival _(1038:1384)_
* SteelSeries Rival 100 _(1038:1702)_
* SteelSeries Rival 300 _(1038:1710)_
* SteelSeries Rival 300 CS:GO Fade Edition _(1038:1394)_

If you have trouble running this software, please open an issue on Github:

* https://github.com/flozz/rivalcfg/issues


## Requirement

* Any Linux distribution that use `udev` (Debian, Ubuntu, ArchLinux,
  Fedora,...)
* [`pyudev`](https://pypi.python.org/pypi/pyudev)


## Installation

### From PYPI

Run the following command (as root):

    pip install rivalcfg

### From sources

Clone the repositiory:

    git clone https://github.com/flozz/rivalcfg.git
    cd rivalcfg

Install rivalcfg (as root):

    pip install .

__NOTE:__ udev rules should be automatically installed, but if setup fails, you
should copy the rules manually: `cp rivalcfg/data/99-steelseries-rival.rules
/etc/udev/rules.d/` and then run the `udevadm trigger` command.

### From Arch Linux AUR package

Use package [rivalcfg-git](https://aur.archlinux.org/packages/rivalcfg-git)


## CLI

    Usage: rivalcfg [options]

Main Options:

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -l, --list          print compatible mice and exit

SteelSeries Rival and Rival 300 Options:

    -c LOGO_COLOR, --logo-color=LOGO_COLOR
                        Set the logo backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -e LOGO_LIGHT_EFFECT, --logo-light-effect=LOGO_LIGHT_EFFECT
                        Set the logo light effect (values: 1, 2, 3, 4, breath,
                        steady, default: steady)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (from 50 to 6500 in
                        increments of 50, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (from 50 to 6500 in
                        increments of 50, default: 1600)
    -C WHEEL_COLOR, --wheel-color=WHEEL_COLOR
                        Set the wheel backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -E WHEEL_LIGHT_EFFECT, --wheel-light-effect=WHEEL_LIGHT_EFFECT
                        Set the wheel light effect (values: 1, 2, 3, 4,
                        breath, steady, default: steady)
    -r, --reset         Reset all options to their factory values

SteelSeries Rival 100 Options:

    -b BTN6_ACTION, --btn6-action=BTN6_ACTION
                        Set the action of the button under the wheel (values:
                        default, os, default: default)
    -c COLOR, --color=COLOR
                        Set the mouse backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #00FFFF)
    -e LIGHT_EFFECT, --light-effect=LIGHT_EFFECT
                        Set the light effect (values: 1, 2, 3, 4, breath,
                        steady, default: steady)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (values: 250, 500, 1000,
                        1250, 1500, 1750, 2000, 4000, default: 1000)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (values: 250, 500, 1000,
                        1250, 1500, 1750, 2000, 4000, default: 2000)
    -r, --reset         Reset all options to their factory values

SteelSeries Rival 300 CS:GO Fade Edition Options:

    -b BTN6_ACTION, --btn6-action=BTN6_ACTION
                        Set the action of the button under the wheel (values:
                        default, os, default: default)
    -c LOGO_COLOR, --logo-color=LOGO_COLOR
                        Set the logo backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF5200)
    -e LOGO_LIGHT_EFFECT, --logo-light-effect=LOGO_LIGHT_EFFECT
                        Set the logo light effect (values: breathfast,
                        breathmed, breathslow, steady, 1, 2, 3, 4, default:
                        steady)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (from 50 to 6500 in
                        increments of 50, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (from 50 to 6500 in
                        increments of 50, default: 1600)
    -C WHEEL_COLOR, --wheel-color=WHEEL_COLOR
                        Set the wheel backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF5200)
    -E WHEEL_LIGHT_EFFECT, --wheel-light-effect=WHEEL_LIGHT_EFFECT
                        Set the wheel light effect (values: breathfast,
                        breathmed, breathslow, steady, 1, 2, 3, 4, default:
                        steady)
    -r, --reset         Reset all options to their factory values


## FAQ (Frequently Asked Questions)

### How can I turn the lights off

You can turn the lights off by setting the black color to the lights.

Example with Rival 100:

    rivalcfg --color=black

Example with Rival, Rival 300:

    rivalcfg --logo-color=black --wheel-color=black


## Debug

* `DEBUG_DRY=true`: Dry run (simulate commands, do not write anything to the
  device).
* `DEBUG_PROFILE=<VendorID>:<ProductId>`: Force to load the corresponding
  profile.
* `DEBUG_DEVICE=<VendorID>:<ProductId>` Force to use the specified USB device
  instead of the one that matches the profile

Example:

    DEBUG_DRY=true DEBUG_PROFILE=1038:1384 rivalcfg -c ff3300

Result:

    [DEBUG] Debugging rivalcfg 2.0.0...
    [DEBUG] Dry run enabled
    [DEBUG] Debugging mouse profile 1038:1384
    [DEBUG] Mouse profile found: SteelSeries Rival
    [DEBUG] _device_write: 08 01 FF 33 00
    [DEBUG] _device_write: 09 00


## Changelog

* **2.5.0:** Rival 300 CS:GO Fade Edition support (thanks @Percinnamon, #20)
* **2.4.4:** Improves debug options
* **2.4.3:** Fixes an issue with Python 3 (#8)
* **2.4.2:** Fixes a TypeError with Python 3 (#7)
* **2.4.1:** Help improved
* **2.4.0:** Python 3 support (#4)
* **2.3.0:**
  * Rival and Rival 300 support is no more experimental
  * Improves the device listing (--list)
  * Fixes bug with color parsing in CLI (#1)
  * Fixes unrecognized devices path on old kernel (#2)
* **2.2.0:** Experimental Rival 300 support
* **2.1.1:** Includes udev rules in the package and automatically install the
  rules (if possible)
* **2.1.0:** Experimental Original Rival support
* **2.0.0:** Refactored to support multiple mice
* **1.0.1:** Fixes the pypi package
* **1.0.0:** Initial release
