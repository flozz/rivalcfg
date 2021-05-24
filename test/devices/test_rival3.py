import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival3
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival3.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival3.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (200, b"\x02\x00\x0b\x00\x01\x01\x04"),
            ("200", b"\x02\x00\x0b\x00\x01\x01\x04"),
            ("200,400", b"\x02\x00\x0b\x00\x02\x01\x04\x08"),
            ("200,400,800,1600", b"\x02\x00\x0b\x00\x04\x01\x04\x08\x11\x24"),
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
            (125, b"\x02\x00\x04\x00\x04"),
            (250, b"\x02\x00\x04\x00\x03"),
            (500, b"\x02\x00\x04\x00\x02"),
            (1000, b"\x02\x00\x04\x00\x01"),
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
            ("#ABCDEF", b"\x02\x00\x05\x00\x01\xAB\xCD\xEF\x64"),
            ("red", b"\x02\x00\x05\x00\x01\xFF\x00\x00\x64"),
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
            ("#ABCDEF", b"\x02\x00\x05\x00\x02\xAB\xCD\xEF\x64"),
            ("red", b"\x02\x00\x05\x00\x02\xFF\x00\x00\x64"),
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
            ("#ABCDEF", b"\x02\x00\x05\x00\x03\xAB\xCD\xEF\x64"),
            ("red", b"\x02\x00\x05\x00\x03\xFF\x00\x00\x64"),
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
            ("#ABCDEF", b"\x02\x00\x05\x00\x04\xAB\xCD\xEF\x64"),
            ("red", b"\x02\x00\x05\x00\x04\xFF\x00\x00\x64"),
        ],
    )
    def test_set_logo_color(self, mouse, value, expected_hid_report):
        mouse.set_logo_color(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("rainbow-shift", b"\x02\x00\x06\x00\x00"),
            ("breath-fast", b"\x02\x00\x06\x00\x01"),
            ("breath", b"\x02\x00\x06\x00\x02"),
            ("breath-slow", b"\x02\x00\x06\x00\x03"),
            ("steady", b"\x02\x00\x06\x00\x04"),
            ("rainbow-breath", b"\x02\x00\x06\x00\x05"),
            ("disco", b"\x02\x00\x06\x00\x06"),
        ],
    )
    def test_set_light_effect(self, mouse, value, expected_hid_report):
        mouse.set_light_effect(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (
                "default",
                b"\x02\x00\x07\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x30\x00\x31\x00\x32\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x02\x00\x07\x00\x01\x00\x06\x00\x03\x00\x04\x00\x05\x00\x30\x00\x31\x00\x32\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x02\x00\x07\x00\x01\x00\x06\x00\x03\x00\x04\x00\x05\x00\x30\x00\x31\x00\x32\x00",
            ),
            (
                "buttons(ScrollUp=ScrollDown; ScrollDown=ScrollUp)",
                b"\x02\x00\x07\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x30\x00\x32\x00\x31\x00",
            ),
        ],
    )
    def test_set_buttons_mapping(self, mouse, value, expected_hid_report):
        mouse.set_buttons_mapping(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x09\x00"

    def test_firmware_version(self, mouse):
        mouse.firmware_version_tuple
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x10\x00"
