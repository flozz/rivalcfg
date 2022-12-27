import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import aerox3
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            aerox3.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            aerox3.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (200, b"\x02\x00\x2d\x01\x01\x04"),
            ("200", b"\x02\x00\x2d\x01\x01\x04"),
            ("200,400", b"\x02\x00\x2d\x02\x01\x04\x08"),
            ("200,400,800,1600", b"\x02\x00\x2d\x04\x01\x04\x08\x11\x24"),
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
            ("#ABCDEF", b"\x02\x00\x21\x01\xAB\xCD\xEF"),
            ("red", b"\x02\x00\x21\x01\xFF\x00\x00"),
        ],
    )
    def test_set_z1_color(self, mouse, value, expected_hid_report):
        mouse.set_z1_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("#ABCDEF", b"\x02\x00\x21\x02\x00\x00\x00\xAB\xCD\xEF"),
            ("red", b"\x02\x00\x21\x02\x00\x00\x00\xFF\x00\x00"),
        ],
    )
    def test_set_z2_color(self, mouse, value, expected_hid_report):
        mouse.set_z2_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("#ABCDEF", b"\x02\x00\x21\x04\x00\x00\x00\x00\x00\x00\xAB\xCD\xEF"),
            ("red", b"\x02\x00\x21\x04\x00\x00\x00\x00\x00\x00\xFF\x00\x00"),
        ],
    )
    def test_set_z3_color(self, mouse, value, expected_hid_report):
        mouse.set_z3_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("red", b"\x02\x00\x26\x01\x00\xff\x00\x00"),
            ("#ff1802", b"\x02\x00\x26\x01\x00\xff\x18\x02"),
            ("disable", b"\x02\x00\x26\x00\x00\x00\x00\x00"),
            ("off", b"\x02\x00\x26\x00\x00\x00\x00\x00"),
        ],
    )
    def test_set_reactive_color(self, mouse, value, expected_hid_report):
        mouse.set_reactive_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (0, b"\x02\x00\x23\x00"),
            (100, b"\x02\x00\x23\x64"),
        ],
    )
    def test_set_led_brightness(self, mouse, value, expected_hid_report):
        mouse.set_led_brightness(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("all", b"\x02\x00\x22\x07"),
            ("bottom", b"\x02\x00\x22\x04"),
            ("middle", b"\x02\x00\x22\x02"),
            ("top", b"\x02\x00\x22\x01"),
            ("bottom-middle", b"\x02\x00\x22\x06"),
            ("middle-top", b"\x02\x00\x22\x03"),
            ("bottom-top", b"\x02\x00\x22\x05"),
        ],
    )
    def test_set_rainbow_effect(self, mouse, value, expected_hid_report):
        mouse.set_rainbow_effect(value)
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
            ("off", b"\x02\x00\x27\x00\x00"),
            ("reactive", b"\x02\x00\x27\x00\x01"),
            ("rainbow", b"\x02\x00\x27\x01\x00"),
            ("reactive-rainbow", b"\x02\x00\x27\x01\x01"),
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
