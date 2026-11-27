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

    def test_search_by_usage_page(self, monkeypatch):
        monkeypatch.delenv("RIVALCFG_DRY")  # Be sure that dry mode is disabled
        opened = []

        class FakeHidDevice:
            def open_path(self, path):
                opened.append(path)

        interfaces = [
            {"interface_number": -1, "usage_page": 0x0001, "path": b"mouse"},
            {"interface_number": -1, "usage_page": 0xFFC0, "path": b"vendor"},
        ]
        monkeypatch.setattr(usbhid.hid, "enumerate", lambda *args: interfaces)
        monkeypatch.setattr(usbhid.hid, "device", FakeHidDevice)

        usbhid.open_device(0x0111, 0x1854, 0, usage_page=0xFFC0)
        assert opened == [b"vendor"]

        with pytest.raises(usbhid.DeviceNotFound):
            usbhid.open_device(0x0111, 0x1854, 0, usage_page=0xFFC1)
