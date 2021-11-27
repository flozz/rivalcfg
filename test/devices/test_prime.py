import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import prime
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            prime.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            prime.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x61\x01\x00\x02\x00"),
            ("100", b"\x02\x00\x61\x01\x00\x02\x00"),
            ("500,2500", b"\x02\x00\x61\x02\x00\x0A\x00\x32\x00"),
            (
                "500,2500,11050,18000",
                b"\x02\x00\x61\x04\x00\x0A\x00\x32\x00\xDD\x00\x68\x01",
            ),
        ],
    )
    def test_set_sensitivity(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (125, b"\x02\x00\x5D\x04"),
            (250, b"\x02\x00\x5D\x03"),
            (500, b"\x02\x00\x5D\x02"),
            (1000, b"\x02\x00\x5D\x01"),
        ],
    )
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (
                "#ABCDEF",
                b"\x02\x00\x62\x01\xAB\xCD\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF",
            ),
            (
                "red",
                b"\x02\x00\x62\x01\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF",
            ),
        ],
    )
    def test_set_color(self, mouse, value, expected_hid_report):
        mouse.set_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (0, b"\x02\x00\x5F\x00\x00"),
            (256, b"\x02\x00\x5F\x00\x01"),
            (111, b"\x02\x00\x5F\x6F\x00"),
        ],
    )
    def test_set_led_brightness(self, mouse, value, expected_hid_report):
        mouse.set_led_brightness(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report
