import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival650
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival650.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival650.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x15\x01\x00"),
            (200, b"\x02\x00\x15\x01\x01"),
            (1000, b"\x02\x00\x15\x01\x09"),
            (12000, b"\x02\x00\x15\x01\x77"),
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
            (100, b"\x02\x00\x15\x02\x00"),
            (200, b"\x02\x00\x15\x02\x01"),
            (1000, b"\x02\x00\x15\x02\x09"),
            (12000, b"\x02\x00\x15\x02\x77"),
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
            (125, b"\x02\x00\x17\x04"),
            (250, b"\x02\x00\x17\x03"),
            (500, b"\x02\x00\x17\x02"),
            (1000, b"\x02\x00\x17\x01"),
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
                "default",
                b"\x02\x00\x19\x01\x00\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x02\x00\x19\x01\x00\x00\x00\x00\x06\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x02\x00\x19\x01\x00\x00\x00\x00\x06\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00",
            ),
            (
                "buttons(Button1=ScrollDown; Button2=ScrollUp)",
                b"\x02\x00\x19\x32\x00\x00\x00\x00\x31\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00",
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
            (1, b"\x02\x00\x2b\x01\x01\x00\x00\x00\x3c\x00"),
            (2, b"\x02\x00\x2b\x01\x01\x00\x00\x00\x78\x00"),
            (5, b"\x02\x00\x2b\x01\x01\x00\x00\x00\x2c\x01"),
            (20, b"\x02\x00\x2b\x01\x01\x00\x00\x00\xb0\x04"),
        ],
    )
    def test_set_sleep_timer(self, mouse, value, expected_hid_report):
        mouse.set_sleep_timer(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_battery_level(self, mouse):
        battery_info = mouse.battery
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\xAA\x01"
        assert "is_charging" in battery_info
        assert "level" in battery_info

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x09"
