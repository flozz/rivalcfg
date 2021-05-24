import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival310
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival310.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival310.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x53\x00\x01\x00\x00\x42"),
            (200, b"\x02\x00\x53\x00\x01\x01\x00\x42"),
            (1000, b"\x02\x00\x53\x00\x01\x09\x00\x42"),
            (12000, b"\x02\x00\x53\x00\x01\x77\x00\x42"),
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
            (100, b"\x02\x00\x53\x00\x02\x00\x00\x42"),
            (200, b"\x02\x00\x53\x00\x02\x01\x00\x42"),
            (1000, b"\x02\x00\x53\x00\x02\x09\x00\x42"),
            (12000, b"\x02\x00\x53\x00\x02\x77\x00\x42"),
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
            (125, b"\x02\x00\x54\x00\x04"),
            (250, b"\x02\x00\x54\x00\x03"),
            (500, b"\x02\x00\x54\x00\x02"),
            (1000, b"\x02\x00\x54\x00\x01"),
        ],
    )
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    def test_set_logo_color(self, mouse):
        mouse.set_logo_color(
            "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x5B\x00\x00\xe8\x03\x00\x00\x00"
        #                        |wValue |command|LED|duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04"
        #                            |rpt|           |trg|           |clr count
        expected_hid_report += b"\xFF\x00\x00\xFF\x00\x00\x00\x00\xFF\x00"
        #                        |init color |color1     |ps1|color2     |
        expected_hid_report += b"\x54\x00\x00\xFF\x54\xFF\x00\x00\x57"
        #                        |ps2|color3     |ps3|color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_wheel_color(self, mouse):
        mouse.set_wheel_color(
            "rgbgradient(duration=5000; colors=0%: #112233, 25%: #445566, 50%: #778899, 75%: #AABBCC)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x5B\x00\x01\x88\x13\x00\x00\x00"
        #                        |wValue |command|LED|duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05"
        #                            |rpt|           |trg|           |clr count
        expected_hid_report += b"\x11\x22\x33"
        #                        |init color |
        expected_hid_report += b"\x11\x22\x33\x00"
        #                        |color1     |pos1|
        expected_hid_report += b"\x44\x55\x66\x3F"
        #                        |color2     |pos2|
        expected_hid_report += b"\x77\x88\x99\x40"
        #                        |color3     |pos3|
        expected_hid_report += b"\xAA\xBB\xCC\x40"
        #                        |color4     |pos4|
        expected_hid_report += b"\x11\x22\x33\x40"
        # (=color1: smoothing)   |color5     |pos5|

        assert hid_report == expected_hid_report

    def test_set_wheel_color_with_color_string(self, mouse):
        mouse.set_wheel_color("#FF1800")

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x5B\x00\x01\xe8\x03\x00\x00\x00"
        #                        |wValue |command|LED|duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #
        expected_hid_report += b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01"
        #                            |rpt|           |trg|           |clr count
        expected_hid_report += b"\xff\x18\x00\xff\x18\x00\x00"
        #                        |init color |color1     |ps1|

        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (
                "default",
                b"\x02\x00\x31\x00\x01\x00\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x30\x00\x00\x00\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x02\x00\x31\x00\x01\x00\x00\x00\x00\x06\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x30\x00\x00\x00\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x02\x00\x31\x00\x01\x00\x00\x00\x00\x06\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x30\x00\x00\x00\x00",
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
        assert hid_report == b"\x02\x00\x59\x00"

    def test_firmware_version(self, mouse):
        mouse.firmware_version_tuple
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == b"\x02\x00\x90\x00"
