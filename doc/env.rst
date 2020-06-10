Environment Variables
=====================

Some environment variables can be used to change the behaviour of Rivalcfg. Here is a list with explanations.


RIVALCFG_DRY
------------

This variable allows to test commands without sending anything to a real device. This is used for testing and debug.

Usage::

    RIVALCFG_DRY=1


RIVALCFG_PROFILE
----------------

This variable can be used to force loading a specific device profile. This is used for testing and debug. You may want to use ``RIVALCFG_DRY`` too when using this variable.

Usage::

    RIVALCFG_PROFILE=<VendorId>:<ProductId>

For example, to load the Rival 100 profile and list its CLI options::

    RIVALCFG_PROFILE=1038:1702 RIVALCFG_DRY=1 rivalcfg --help
