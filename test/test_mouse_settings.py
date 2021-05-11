from rivalcfg import mouse_settings


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
            mouse_settings.get_settings_path("1038_1729")
            == "/tmp/foo/bar/rivalcfg/1038_1729.device.json"
        )
