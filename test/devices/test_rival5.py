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
