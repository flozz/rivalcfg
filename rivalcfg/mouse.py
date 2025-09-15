import os
import time

from . import usbhid
from . import devices
from . import handlers
from . import helpers
from . import mouse_settings


def get_mouse(vendor_id=0x1038, product_id=None):
    """Get a :class:`Mouse` instance to manipulate requested device.

    :param int vendor_id: The vendor id of the device (optional, by default
                          this is set to the SteelSeries vendor id
                          (``0x1038``)).
    :param int product_id: The product id of one of the supported device (e.g.
                           ``0x1702``).
    :raise rivalcfg.devices.UnsupportedDevice: The requested device is not
                                               supported by rivalcfg.
    :rtype: Mouse

    >>> from rivalcfg.mouse import get_mouse
    >>> get_mouse(vendor_id=0x1038, product_id=0x1702)
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """
    if not product_id:
        raise ValueError("You must define the 'product_id' parameter")

    profile = devices.get_profile(vendor_id, product_id)
    settings = mouse_settings.get_mouse_settings(
        vendor_id,
        product_id,
        profile,
    )

    hid_device = usbhid.open_device(vendor_id, product_id, profile["endpoint"])

    return Mouse(hid_device, profile, settings)


class Mouse:
    """Generic class to handle any supported mouse.

    .. NOTE::

       Additional methods are available in this class depending on the loaded
       profile. Read device specific documentation for more information.

    .. WARNING::

       You should not instanciate this class yourself. Use the
       :func:`get_mouse` factory function instead.

    :param hid_device: The HID device to write in (provided by the
                        :func:`rivalcfg.usbhid.open_device`).
    :param mouse_profile: One of the rivalcfg mouse profile (provided by
                            :func:`rivalcfg.devices.get_profile`).
    :param float command_delay: Waiting time beween two commands to not
                                overload the device.

    >>> from rivalcfg import usbhid
    >>> from rivalcfg import devices
    >>> from rivalcfg.mouse import Mouse
    >>> from rivalcfg.mouse_settings import get_mouse_settings
    >>> profile = devices.get_profile(vendor_id=0x1038, product_id=0x1702)
    >>> settings = get_mouse_settings(0x1038, 0x1702, profile)
    >>> Mouse(
    ...     usbhid.open_device(vendor_id=0x1038, product_id=0x1702, endpoint=0),
    ...     profile,
    ...     settings,
    ... )
    <Mouse SteelSeries Rival 100 (1038:1702:00)>
    """

    #: The mouse settings (``rivalcfg.devices.*``)
    mouse_profile = None

    #: The mouse settings (:class:`rivalcfg.mouse_settings.MouseSettings`)
    mouse_settings = None

    _MIN_COMMAND_DELAY = 0.001
    _command_approve_delay = None

    def __init__(self, hid_device, mouse_profile, mouse_settings, command_delay=0.05):
        """Constructor."""
        self._hid_device = hid_device
        self.mouse_profile = mouse_profile
        self.mouse_settings = mouse_settings
        self.command_delay = command_delay

    @property
    def command_delay(self):
        """Waiting time beween two commands to not overload the device.

        .. WARNING::

           Setting this value too low can hang the device. Some mice like the
           Kinzu v2 are known to become laggy or even to crash when commands
           are sent too quickly.
        """
        return self._command_delay

    @command_delay.setter
    def command_delay(self, new_value):
        if new_value < self._MIN_COMMAND_DELAY:
            raise ValueError(
                f"command_delay is unsafe to use, with a delay of less than {self._MIN_COMMAND_DELAY} seconds"
            )

        self._command_approve_delay = new_value

    @property
    def name(self):
        """The mouse name."""
        return self.mouse_profile["name"]

    @property
    def vendor_id(self):
        """The mouse vendor id."""
        return self.mouse_profile["vendor_id"]

    @property
    def product_id(self):
        """The mouse product id."""
        return self.mouse_profile["product_id"]

    def _send_firmware_query(self):
        """Send 0x90 firmware query packet."""
        if "firmware_version" not in self.mouse_profile:
            print("No firmware_version in profile, skipping query")
            return
        self._hid_write(
            report_type=self.mouse_profile["firmware_version"]["report_type"],
            data=self.mouse_profile["firmware_version"]["command"],
            packet_length=64,
        )
        response = self._hid_device.read(
            self.mouse_profile["firmware_version"]["response_length"],
            timeout_ms=200,
        )
        if response:
            version_str = ''.join(chr(b) for b in response[1:16] if 32 <= b <= 126)
            print(f"Firmware query response: {version_str}")
        else:
            print("No firmware response received")
        time.sleep(0.1)

    def _send_reset_packet(self, reset_packet=None):
        """Send reset packet with retries."""
        if reset_packet is None:
            reset_packet = helpers.merge_bytes(0x34, 0x1, 0x0, 0x8, 0x8)
        for _ in range(3):
            self._hid_write(
                report_type=usbhid.HID_REPORT_TYPE_OUTPUT,
                data=reset_packet,
                packet_length=64,
            )
            print(f"Sent reset packet: {list(map(hex, reset_packet))}")
            time.sleep(0.1)

    def _send_initialization_sequence(self, reset_packet=None):
        """Mimic PCAP initialization sequence."""
        self._send_firmware_query()
        if "button_mapping" in self.mouse_profile["settings"]:
            self._hid_write(
                report_type=self.mouse_profile["settings"]["button_mapping"]["report_type"],
                data=self.mouse_profile["settings"]["button_mapping"]["command"],
                packet_length=64,
            )
            print("Sent button_mapping packet: [0x31, 0x00]")
            time.sleep(0.1)
        if reset_packet:
            self._send_reset_packet(reset_packet)
        else:
            self._send_reset_packet()

    @property
    def firmware_version_tuple(self):
        """Firmware version as a tuple (e.g., (1, 1, 5))."""
        if "firmware_version" not in self.mouse_profile:
            return (0,)
        self._hid_write(
            self.mouse_profile["firmware_version"]["report_type"],
            data=self.mouse_profile["firmware_version"]["command"],
            packet_length=64,
        )
        version = self._hid_device.read(
            self.mouse_profile["firmware_version"]["response_length"],
            timeout_ms=200,
        )
        if not version:
            return (0,)
        if self.mouse_profile["firmware_version"]["response_length"] > 2:
            try:
                version_str = ''.join(chr(b) for b in version[1:6] if 32 <= b <= 126)
                version_parts = version_str.split('.')
                return tuple(int(part) for part in version_parts if part.isdigit())
            except Exception:
                return tuple(version[:2])
        return tuple(version)

    @property
    def firmware_version(self):
        """Firmware version as a string (e.g., '1.1.5 +9459436c')."""
        if "firmware_version" not in self.mouse_profile:
            return "0"
        self._hid_write(
            self.mouse_profile["firmware_version"]["report_type"],
            data=self.mouse_profile["firmware_version"]["command"],
            packet_length=64,
        )
        version = self._hid_device.read(
            self.mouse_profile["firmware_version"]["response_length"],
            timeout_ms=200,
        )
        if not version:
            return "0"
        if self.mouse_profile["firmware_version"]["response_length"] > 2:
            try:
                version_str = ''.join(chr(b) for b in version[1:16] if 32 <= b <= 126)
                return version_str.strip()
            except Exception:
                return ".".join(str(i) for i in version[:2])
        return ".".join(str(i) for i in version)

    @property
    def battery(self):
        """Information about the device battery.

        :rtype: dict
        :return: ``{"is_charging": True|False|None, "level": int(0-100)|None}``.

        .. NOTE::

           A value of ``None`` means the feature is not supported or that the mouse is turned off.
        """
        result = {
            "is_charging": None,
            "level": None,
        }
        if "battery_level" not in self.mouse_profile:
            return result

        self._hid_write(
            self.mouse_profile["battery_level"]["report_type"],
            data=self.mouse_profile["battery_level"]["command"],
        )
        data = self._hid_device.read(
            self.mouse_profile["battery_level"]["response_length"],
            timeout_ms=200,
        )

        try:
            if "is_charging" in self.mouse_profile["battery_level"]:
                result["is_charging"] = self.mouse_profile["battery_level"][
                    "is_charging"
                ](data)
        except Exception:
            pass

        try:
            if "level" in self.mouse_profile["battery_level"]:
                result["level"] = self.mouse_profile["battery_level"]["level"](data)
        except Exception:
            pass

        if result["level"] is None or result["level"] > 100 or result["level"] < 0:
            return {"is_charging": None, "level": None}

        return result

    def reset_settings(self):
        """Sets all settings to their factory default values."""
        self._send_initialization_sequence()

        normal_dpi_value = 0x14
        if "sensitivity" in self.mouse_profile["settings"] and "default" in self.mouse_profile["settings"]["sensitivity"]:
            default_cpi = self.mouse_profile["settings"]["sensitivity"]["default"]
            cpi_values = [int(x) for x in default_cpi.split(",")]
            normal_dpi = cpi_values[len(cpi_values) // 2] if cpi_values else 800
            cpi_mappings = {200: 0x04, 400: 0x08, 800: 0x14, 1600: 0x24, 2400: 0x37, 3200: 0x4C}
            normal_dpi_value = cpi_mappings.get(normal_dpi, 0x14)
            print(f"Using normal DPI for pre-reset: {normal_dpi} (0x{normal_dpi_value:02x})")

        if any(key in self.mouse_profile["settings"] for key in ["sensitivity", "sensitivity1", "sensitivity2"]):
            pre_reset_packet = [0x34, 0x4, 0x0, normal_dpi_value, normal_dpi_value, normal_dpi_value, normal_dpi_value, normal_dpi_value, normal_dpi_value, normal_dpi_value, normal_dpi_value]
            print(f"Sending four-pair pre-reset packet for -r: {list(map(hex, pre_reset_packet))}")
            self._hid_write(data=pre_reset_packet)
            time.sleep(0.1)

            clear_packet = [0x34, 0x0, 0x0]
            print(f"Sending clear packet for -r: {list(map(hex, clear_packet))}")
            self._hid_write(data=clear_packet)
            time.sleep(0.1)

            pre_reset_single = [0x34, 0x1, 0x0, normal_dpi_value, normal_dpi_value]
            print(f"Sending fallback pre-reset packet: {list(map(hex, pre_reset_single))}")
            self._hid_write(data=pre_reset_single)
            time.sleep(0.1)

        for key in ["sensitivity", "sensitivity1", "sensitivity2"]:
            if key in self.mouse_profile["settings"] and "default" in self.mouse_profile["settings"][key]:
                print(f"Resetting {key} to default: {self.mouse_profile['settings'][key]['default']}")
                getattr(self, f"set_{key}")(self.mouse_profile["settings"][key]["default"])
                time.sleep(0.1)

        # Process other settings
        for name, setting_info in self.mouse_profile["settings"].items():
            method_name = "set_%s" % name
            method = getattr(self, method_name)
            if (
                "value_type" in setting_info
                and setting_info["value_type"]
                and setting_info["value_type"] != "none"
            ):
                if "default" in setting_info:
                    print(f"Resetting {name} to default: {setting_info['default']}")
                    method(setting_info["default"])
                else:
                    print(f"Skipping reset for {name}: no default value defined")
            else:
                method()
            time.sleep(0.1)

        for key in ["sensitivity", "sensitivity1", "sensitivity2"]:
            if key in self.mouse_profile["settings"] and "default" in self.mouse_profile["settings"][key]:
                print(f"Retrying {key} reset to: {self.mouse_profile['settings'][key]['default']}")
                getattr(self, f"set_{key}")(self.mouse_profile['settings'][key]["default"])
                time.sleep(0.1)

        self.save()

    def save(self):
        """Save current config to the mouse internal memory."""
        # This should never happen... But who knows...
        if (
            "save_command" not in self.mouse_profile
            or not self.mouse_profile["save_command"]
        ):
            raise Exception("This mouse does not provide any save command.")

        packet_length = 0
        if "packet_length" in self.mouse_profile["save_command"]:
            packet_length = self.mouse_profile["save_command"]["packet_length"]

        self._hid_write(
            report_type=self.mouse_profile["save_command"]["report_type"],
            data=self.mouse_profile["save_command"]["command"],
            packet_length=packet_length,
        )

        response = None
        if (
            "readback_length" in self.mouse_profile["save_command"]
            and self.mouse_profile["save_command"]["readback_length"]
        ):
            response = self._hid_device.read(
                self.mouse_profile["save_command"]["readback_length"],
                timeout_ms=200,
            )

        self.mouse_settings.save()

        return response

    def close(self):
        """Close the device.

        .. WARNING::

           Once called, any access of the Mouse class properties or function
           may raise an error.
        """
        self._hid_device.close()

    def _hid_write(
        self,
        report_type=usbhid.HID_REPORT_TYPE_OUTPUT,
        report_id=0x00,
        data=[],
        packet_length=0,
    ):
        """
        Write data to the device.

        :param int report_type: The HID report type
                                (:data:`rivalcfg.usbhid.HID_REPORT_TYPE_OUTPUT`
                                or
                                :data:`rivalcfg.usbhid.HID_REPORT_TYPE_FEATURE`).
        :param int report_id: The id of the report (always ``0x00``).
        :param list(int) data: The data to send to the mouse.
        :param int packet_length: The fixed length of the packet that will be
                                  sent to the device (default: ``0`` (no fixed
                                  length)).

        :raises ValueError: Invalid report type, or HID device not openned.
        """
        if packet_length:
            bytes_ = bytearray(
                helpers.merge_bytes(
                    report_id, data, [0x00] * (packet_length - len(data))
                )
            )
        else:
            bytes_ = bytearray(helpers.merge_bytes(report_id, data))
        if report_type == usbhid.HID_REPORT_TYPE_OUTPUT:
            self._hid_device.write(bytes_)
        elif report_type == usbhid.HID_REPORT_TYPE_FEATURE:
            self._hid_device.send_feature_report(bytes_)
        else:
            raise ValueError("Invalid HID report type: %2x" % report_type)

        # Avoids sending multiple commands to quickly
        if "RIVALCFG_DEBUG_NO_COMMAND_DELAY" not in os.environ:
            time.sleep(self._command_approve_delay)

    def __getattr__(self, name):
        # Handle every set_xxx methods generated from device's profiles

        if not name.startswith("set_"):
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_name = name[4:]

        if setting_name not in self.mouse_profile["settings"]:
            raise AttributeError("Mouse instance has no attribute '%s'" % name)

        setting_info = self.mouse_profile["settings"][setting_name]

        handler_name = None

        if "value_type" in setting_info and setting_info["value_type"]:
            handler_name = setting_info["value_type"]
            if handler_name not in helpers.module_ls(handlers):
                raise ValueError(
                    "Unknown handler '%s' for '%s' setting of the %s"
                    % (
                        handler_name,
                        setting_name,
                        self.mouse_profile["name"],
                    )
                )

        packet_length = 0
        if "packet_length" in setting_info:
            packet_length = setting_info["packet_length"]

        suffix = []
        if "command_suffix" in setting_info:
            suffix = setting_info["command_suffix"]

        def _exec_command(*args):
            if setting_name in ["sensitivity", "sensitivity1", "sensitivity2"]:
                self._send_initialization_sequence()

            data = []
            if handler_name:
                data = getattr(handlers, handler_name).process_value(
                    setting_info, *args
                )
            # Write data to the device
            self._hid_write(
                report_type=setting_info["report_type"],
                data=helpers.merge_bytes(setting_info["command"], data, suffix),
                packet_length=packet_length,
            )
            # Readback when required
            response = None
            if "readback_length" in setting_info and setting_info["readback_length"]:
                response = self._hid_device.read(
                    setting_info["readback_length"],
                    timeout_ms=200,
                )
            # Save settings
            if len(args) == 1:
                self.mouse_settings.set(setting_name, args[0])
            else:
                self.mouse_settings.set(setting_name, args)
            #
            return response

        return _exec_command

    def __repr__(self):
        return "<Mouse %s (%04x:%04x:%02x)>" % (
            self.mouse_profile["name"],
            self.mouse_profile["vendor_id"],
            self.mouse_profile["product_id"],
            self.mouse_profile["endpoint"],
        )

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()
