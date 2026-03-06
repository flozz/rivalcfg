import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival5
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival5.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival5.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x2d\x01\x00\x00"),
            (200, b"\x02\x00\x2d\x01\x00\x02"),
            (300, b"\x02\x00\x2d\x01\x00\x03"),
            (18000, b"\x02\x00\x2d\x01\x00\xd6"),
            ("200,400", b"\x02\x00\x2d\x02\x00\x02\x04"),
            ("200,400,800,1600", b"\x02\x00\x2d\x04\x00\x02\x04\x09\x12"),
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

    def test_set_wheel_color(self, mouse):
        mouse.set_wheel_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            01 00
            AB CD EF
        """)

    def test_set_z2_color(self, mouse):
        mouse.set_z2_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            02 00
            00 00 00
            AB CD EF
        """)

    def test_set_z3_color(self, mouse):
        mouse.set_z3_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            04 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z4_color(self, mouse):
        mouse.set_z4_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            08 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z5_color(self, mouse):
        mouse.set_z5_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            10 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z6_color(self, mouse):
        mouse.set_z6_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            20 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z7_color(self, mouse):
        mouse.set_z7_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            40 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z8_color(self, mouse):
        mouse.set_z8_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            80 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_z9_color(self, mouse):
        mouse.set_z9_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            00 01
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    def test_set_logo_color(self, mouse):
        mouse.set_logo_color("ABCDEF")
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            21
            00 02
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            00 00 00
            AB CD EF
        """)

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("#ABCDEF", bytes.fromhex("02 00 26 01 00 AB CD EF")),
            ("off", bytes.fromhex("02 00 26 00 00 00 00 00")),
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
            ("100", bytes.fromhex("02 00 23 64")),
            ("75", bytes.fromhex("02 00 23 32")),
            ("50", bytes.fromhex("02 00 23 19")),
            ("25", bytes.fromhex("02 00 23 0C")),
            ("0", bytes.fromhex("02 00 23 00")),
        ],
    )
    def test_set_led_brightness(self, mouse, value, expected_hid_report):
        mouse.set_led_brightness(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_set_buttons_mapping(self, mouse):
        mouse.set_buttons_mapping(
            "buttons(button1=button2; button2=a; button3=ScrollUp)"
        )
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("""
            02 00
            2A
            02 00 00 00 00
            51 04 00 00 00
            31 00 00 00 00
            04 00 00 00 00
            05 00 00 00 00
            00 00 00 00 00
            00 00 00 00 00
            00 00 00 00 00
            30 00 00 00 00
            31 00 00 00 00
            32 00 00 00 00
            """)

    def test_set_rainbow_effect(self, mouse):
        mouse.set_rainbow_effect()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == bytes.fromhex("02 00 22 FF 03")

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("off", bytes.fromhex("02 00 27 00")),
            ("rainbow", bytes.fromhex("02 00 27 01")),
        ],
    )
    def test_set_default_lighting(self, mouse, value, expected_hid_report):
        mouse.set_default_lighting(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report
