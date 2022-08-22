import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival100
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival100.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival100.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (250, b"\x02\x00\x03\x01\x08"),
            (500, b"\x02\x00\x03\x01\x07"),
            (1000, b"\x02\x00\x03\x01\x06"),
            (1250, b"\x02\x00\x03\x01\x05"),
            (1500, b"\x02\x00\x03\x01\x04"),
            (1750, b"\x02\x00\x03\x01\x03"),
            (2000, b"\x02\x00\x03\x01\x02"),
            (4000, b"\x02\x00\x03\x01\x01"),
        ],
    )
    def test_set_sensitivity1(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity1(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (250, b"\x02\x00\x03\x02\x08"),
            (500, b"\x02\x00\x03\x02\x07"),
            (1000, b"\x02\x00\x03\x02\x06"),
            (1250, b"\x02\x00\x03\x02\x05"),
            (1500, b"\x02\x00\x03\x02\x04"),
            (1750, b"\x02\x00\x03\x02\x03"),
            (2000, b"\x02\x00\x03\x02\x02"),
            (4000, b"\x02\x00\x03\x02\x01"),
        ],
    )
    def test_set_sensitivity2(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity2(value)
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
            ("#ABCDEF", b"\x02\x00\x05\x00\xAB\xCD\xEF"),
            ("red", b"\x02\x00\x05\x00\xFF\x00\x00"),
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
            ("steady", b"\x02\x00\x07\x00\x01"),
            ("breath", b"\x02\x00\x07\x00\x03"),
            (1, b"\x02\x00\x07\x00\x01"),
            (2, b"\x02\x00\x07\x00\x02"),
            (3, b"\x02\x00\x07\x00\x03"),
            (4, b"\x02\x00\x07\x00\x04"),
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
            ("dpi", b"\x02\x00\x0B\x00"),
            ("os", b"\x02\x00\x0B\x01"),
        ],
    )
    def test_set_btn6_mode(self, mouse, value, expected_hid_report):
        mouse.set_btn6_mode(value)
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
