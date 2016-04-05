# rivalcfg: Configure the SteelSeries Rival 100 gaming mouse

rivalcfg is a small CLI utility program that allows you to configure
the SteelSeries Rival 100 gaming mouse on Linux.


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

    Options:
    -h, --help            show this help message and exit
    -s SENSITIVITY, --sensitivity1=SENSITIVITY
                            Set sensitivity preset 1 (allowed values are 250, 500,
                            1000, 1250, 1500, 1750, 2000 and 4000; default value
                            is 1000)
    -S SENSITIVITY, --sensitivity2=SENSITIVITY
                            Set sensitivity preset 2 (allowed values are 250, 500,
                            1000, 1250, 1500, 1750, 2000 and 4000; default value
                            is 2000)
    -p POLLING_RATE, --polling-rate=POLLING_RATE
                            Set polling rate in Hz (allowed values are 125, 250,
                            500 and 1000; default value is 1000)
    -c COLOR, --color=COLOR
                            Set the mouse backlight color (color can be an
                            hexadecimal color or a nammed color; e.g. ff0000, f00,
                            #ff0000, #f00, red,...)
    -e LIGHT_EFFECT, --light-effect=LIGHT_EFFECT
                            Set the light effect (allowed values are 1 or static,
                            2, 3 or breath, 4)
    -b ACTION, --btn6-action=ACTION
                            Set the action of the button under the wheel (allowed
                            values are default and os)
    -r, --reset           Reset all options to their default values

