import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival600
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            rival600.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            rival600.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x03\x00\x01\x00\x00\x42"),
            (200, b"\x02\x00\x03\x00\x01\x01\x00\x42"),
            (1000, b"\x02\x00\x03\x00\x01\x09\x00\x42"),
            (12000, b"\x02\x00\x03\x00\x01\x77\x00\x42"),
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
            (100, b"\x02\x00\x03\x00\x02\x00\x00\x42"),
            (200, b"\x02\x00\x03\x00\x02\x01\x00\x42"),
            (1000, b"\x02\x00\x03\x00\x02\x09\x00\x42"),
            (12000, b"\x02\x00\x03\x00\x02\x77\x00\x42"),
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

    def test_set_wheel_color(self, mouse):
        mouse.set_wheel_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x00\x00\x00\x00\x00\x00"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_logo_color(self, mouse):
        mouse.set_logo_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x01\x00\x00\x00\x00\x01"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z2_color(self, mouse):
        mouse.set_z2_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x02\x00\x00\x00\x00\x02"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z3_color(self, mouse):
        mouse.set_z3_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x03\x00\x00\x00\x00\x03"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z4_color(self, mouse):
        mouse.set_z4_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x04\x00\x00\x00\x00\x04"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z5_color(self, mouse):
        mouse.set_z5_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x05\x00\x00\x00\x00\x05"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z6_color(self, mouse):
        mouse.set_z6_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x06\x00\x00\x00\x00\x06"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    def test_set_z7_color(self, mouse):
        mouse.set_z7_color(
            "rgbgradient(duration=5000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)"
        )

        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()

        expected_hid_report = b""
        expected_hid_report += b"\x03\x00\x05\x00\x07\x00\x00\x00\x00\x07"
        #                       |wValue  |command|led|               |led|
        expected_hid_report += b"\x88\x13\x00\x00\x00\x00\x00\x00\x00\x00"
        #                       |duratio|
        expected_hid_report += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        #                                                |rpt|trg|
        expected_hid_report += b"\x00\x04\xFF\x00\x00"
        #                                |init color |
        expected_hid_report += b"\xFF\x00\x00\x00"
        #                        |color1     |ps1|
        expected_hid_report += b"\x00\xFF\x00\x54"
        #                        |color2     |ps2|
        expected_hid_report += b"\x00\x00\xFF\x54"
        #                        |color3     |ps3|
        expected_hid_report += b"\xFF\x00\x00\x57"
        #                        |color4     |ps4|
        # color4 = color1 (added for smoothing)

        assert hid_report == expected_hid_report

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (
                "default",
                b"\x03\x00"
                b"\x31\x00"
                b"\x01\x00\x00\x00\x00"
                b"\x02\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00",
            ),
            (
                "buttons(button2=button6)",
                b"\x03\x00"
                b"\x31\x00"
                b"\x01\x00\x00\x00\x00"
                b"\x06\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00",
            ),
            (
                {"buttons": {"button2": "button6"}},
                b"\x03\x00"
                b"\x31\x00"
                b"\x01\x00\x00\x00\x00"
                b"\x06\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00",
            ),
            (
                "buttons(Button1=ScrollDown; Button2=ScrollUp)",
                b"\x03\x00"
                b"\x31\x00"
                b"\x32\x00\x00\x00\x00"
                b"\x31\x00\x00\x00\x00"
                b"\x03\x00\x00\x00\x00"
                b"\x04\x00\x00\x00\x00"
                b"\x05\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00"
                b"\x30\x00\x00\x00\x00",
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
