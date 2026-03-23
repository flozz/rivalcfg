Environment Variables
=====================

Some environment variables can be used to change the behaviour of Rivalcfg. Here is a list with explanations.


RIVALCFG_DRY
------------

This variable allows to test commands without sending anything to a real device. This is used for testing and debug.

Usage::

    RIVALCFG_DRY=1


RIVALCFG_DEBUG_NO_COMMAND_DELAY
-------------------------------

When set, this remove the delay between commands. This is only usefull to allow tests to run faster, you may not use this with real devices, they may hang or even crash. See :py:attr:`~rivalcfg.mouse.Mouse.command_delay`.


RIVALCFG_DEBUG_PRINT_HID_REPORT
-------------------------------

When set, Rivalcfg will print bytes sent to and received from the USB devices, in hexadecimal.

Example output::

    [USBHID]< 02 00 | 0B 00 02 01 12 24
    [USBHID]< 02 00 | 04 00 01
    [USBHID]< 02 00 | 05 00 01 FF 00 00 64
    [USBHID]< 02 00 | 05 00 02 00 FF 00 64
    [USBHID]< 02 00 | 05 00 03 00 00 FF 64
    [USBHID]< 02 00 | 05 00 04 80 00 80 64
    [USBHID]< 02 00 | 06 00 04
    [USBHID]< 02 00 | 07 00 01 00 02 00 03 00 04 00 05 00 30 00 31 00 32 00
    [USBHID]< 02 00 | 09 00
    [USBHID]< 02 00 | 10 00
    [USBHID]>       | 24 00

Lines starting with ``[USBHID]<`` are bytes sent to the device, and the ones starting with ``[USBHID]>`` are bytes received from the device.

For lines sent to the devices, the two first bytes (before the pipe ``|``) is the ``wValue`` field, defining the report type (``02`` for *output*, ``03`` for *feature*) and report ID (always ``00`` on SteelSeries devices).


RIVALCFG_PROFILE
----------------

This variable can be used to force loading a specific device profile. This is used for testing and debug. You may want to use ``RIVALCFG_DRY`` too when using this variable.

Usage::

    RIVALCFG_PROFILE=<VendorId>:<ProductId>

For example, to load the Rival 100 profile and list its CLI options::

    RIVALCFG_PROFILE=1038:1702 RIVALCFG_DRY=1 rivalcfg --help

