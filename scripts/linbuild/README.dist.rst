Rivalcfg Standalone Build for Linux
-----------------------------------

Rivalcfg is a CLI utility program that allows you to configure SteelSeries
gaming mice.

* Website: https://rivalcfg.flozz.org/
* Documentation: https://flozz.github.io/rivalcfg/
* Source code: https://github.com/flozz/rivalcfg/

This is a standalone (compiled) version of Rivalcfg for Linux. You can use it
without installing any dependencies.


Usage
-----

To use it, first extract the archive::

    tar -xvzf rivalcfg-cli_v*_linux_*.tar.gz

Then go to the extracted folder::

    cd rivalcfg-cli_v*_linux_*

Then install the udev rules to allow regular users to configure the devices (run
as root)::

    sudo ./rivalcfg --update-udev

Finally, you can run Rivalcfg::

    ./rivalcfg --help
