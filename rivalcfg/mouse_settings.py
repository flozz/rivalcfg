import os


def get_xdg_config_home():
    if "XDG_CONFIG_HOME" in os.environ and os.environ["XDG_CONFIG_HOME"]:
        return os.environ["XDG_CONFIG_HOME"]
    return os.path.join(os.path.expanduser("~"), ".config")


def get_settings_path(mouse_id):
    return os.path.join(
        get_xdg_config_home(), "rivalcfg", "%s.device.json" % mouse_id
    )


class MouseSettings(object):
    def __init__(self, vendor_id, product_id, mouse_profile):
        raise NotImplementedError()

    def list_settings_profiles(self):
        raise NotImplementedError()

    def get_settings_profile(self, name="default"):
        raise NotImplementedError()

    def create_settings_profile(self, name, from_profile_name=None):
        # TODO Unique profile name
        raise NotImplementedError()

    def remove_settings_profile(self, name):
        # TODO default profile cannot be removed
        raise NotImplementedError()

    def set(self, setting_name, value):
        raise NotImplementedError()

    def get(self, setting_name):
        raise NotImplementedError()


class FakeMouseSettings(MouseSettings):
    def __init__(self, vendor_id, product_id, mouse_profile):
        self._moues_profile = mouse_profile
        self._mouse_id = "%04x_%04x" % (vendor_id, product_id)
        self._settings_profiles = {}
