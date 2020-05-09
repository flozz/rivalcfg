import pytest

from rivalcfg import usbhid


class TestIsDevicePlugged(object):

    def test_a_not_plugged_device(self):
        assert not usbhid.is_device_plugged(0x1038, 0xbaad)


class TestOpenDevice(object):

    def test_a_not_plugged_device(self):
        with pytest.raises(usbhid.DeviceNotFound):
            usbhid.open_device(0x1038, 0xbaad, 0x00)

    def test_in_dry_mode(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DRY", "1")
        device = usbhid.open_device(0x1038, 0xbaad, 0x00)
        assert hasattr(device, "write")
        assert hasattr(device, "close")
        assert hasattr(device, "send_feature_report")
