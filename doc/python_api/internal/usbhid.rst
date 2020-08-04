usbhid
======

.. automodule:: rivalcfg.usbhid


Constants
---------

.. autodata:: HID_REPORT_TYPE_OUTPUT
.. autodata:: HID_REPORT_TYPE_FEATURE


Functions
---------

.. autofunction:: is_device_plugged
.. autofunction:: open_device


Exceptions
----------

.. autoclass:: DeviceNotFound


Fake HID device
---------------

When the ``RIVALCFG_DRY`` environment variable is set, the :func:`open_device`
function of this module returns a fake device instead opening a real one. This
is useful for debuging and testing purpose.

.. autoclass:: FakeDevice
   :members:
