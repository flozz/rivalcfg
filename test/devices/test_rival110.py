import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival110


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), rival110.profile)

    # TODO Sensitivity 1
    # TODO Sensitivity 2

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
        assert len(hid_report) == 1 + 1 + 32   # report_type + report_id + data
        assert hid_report.startswith(expected_hid_report)

    @pytest.mark.parametrize("value,expected_hid_report", [
        ("#ABCDEF", b"\x02\x00\x05\x00\xAB\xCD\xEF"),
        ("red", b"\x02\x00\x05\x00\xFF\x00\x00"),
        ])
    def test_set_color(self, mouse, value, expected_hid_report):
        mouse.set_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert len(hid_report) == 1 + 1 + 32   # report_type + report_id + data
        assert hid_report.startswith(expected_hid_report)

    @pytest.mark.parametrize("value,expected_hid_report", [
        ("steady", b"\x02\x00\x07\x00\x01"),
        ("breath", b"\x02\x00\x07\x00\x03"),
        (1, b"\x02\x00\x07\x00\x01"),
        (2, b"\x02\x00\x07\x00\x02"),
        (3, b"\x02\x00\x07\x00\x03"),
        (4, b"\x02\x00\x07\x00\x04"),
        ])
    def test_set_light_effect(self, mouse, value, expected_hid_report):
        mouse.set_light_effect(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert len(hid_report) == 1 + 1 + 32   # report_type + report_id + data
        assert hid_report.startswith(expected_hid_report)

    @pytest.mark.parametrize("value,expected_hid_report", [
        ("dpi", b"\x02\x00\x0B\x00"),
        ("os", b"\x02\x00\x0B\x01"),
        ])
    def test_set_btn6_mode(self, mouse, value, expected_hid_report):
        mouse.set_btn6_mode(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert len(hid_report) == 1 + 1 + 32   # report_type + report_id + data
        assert hid_report.startswith(expected_hid_report)

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert len(hid_report) == 1 + 1 + 32   # report_type + report_id + data
        assert hid_report.startswith(b"\x02\x00\x09\x00")
