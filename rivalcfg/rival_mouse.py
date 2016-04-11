from helpers import is_color, color_string_to_rgb


class RivalMouse:

    """Generic class to handle any Rival mouse."""

    def __init__(self, mouse_profile):
        """Contructor.

        Arguments:
        mouse_profile -- the mouse profile (rivalcfg.mice.*)
        """
        self._device_path = None
        self._device = None
        self._current_command = []
        pass  # TODO

    def set_default(self):
        """Set all option to their default values."""
        pass  # TODO

    def _find_device(self):
        """Find the HIDRAW device file path."""
        pass  # TODO

    def _device_open(self):
        """Open the device file"""
        self._device = open(self._device_path, "wb")

    def _device_write(self, *bytes_):
        """Write bytes to the device file.

        Arguments:
        *bytes_ -- bytes to write
        """
        if not self._device:
            return;
        self._device.write(bytearray(bytes_))
        self._device.flush()

    def _device_close(self):
        """Close the device file."""
        if self._device:
            self._device.close()
            self._device = None

    def _value_type_choice(self, value):
        """Handle commands with value picked from a dict."""
        pass  # TODO

    def _value_type_rgbcolor(self, *args):
        """Handle commands with RGB color values."""
        pass  # TODO

    def _value_type_none(self):
        """Handle commands with no values."""
        pass  # TODO

    def __getattr__(self, attr):
        pass  # TODO

    def __del__(self):
        self._device_close()

