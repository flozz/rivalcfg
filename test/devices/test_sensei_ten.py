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

    @pytest.mark.parametrize("value,expected_hid_report", [
        (200, b"\x02\x00\x55\x00\x01\x01\x04\x00"),
        ("200", b"\x02\x00\x55\x00\x01\x01\x04\x00"),
        ("200,400", b"\x02\x00\x55\x00\x03\x01\x04\x00\x08\x00"),
        ("200,400,800,18000", b"\x02\x00\x55\x00\x0F\x01\x04\x00\x08\x00\x10\x00\x68\x01"),  # noqa
        ])
    def test_set_sensitivity(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x59\x00"
