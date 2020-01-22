# rivalcfg: Configure SteelSeries gaming mice

[![Build Status](https://travis-ci.org/flozz/rivalcfg.svg?branch=master)](https://travis-ci.org/flozz/rivalcfg)
[![PYPI Version](https://img.shields.io/pypi/v/rivalcfg.svg)](https://pypi.python.org/pypi/rivalcfg)
[![License](https://img.shields.io/pypi/l/rivalcfg.svg)](https://github.com/flozz/rivalcfg/blob/master/LICENSE)
[![Gitter](https://badges.gitter.im/gitter.svg)](https://gitter.im/rivalcfg/Lobby)

rivalcfg is a small CLI utility program that allows you to configure
SteelSeries Rival gaming mice on Linux and Windows (probably works on BSD and
Mac OS too, but not tested).

Supported mice:

* SteelSeries Rival _(1038:1384)_
* SteelSeries Rival 100 _(1038:1702)_
* SteelSeries Rival 100 Dota 2 Edition _(1038:170c)_
* SteelSeries Rival 110 _(1038:1729)_
* SteelSeries Rival 300 _(1038:1710)_
* Acer Predator Gaming Mouse (Rival 300) _(1038:1714)_
* SteelSeries Rival 300 CS:GO Fade Edition _(1038:1394)_
* SteelSeries Rival 300 CS:GO Hyperbeast Edition _(1038:171a)_
* SteelSeries Rival 300 Dota 2 Edition _(1038:1392)_
* SteelSeries Rival 300 HP Omen Edition _(1038:1718)_
* SteelSeries Heroes of the Storm (Sensei Raw) _(1038:1390)_
* SteelSeries Kana V2 _(1038:137a)_

Experimental support:

* SteelSeries Rival 310 _(1038:1720)_
* SteelSeries Rival 500 _(1038:170e)_
* SteelSeries Rival 600 _(1038:1724)_
* SteelSeries Rival 710 _(1038:1730)_

If you have trouble running this software, please open an issue on Github:

* https://github.com/flozz/rivalcfg/issues


## Requirement

* Any Linux distribution that use `udev` (Debian, Ubuntu, ArchLinux,
  Fedora,...) or Windows
* [hidapi](https://pypi.python.org/pypi/hidapi/0.7.99.post20)


## Installation

### Prerequisites

**Linux:**

Installation require a compilation toolchain and python headers to compile
`hidapi`. On Debian / Ubuntu, this can be installed with the following command
(as root):

    apt-get install build-essential python-dev libusb-1.0-0-dev libudev-dev

**Windows:**

On Windows, you have to install first:

* Python 3.6 or 2.7: https://www.python.org/
* Visual C++ 2015 Build Tools: http://landinghub.visualstudio.com/visual-cpp-build-tools

### Installing From PYPI

Run the following command (as root):

    pip install rivalcfg

### Installing From sources

Clone the repositiory:

    git clone https://github.com/flozz/rivalcfg.git
    cd rivalcfg

Install rivalcfg (as root):

    pip install .

__NOTE:__ udev rules should be automatically installed, but if setup fails, you
should copy the rules manually: `cp rivalcfg/data/99-steelseries-rival.rules
/etc/udev/rules.d/` and then run the `udevadm trigger` command.

### Archlinux AUR package

Use package [rivalcfg-git](https://aur.archlinux.org/packages/rivalcfg-git)


## CLI

    Usage: rivalcfg [options]

Main Options:

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -l, --list          print compatible mice and exit

SteelSeries Rival 100 (all editions) Options:

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

SteelSeries Rival 110 Options:

    -b BTN6_ACTION, --btn6-action=BTN6_ACTION
                        Set the action of the button under the wheel (values:
                        default, os, default: default)
    -c COLOR, --color=COLOR
                        Set the mouse backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #00FFFF)
    -e LIGHT_EFFECT, --light-effect=LIGHT_EFFECT
                        Set the light effect (values: steady, breath, 1, 2, 3,
                        4, default: steady)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (values: 200, 300, 400, 500,
                        600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400,
                        1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300,
                        2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200,
                        3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100,
                        4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000,
                        5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900,
                        6000, 6100, 6200, 6300, 6400, 6500, 6600, 6700, 6800,
                        6900, 7000, 7100, 7200, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (values: 200, 300, 400, 500,
                        600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400,
                        1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300,
                        2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200,
                        3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100,
                        4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000,
                        5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900,
                        6000, 6100, 6200, 6300, 6400, 6500, 6600, 6700, 6800,
                        6900, 7000, 7100, 7200, default: 1600)
    -r, --reset         Reset all options to their factory values

SteelSeries Rival and Rival 300 (all editions) Options:

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

SteelSeries Rival 310 Options (Experimental):

    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (from 100 to 12000 in
                        increments of 100, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (from 100 to 12000 in
                        increments of 100, default: 1600)

SteelSeries Rival 500 Options (Experimental):

    -c LOGO_COLOR, --logo-color=LOGO_COLOR
                        Set the logo backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -t COLOR1 COLOR2 SPEED, --logo-colorshift=COLOR1 COLOR2 SPEED
                        Set the logo backlight color (e.g. red aqua 200,
                        ff0000 00ffff 200, default: #FF1800 #FF1800 200)
    -C WHEEL_COLOR, --wheel-color=WHEEL_COLOR
                        Set the wheel backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -T COLOR1 COLOR2 SPEED, --wheel-colorshift=COLOR1 COLOR2 SPEED
                        Set the wheel backlight color (e.g. red aqua 200,
                        ff0000 00ffff 200, default: #FF1800 #FF1800 200)
    -r, --reset         Reset all options to their factory values

SteelSeries Rival 600 Options (Experimental):

    -2 LEFT_STRIP_BOTTOM_COLOR, --lstrip-bottom-color=LEFT_STRIP_BOTTOM_COLOR
                        Set the color(s) and effects of the left LED strip
                        bottom section (e.g. red, #ff0000, ff0000, #f00, f00).
                        If more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -1 LEFT_STRIP_MID_COLOR, --lstrip-mid-color=LEFT_STRIP_MID_COLOR
                        Set the color(s) and effects of the left LED strip
                        middle section (e.g. red, #ff0000, ff0000, #f00, f00).
                        If more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -0 LEFT_STRIP_TOP_COLOR, --lstrip-top-color=LEFT_STRIP_TOP_COLOR
                        Set the color(s) and effects of the left LED strip
                        upper section (e.g. red, #ff0000, ff0000, #f00, f00).
                        If more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -c LOGO_COLOR, --logo-color=LOGO_COLOR
                        Set the logo backlight color(s) and effects (e.g. red,
                        #ff0000, ff0000, #f00, f00). If more than one value is
                        specified, a color shifting effect is set (e.g.
                        x,x,red,0,green,54,blue,54) syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -5 RIGHT_STRIP_BOTTOM_COLOR, --rstrip-bottom-color=RIGHT_STRIP_BOTTOM_COLOR
                        Set the color(s) and effects of the right LED strip
                        bottom section (e.g. red, #ff0000, ff0000, #f00, f00).
                        If more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -4 RIGHT_STRIP_MID_COLOR, --rstrip-mid-color=RIGHT_STRIP_MID_COLOR
                        Set the color(s) and effects of the right LED strip
                        mid section (e.g. red, #ff0000, ff0000, #f00, f00). If
                        more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -3 RIGHT_STRIP_TOP_COLOR, --rstrip-top-color=RIGHT_STRIP_TOP_COLOR
                        Set the color(s) and effects of the right LED strip
                        upper section (e.g. red, #ff0000, ff0000, #f00, f00).
                        If more than one value is specified, a color shifting
                        effect is set (e.g. x,x,red,0,green,54,blue,54)
                        syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (from 100 to 12000 in
                        increments of 100, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (from 100 to 12000 in
                        increments of 100, default: 1600)
    -C WHEEL_COLOR, --wheel-color=WHEEL_COLOR
                        Set the wheel backlight color(s) and effects (e.g.
                        red, #ff0000, ff0000, #f00, f00). If more than one
                        value is specified, a color shifting effect is set
                        (e.g. x,x,red,0,green,54,blue,54) syntax:
                        time(ms),trigger_mask,color1,pos1,...,colorn,posn
    -r, --reset         Reset all options to their factory values

SteelSeries Rival 710 Options (Experimental):

    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (from 100 to 12000 in
                        increments of 100, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (from 100 to 12000 in
                        increments of 100, default: 1600)
    -c LOGO_COLOR, --logo-color=LOGO_COLOR
                        Set the logo backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)
    -C WHEEL_COLOR, --wheel-color=WHEEL_COLOR
                        Set the wheel backlight color (e.g. red, #ff0000,
                        ff0000, #f00, f00, default: #FF1800)

SteelSeries Kana V2 Options:

    -i LED_INTENSITY1, --intensity1=LED_INTENSITY1
                        Set LED intensity preset 1 (values: high, medium, off,
                        low, default: off)
    -I LED_INTENSITY2, --intensity2=LED_INTENSITY2
                        Set LED intensity preset 2 (values: high, medium, off,
                        low, default: high)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                        Set polling rate in Hz (values: 125, 250, 500, 1000,
                        default: 1000)
    -s SENSITIVITY1, --sensitivity1=SENSITIVITY1
                        Set sensitivity preset 1 (values: 400, 800, 1200,
                        1600, 2000, 2400, 3200, 4000, default: 800)
    -S SENSITIVITY2, --sensitivity2=SENSITIVITY2
                        Set sensitivity preset 2 (values: 400, 800, 1200,
                        1600, 2000, 2400, 3200, 4000, default: 1600)
    -r, --reset         Reset all options to their factory values


## FAQ (Frequently Asked Questions)

### How can I dim the brightness of the lights

Lights are configured via RGB color, so to have a lower brightness, just set a darker color (e.g. `#880000` instead of `#FF0000` for a darker red).

### How can I turn the lights off?

You can turn the lights off by setting the black color to the lights.

Example with Rival 100:

    rivalcfg --color=black

Example with Rival, Rival 300:

    rivalcfg --logo-color=black --wheel-color=black

### I have a "Permission denied" error, what can I do?

If you have an error like

    IOError: [Errno 13] Permission denied: u'/dev/hidrawXX'

this means that the udev rules have not been installed with the software. This
can be fixed using the following commands (as root):

    wget https://raw.githubusercontent.com/flozz/rivalcfg/master/rivalcfg/data/99-steelseries-rival.rules -O /etc/udev/rules.d/99-steelseries-rival.rules

    sudo udevadm trigger


## Debug

Rivalcfg uses several environment variable to enable different debug features:

* `RIVALCFG_DEBUG=1`: Enable debug. Setting this variable will allow rivalcfg
  to write debug information to stdout.

* `RIVALCFG_DRY=1` Enable dry run. Setting this variable will avoid rivalcfg to
  write anything to a real device plugged to the computer (i any). It will
  instead simulate the device, so it can be used to make test on mice that are
  not plugged to the computer if used in conjunction to the `RIVALCFG_PROFILE`
  variable.

* `RIVALCFG_PROFILE=<VendorID>:<ProductID>`: Forces rivalcfg to load the
  corresponding profile instead of the one of the plugged device (if any).

* `RIVALCFG_DEVICE=<VendorID>:<ProductID>`: Forces rivalcfg to write bytes to
  this device, even if it is not matching the selected profile.

**Example: debug logging only:**

    $ RIVALCFG_DEBUG=1  rivalcfg --list

**Example: dry run on Rival 300 profile:**

    $ RIVALCFG_DRY=1 RIVALCFG_PROFILE=1038:1710  rivalcfg -c ff1800

**Example: using Rival 300 command set on Rival 300 CS:GO Fade Editon mouse:**

    $ RIVALCFG_PROFILE=1038:1710     RIVALCFG_DEVICE=1038:1394    rivalcfg -c ff1800
    # ↑ selects "Rival 300" profile  ↑ but write on the "Rival 300 CS:GO Fade Edition" device

**Example debug output:**

    [DEBUG] Rivalcfg 2.5.3
    [DEBUG] Python version: 2.7.13
    [DEBUG] OS: Linux
    [DEBUG] Linux distribution: Ubuntu 17.04 zesty
    [DEBUG] Dry run enabled
    [DEBUG] Forced profile: 1038:1710
    [DEBUG] Targeted device: 1038:1710
    [DEBUG] Selected mouse: <Mouse SteelSeries Rival 300 (1038:1710:00)>
    [DEBUG] Mouse._device_write: 00 08 01 FF 18 00
    [DEBUG] Mouse._device_write: 00 09 00


## Changelog

* **3.7.0:** Initial support of the Rival 710 (#91, thanks @mobaradev)
* **3.6.1:** Removes the call of a deprecated function that have been removed from Python 3.8 (#86)
* **3.6.0:** Improved error handeling when sending commands to mice (thanks @Demon000, #76)
* **3.5.0:** Support of the Rival 100 Dota 2 Edition (#75)
* **3.4.0:** Support of the Kana V2 mouse (thanks @pqlaz, #74)
* **3.3.0:** Support of the Acer Predator Gaming Mouse (a rebranded Rival 300) (#72)
* **3.2.0:**
  * Support of the Rival 300 Dota 2 Edition (#67, @virrim)
  * Fixes case issue in udev rule file (#68, @hungarian-notation)
* **3.1.0:**
  * Support of sensitivity commands for Rival 500 (#65, @hungarian-notation)
  * Fix of the reset command on Rival 600 (#66, @ergor)
* **3.0.0**:
  * Adds support of the Rival 300 HP Omen Edition (#52, @FadedCoder)
  * Adds experimental support of the Rival 600 (#60, @ergor)
  * Varous fixes
* **3.0.0-beta1:**
  * Support of the Rival 110
  * Support of the Heroes of the Storm (Sensei Raw)
  * Partial support of the Rival 310
  * Partial support of the Rival 500
  * Microsoft Windows (and Mac OS?) support
  * rivalcfg now uses the `hidapi` lib instead of manipulating udev directly
  * Code refactored (almost all API changed)
  * Various bug fixes
* **2.6.0:** Add CS:GO Hyperbeast Edition support (thanks @chriscoyfish, #33)
* **2.5.3:** Minor typo fixes for cli (thanks @chriscoyfish, #31)
* **2.5.2:** Fixes Rival 300 with updated firmware not working (#5, #25, #28, special thanks to @Thiblizz)
* **2.5.1:** Fixes mouse not recognized on system with more than 10 USB busses (#21)
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
