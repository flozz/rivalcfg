import os
import json


def get_xdg_config_home():
    """Returns the path of the folder where to store the configs (generally
    ``$HOME/.config``).

    :rtype: str
    """
    if "XDG_CONFIG_HOME" in os.environ and os.environ["XDG_CONFIG_HOME"]:
        return os.environ["XDG_CONFIG_HOME"]
    return os.path.join(os.path.expanduser("~"), ".config")


def get_settings_path(vendor_id, product_id):
    """Returns the path of a specific mouse settings file.

    :param int vendor_id: The device's vendor id (e.g. ``0x1038``).
    :param int product_id: The device's product id (e.g. ``0xbaad``).

    :rtype: str
    """
    return os.path.join(
        get_xdg_config_home(),
        "rivalcfg",
        "%04x_%04x.device.json"
        % (
            vendor_id,
            product_id,
        ),
    )


class MouseSettings(object):
    """Stores the settings of a mouse.

    :param int vendor_id: The device's vendor id (e.g. ``0x1038``).
    :param int product_id: The device's product id (e.g. ````0xbaad``).
    :param dict mouse_profile: The mouse profie (``devices/*``).
    :param str current_profile_name: The name of the active profile (optional,
                                     default: ``"default"``).
    """

    def __init__(
        self,
        vendor_id,
        product_id,
        mouse_profile,
        current_profile_name="default",
    ):
        self._mouse_profile = mouse_profile
        self._settings_path = get_settings_path(vendor_id, product_id)
        # TODO Check that the profile exists first!
        self._current_profile_name = current_profile_name
        self._settings = {}
        self._load()

    def list_settings_profiles(self):
        """List available profiles.

        .. WARNING::

            Not implemented yet!
        """
        raise NotImplementedError()  # TODO

    def set_active_profile(self, profile_name):
        """Change the active profile.

        .. WARNING::

            Not implemented yet!

        :param str profile_name: The name of the profile.
        """
        # TODO Raise error if the profile does not exist
        raise NotImplementedError()  # TODO

    def create_settings_profile(self, profile_name, from_profile_name=None):
        """Create a new setting profile.

        .. WARNING::

            Not implemented yet!

        :param str profile_name: The name of the new profile.
        :param str from_profile_name: Clone the given profile name (optional,
                                      default: ``None``).
        """
        # TODO Unique profile name (raise error if already exists)
        raise NotImplementedError()  # TODO

    def remove_settings_profile(self, profile_name):
        """Remove a profile.

        .. WARNING::

            Not implemented yet!

        :param str profile_name: The name of the profile to remove.
        """
        # TODO default profile cannot be removed
        # TODO Raise error if profile does not exist
        raise NotImplementedError()  # TODO

    def get_default_values(self):
        """Returns default settings of the device.

        :rtype: dict
        """
        return {
            k: v["default"]
            for k, v in self._mouse_profile["settings"].items()
            if "default" in self._mouse_profile["settings"][k]
        }

    def set(self, setting_name, value):
        """Set a value to a setting.

        :param str setting_name: The setting to set.
        :param value: The value to set.
        """
        if setting_name not in self._mouse_profile["settings"]:
            raise KeyError(
                "The %s device has no '%s' setting"
                % (
                    self._mouse_profile["name"],
                    setting_name,
                )
            )
        if (
            "value_type" in self._mouse_profile["settings"][setting_name]
            and self._mouse_profile["settings"][setting_name]["value_type"] == "none"
        ):
            return  # Skip settings without values
        self._settings[self._current_profile_name][setting_name] = value

    def get(self, setting_name):
        """Get the value of a setting.

        :param str setting_name: The setting to set.
        """
        if setting_name not in self._mouse_profile["settings"]:
            raise KeyError(
                "The %s device has no '%s' setting"
                % (
                    self._mouse_profile["name"],
                    setting_name,
                )
            )
        if (
            "value_type" in self._mouse_profile["settings"][setting_name]
            and self._mouse_profile["settings"][setting_name]["value_type"] == "none"
        ):
            return None
        return self._settings[self._current_profile_name][setting_name]

    def save(self):
        """Save settings in a file.

        .. NOTE::

            Settings are located in
            ``$XDG_CONFIG_HOME/rivalcfg/<vendor_id>_<product_id>.device.json``.
        """
        settings_dir = os.path.dirname(self._settings_path)
        if not os.path.isdir(settings_dir):
            os.makedirs(settings_dir)
        with open(self._settings_path, "w") as file_:
            json.dump(self._settings, file_, indent=2)

    def _load(self):
        """Load settings from a file.

        .. NOTE::

            Settings are located in
            ``$XDG_CONFIG_HOME/rivalcfg/<vendor_id>_<product_id>.device.json``.
        """
        if os.path.isfile(self._settings_path):
            with open(self._settings_path, "r") as file_:
                self._settings = json.load(file_)
        else:
            self._settings = {
                "default": self.get_default_values(),
            }


class FakeMouseSettings(MouseSettings):
    """An implementation of the :class:`MouseSettings` that does not make any I/O.

    :param int vendor_id: The device's vendor id (e.g. ``0x1038``).
    :param int product_id: The device's product id (e.g. ````0xbaad``).
    :param dict mouse_profile: The mouse profie (``devices/*``).
    :param str current_profile_name: The name of the active profile (optional,
                                     default: ``"default"``).
    """

    def save(self):
        pass

    def _load(self):
        self._settings = {
            "default": self.get_default_values(),
        }


def get_mouse_settings(
    vendor_id,
    product_id,
    mouse_profile,
    current_profile_name="default",
):
    """Returns a :class:`MouseSetting` instance.

    .. NOTE::

       A :class:`FakeMouseSettings` instance is returned when ``DEBUG_DRY``
       environment variable is set.

    :param int vendor_id: The device's vendor id (e.g. ``0x1038``).
    :param int product_id: The device's product id (e.g. ````0xbaad``).
    :param dict mouse_profile: The mouse profie (``devices/*``).
    :param str current_profile_name: The name of the active profile (optional,
                                     default: ``"default"``).

    :rtype MouseSettings, FakeMouseSettings
    """
    if "RIVALCFG_DRY" in os.environ:
        return FakeMouseSettings(
            vendor_id,
            product_id,
            mouse_profile,
            current_profile_name,
        )
    return MouseSettings(
        vendor_id,
        product_id,
        mouse_profile,
        current_profile_name,
    )
