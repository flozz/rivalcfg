import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import sensei_ten


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), sensei_ten.profile)

    @pytest.mark.parametrize("value,expected_hid_report", [
        (125, b"\x02\x00\x54\x00\x04"),
        (250, b"\x02\x00\x54\x00\x03"),
        (500, b"\x02\x00\x54\x00\x02"),
        (1000, b"\x02\x00\x54\x00\x01"),
        ])
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x59\x00"
