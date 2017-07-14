import pytest

import rivalcfg.debug


class TestGetDebugProfil(object):

    def test_env_variable_not_defined(self, monkeypatch):
        assert rivalcfg.debug.get_debug_profile() is None

    def test_env_variable_defined(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        debugMouseInfo = rivalcfg.debug.get_debug_profile()
        assert debugMouseInfo.vendor_id == 0x1038
        assert debugMouseInfo.product_id == 0x1702

    def test_env_variable_defined_to_wrong_value(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_PROFILE", "foobar")
        with pytest.raises(ValueError):
            rivalcfg.debug.get_debug_profile()


class TestGetDebugDevice(object):

    def test_env_variable_not_defined(self, monkeypatch):
        assert rivalcfg.debug.get_debug_device() is None

    def test_env_variable_defined(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DEVICE", "1038:1702")
        debugMouseInfo = rivalcfg.debug.get_debug_device()
        assert debugMouseInfo.vendor_id == 0x1038
        assert debugMouseInfo.product_id == 0x1702

    def test_env_variable_defined_to_wrong_value(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DEVICE", "foobar")
        with pytest.raises(ValueError):
            rivalcfg.debug.get_debug_device()

    def test_device_env_variable_not_defined_but_profile_env_variable_defined(self, monkeypatch):  # noqa
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        debugMouseInfo = rivalcfg.debug.get_debug_device()
        assert debugMouseInfo.vendor_id == 0x1038
        assert debugMouseInfo.product_id == 0x1702

    def test_device_env_variable_and_profile_env_variable_defined(self, monkeypatch):  # noqa
        monkeypatch.setenv("RIVALCFG_DEVICE", "1038:1710")
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        debugMouseInfo = rivalcfg.debug.get_debug_device()
        assert debugMouseInfo.vendor_id == 0x1038
        assert debugMouseInfo.product_id == 0x1710
