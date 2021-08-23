import json

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
        "setting3": {
            "value_type": "none",
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
            mouse_settings.get_settings_path(0x1038, 0xBAAD)
            == "/tmp/foo/bar/rivalcfg/1038_baad.device.json"
        )


class Test_FakeMouseSettings(object):
    @pytest.fixture
    def mouse_settings(self):
        return mouse_settings.FakeMouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)

    def test_get_default_values(self, mouse_settings):
        assert mouse_settings.get_default_values() == {
            "setting1": "foo",
            "setting2": "bar",
        }

    def test_get_set_with_existing_setting(self, mouse_settings):
        assert mouse_settings.get("setting1") == "foo"
        mouse_settings.set("setting1", "test")
        assert mouse_settings.get("setting1") == "test"

    def test_get_with_non_existing_setting(self, mouse_settings):
        with pytest.raises(KeyError):
            mouse_settings.get("foobar")

    def test_set_with_non_existing_setting(self, mouse_settings):
        with pytest.raises(KeyError):
            mouse_settings.set("foobar", "test")


class Test_MouseSettings(object):
    def test_save_load_defaults(self, monkeypatch, tmpdir):
        monkeypatch.delenv("DEBUG_DRY", raising=False)
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))
        ms = mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)
        ms.save()
        mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)

    def test_save_load(self, monkeypatch, tmpdir):
        monkeypatch.delenv("DEBUG_DRY", raising=False)
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))
        ms = mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)
        ms.set("setting1", "test1")
        ms.save()
        ms2 = mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)
        assert ms2.get("setting1") == "test1"

    def test_none_value_type_settings_return_none(self, monkeypatch, tmpdir):
        monkeypatch.delenv("DEBUG_DRY", raising=False)
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))
        ms = mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)
        ms.set("setting3", "foo")
        assert ms.get("setting3") is None

    def test_none_value_type_settings_not_saved(self, monkeypatch, tmpdir):
        monkeypatch.delenv("DEBUG_DRY", raising=False)
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))
        ms = mouse_settings.MouseSettings(0x1038, 0xBAAD, FAKE_PROFILE)
        ms.set("setting3", "foo")
        ms.save()
        with open(mouse_settings.get_settings_path(0x1038, 0xBAAD), "r") as file_:
            saved_data = json.load(file_)
        assert "setting3" not in saved_data["default"]
