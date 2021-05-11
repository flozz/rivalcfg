import os


def get_xdg_config_home():
    if "XDG_CONFIG_HOME" in os.environ and os.environ["XDG_CONFIG_HOME"]:
        return os.environ["XDG_CONFIG_HOME"]
    return os.path.join(os.path.expanduser("~"), ".config")


def get_settings_path(vendor_id, product_id):
    return os.path.join(
        get_xdg_config_home(), "rivalcfg", "%04x_%04x.device.json" % (
            vendor_id,
            product_id,
        )
    )


class MouseSettings(object):
    def __init__(
        self,
        vendor_id,
        product_id,
        mouse_profile,
        current_profile_name="default",
    ):
        self._mouse_profile = mouse_profile
        self._settings_path = get_settings_path(vendor_id, product_id)
        self._current_profile_name = current_profile_name
        self._settings = {}
        self._load()

    def list_settings_profiles(self):
        raise NotImplementedError()

    def set_active_profile(self, profile_name):
        raise NotImplementedError()

    def create_settings_profile(self, name, from_profile_name=None):
        # TODO Unique profile name
        raise NotImplementedError()

    def remove_settings_profile(self, name):
        # TODO default profile cannot be removed
        raise NotImplementedError()

    def get_default_values(self):
        return {
            k: v["default"] for k, v in self._mouse_profile["settings"].items()
        }

    def set(self, setting_name, value):
        raise NotImplementedError()

    def get(self, setting_name):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def _load(self):
        raise NotImplementedError()


class FakeMouseSettings(MouseSettings):
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
    if "RIVALCFG_DRY" in os.environ:
        return FakeMouseSettings(
            vendor_id,
            product_id,
            mouse_profile,
            current_profile_name
        )
    return MouseSettings(
        vendor_id,
        product_id,
        mouse_profile,
        current_profile_name
    )
