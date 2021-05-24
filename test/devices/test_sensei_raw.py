import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import sensei_raw
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            sensei_raw.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            sensei_raw.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (90, b"\x02\x00\x03\x01\x01"),
            (180, b"\x02\x00\x03\x01\x02"),
            (1530, b"\x02\x00\x03\x01\x11"),
            (2520, b"\x02\x00\x03\x01\x1C"),
            (5400, b"\x02\x00\x03\x01\x3C"),
            (5670, b"\x02\x00\x03\x01\x3F"),
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
            (90, b"\x02\x00\x03\x02\x01"),
            (180, b"\x02\x00\x03\x02\x02"),
            (1530, b"\x02\x00\x03\x02\x11"),
            (2520, b"\x02\x00\x03\x02\x1C"),
            (5400, b"\x02\x00\x03\x02\x3C"),
            (5670, b"\x02\x00\x03\x02\x3F"),
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
            ("off", b"\x02\x00\x05\x01\x01"),
            ("low", b"\x02\x00\x05\x01\x02"),
            ("medium", b"\x02\x00\x05\x01\x03"),
            ("high", b"\x02\x00\x05\x01\x04"),
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
            ("steady", b"\x02\x00\x07\x01\x01"),
            ("breath", b"\x02\x00\x07\x01\x03"),
            (1, b"\x02\x00\x07\x01\x01"),
            (2, b"\x02\x00\x07\x01\x02"),
            (3, b"\x02\x00\x07\x01\x03"),
            (4, b"\x02\x00\x07\x01\x04"),
            ("trigger", b"\x02\x00\x07\x01\x05"),
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
                b"\x02\x00\x31\x00\x01\x00\x00\x02\x00\x00\x03\x00\x00\x04\x00\x00\x05\x00\x00\x10\x4b\x00\x10\x4e\x00\x30\x00\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x02\x00\x31\x00\x01\x00\x00\x06\x00\x00\x03\x00\x00\x04\x00\x00\x05\x00\x00\x10\x4b\x00\x10\x4e\x00\x30\x00\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x02\x00\x31\x00\x01\x00\x00\x06\x00\x00\x03\x00\x00\x04\x00\x00\x05\x00\x00\x10\x4b\x00\x10\x4e\x00\x30\x00\x00",
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
