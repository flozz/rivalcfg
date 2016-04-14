# rivalcfg: Configure SteelSeries Rival gaming mice

rivalcfg is a small CLI utility program that allows you to configure
SteelSeries Rival gaming mice on Linux.

Supported mice:

* ~~SteelSeries Rival~~ **WORK IN PROGRESS**
* SteelSeries Rival 100
* ~~SteelSeries Rival 300~~ **WORK IN PROGRESS**


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

Install `udev` rules to allow non-root users to configure the mouse (as root):

    cp extra/99-steelseries-rival-100.rules /etc/udev/rules.d/
    udevadm trigger


## CLI

    Usage: rivalcfg [options]

Main Options:

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -l, --list          print compatible mice and exit

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


## Changelog

* **2.0.0:** Refactored to support multiple mice
* **1.0.1:** Fixes the pypi package
* **1.0.0:** Initial release

