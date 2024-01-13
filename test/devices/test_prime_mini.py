import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import prime_mini
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            prime_mini.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            prime_mini.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x2D\x01\x00\x02\x00"),
            ("100", b"\x02\x00\x2D\x01\x00\x02\x00"),
            ("500,2500", b"\x02\x00\x2D\x02\x00\x0A\x00\x32\x00"),
            (
                "500,2500,11050,18000",
                b"\x02\x00\x2D\x04\x00\x0A\x00\x32\x00\xDD\x00\x68\x01",
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
            (125, b"\x02\x00\x2b\x04"),
            (250, b"\x02\x00\x2b\x03"),
            (500, b"\x02\x00\x2b\x02"),
            (1000, b"\x02\x00\x2b\x01"),
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
            ("#ABCDEF", b"\x02\x00\x21\x00\xAB\xCD\xEF"),
            ("red", b"\x02\x00\x21\x00\xFF\x00\x00"),
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
            (
                "default",
                b"\x02\x00"
                b"\x2a"
                b"\x01\x00\x00\x00\x00"
                b"\x02\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00"
                b"\x31\x00\x00\x00\x00"
                b"\x32\x00\x00\x00\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x02\x00"
                b"\x2a"
                b"\x01\x00\x00\x00\x00"
                b"\x06\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00"
                b"\x31\x00\x00\x00\x00"
                b"\x32\x00\x00\x00\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x02\x00"
                b"\x2a"
                b"\x01\x00\x00\x00\x00"
                b"\x06\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00"
                b"\x31\x00\x00\x00\x00"
                b"\x32\x00\x00\x00\x00",
            ),
            (
                "buttons(ScrollUp=ScrollDown; ScrollDown=ScrollUp)",
                b"\x02\x00"
                b"\x2a"
                b"\x01\x00\x00\x00\x00"
                b"\x02\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00"
                b"\x32\x00\x00\x00\x00"
                b"\x31\x00\x00\x00\x00",
            ),
        ],
    )
    def test_set_buttons_mapping(self, mouse, value, expected_hid_report):
        mouse.set_buttons_mapping(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("off", b"\x02\x00\x27\x00"),
            ("rainbow", b"\x02\x00\x27\x01"),
        ],
    )
    def test_set_default_lighting(self, mouse, value, expected_hid_report):
        mouse.set_default_lighting(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x11\x00"
