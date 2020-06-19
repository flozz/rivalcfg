import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival3


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), rival3.profile)

    @pytest.mark.parametrize("value,expected_hid_report", [
        (200, b"\x02\x00\x0b\x00\x01\x01\x04"),
        ("200", b"\x02\x00\x0b\x00\x01\x01\x04"),
        ("200,400", b"\x02\x00\x0b\x00\x02\x01\x04\x08"),
        ("200,400,800,1600", b"\x02\x00\x0b\x00\x04\x01\x04\x08\x11\x24"),
        ])
    def test_set_sensitivity(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (125, b"\x02\x00\x04\x00\x04"),
        (250, b"\x02\x00\x04\x00\x03"),
        (500, b"\x02\x00\x04\x00\x02"),
        (1000, b"\x02\x00\x04\x00\x01"),
        ])
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        ("#FF1800", b"\x02\x00\x0A\x00\x0F\xFF\x18\x00\xFF\x18\x00\xFF\x18\x00\xFF\x18\x00"),  # noqa
        ("123,456,789,red", b"\x02\x00\x0A\x00\x0F\x11\x22\x33\x44\x55\x66\x77\x88\x99\xFF\x00\x00"),  # noqa
        ])
    def test_set_colors(self, mouse, value, expected_hid_report):
        mouse.set_colors(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x09\x00"
