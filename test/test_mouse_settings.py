import pytest

from rivalcfg import mouse_settings

FAKE_PROFILE = {
    "settings": {
        "setting1": {
            "default": "foo",
        },
        "setting2": {
            "default": "bar",
        },
    },
}


class Test_get_xdg_config_home(object):
    def test_environ_not_set(self, monkeypatch):
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        monkeypatch.setenv("HOME", "/tmp")
        assert mouse_settings.get_xdg_config_home() == "/tmp/.config"

    def test_environ_set(self, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", "/tmp/foo/bar")
        assert mouse_settings.get_xdg_config_home() == "/tmp/foo/bar"


class Test_get_settings_path(object):
    def test_settings_file_path(self, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", "/tmp/foo/bar")
        assert (
            mouse_settings.get_settings_path(0x1038, 0xbaad)
            == "/tmp/foo/bar/rivalcfg/1038_baad.device.json"
        )


class Test_MouseSettings(object):

    @pytest.fixture
    def mouse_settings(self):
        return mouse_settings.get_mouse_settings(0x1038, 0xbaad, FAKE_PROFILE)

    def test_get_default_values(self, mouse_settings):
        assert mouse_settings.get_default_values() == {
            "setting1": "foo",
            "setting2": "bar",
        }
