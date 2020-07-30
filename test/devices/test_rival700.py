import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival700


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), rival700.profile)

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x03\x00\x01\x00\x00\x42"),
        (200, b"\x02\x00\x03\x00\x01\x01\x00\x42"),
        (1000, b"\x02\x00\x03\x00\x01\x09\x00\x42"),
        (12000, b"\x02\x00\x03\x00\x01\x77\x00\x42"),
        ])
    def test_set_sensitivity1(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity1(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x03\x00\x02\x00\x00\x42"),
        (200, b"\x02\x00\x03\x00\x02\x01\x00\x42"),
        (1000, b"\x02\x00\x03\x00\x02\x09\x00\x42"),
        (12000, b"\x02\x00\x03\x00\x02\x77\x00\x42"),
        ])
    def test_set_sensitivity2(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity2(value)
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

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x09\x00"
