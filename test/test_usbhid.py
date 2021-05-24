import pytest

from rivalcfg import usbhid


class TestIsDevicePlugged(object):
    def test_a_not_plugged_device(self):
        assert not usbhid.is_device_plugged(0x1038, 0xBAAD)

    def test_a_plugged_debug_device(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        assert usbhid.is_device_plugged(0x1038, 0x1702)


class TestOpenDevice(object):
    def test_a_not_plugged_device(self, monkeypatch):
        monkeypatch.delenv("RIVALCFG_DRY")  # Be sure that dry mode is disabled
        with pytest.raises(usbhid.DeviceNotFound):
            usbhid.open_device(0x1038, 0xBAAD, 0x00)

    def test_in_dry_mode(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DRY", "1")
        device = usbhid.open_device(0x1038, 0xBAAD, 0x00)
        assert hasattr(device, "write")
        assert hasattr(device, "close")
        assert hasattr(device, "send_feature_report")
