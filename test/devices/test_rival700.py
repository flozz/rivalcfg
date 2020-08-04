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

    def test_set_logo_color(self, mouse):
        mouse.set_logo_color("rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)")  # noqa

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00"
        expected_hid_report += b"\x00\x1D\x01\x02\x31\x51\xFF\xC8\x00\x00"
        expected_hid_report += b"\x00\xF4\x0C\x00\x00\x4A\x01\x01\x00\x00"
        expected_hid_report += b"\xF4\x0C\x00\x4A\x01\x02\x00\x0C\x00\xF4"
        expected_hid_report += b"\x00\x54\x01\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF0"
        expected_hid_report += b"\x0F\x00\x00\x00\x00\xFF\x00\xDC\x05\x8A"
        expected_hid_report += b"\x02\x00\x00\x00\x00\x01\x00\x03\x00\xE8"
        expected_hid_report += b"\x03"

        assert hid_report == expected_hid_report

    def test_set_wheel_color(self, mouse):
        mouse.set_wheel_color("rgbgradient(duration=5000; colors=0%: #112233, 25%: #445566, 50%: #778899, 75%: #AABBCC)")  # noqa

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00"
        expected_hid_report += b"\x01\x1D\x01\x02\x31\x51\xFF\xC8\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\xE2\x04\x01\x00\x00"
        expected_hid_report += b"\x00\x00\x00\xE2\x04\x02\x00\x00\x00\x00"
        expected_hid_report += b"\x00\xE2\x04\x03\x00\xFF\xFF\xFF\x00\xE2"
        expected_hid_report += b"\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10"
        expected_hid_report += b"\x01\x20\x02\x30\x03\xFF\x00\xDC\x05\x8A"
        expected_hid_report += b"\x02\x00\x00\x00\x00\x01\x00\x04\x00\x88"
        expected_hid_report += b"\x13"

        assert hid_report == expected_hid_report

    def test_set_wheel_color_with_color_string(self, mouse):
        mouse.set_wheel_color("#FF1800")

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00"
        expected_hid_report += b"\x01\x1D\x01\x02\x31\x51\xFF\xC8\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF0"
        expected_hid_report += b"\x0F\x80\x01\x00\x00\xFF\x00\xDC\x05\x8A"
        expected_hid_report += b"\x02\x00\x00\x00\x00\x01\x00\x00\x00\xE8"
        expected_hid_report += b"\x03"

        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x09\x00"
