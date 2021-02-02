import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival650


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), rival650.profile)

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x15\x01\x00"),
        (200, b"\x02\x00\x15\x01\x01"),
        (1000, b"\x02\x00\x15\x01\x09"),
        (12000, b"\x02\x00\x15\x01\x77"),
        ])
    def test_set_sensitivity1(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity1(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x15\x02\x00"),
        (200, b"\x02\x00\x15\x02\x01"),
        (1000, b"\x02\x00\x15\x02\x09"),
        (12000, b"\x02\x00\x15\x02\x77"),
        ])
    def test_set_sensitivity2(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity2(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (125, b"\x02\x00\x17\x04"),
        (250, b"\x02\x00\x17\x03"),
        (500, b"\x02\x00\x17\x02"),
        (1000, b"\x02\x00\x17\x01"),
        ])
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report
