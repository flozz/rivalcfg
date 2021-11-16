import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import aerox3_wireless_wired
from rivalcfg import mouse_settings


class TestDevice(object):
    @pytest.fixture
    def mouse(self):
        settings = mouse_settings.FakeMouseSettings(
            0x1038,
            0xBAAD,
            aerox3_wireless_wired.profile,
        )
        return mouse.Mouse(
            usbhid.FakeDevice(),
            aerox3_wireless_wired.profile,
            settings,
        )

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            (100, b"\x02\x00\x2d\x01\x00\x00"),
            (200, b"\x02\x00\x2d\x01\x00\x01"),
            (300, b"\x02\x00\x2d\x01\x00\x02"),
            (18000, b"\x02\x00\x2d\x01\x00\xD6"),
            ("200,400", b"\x02\x00\x2d\x02\x00\x01\x03"),
            ("200,400,800,1600", b"\x02\x00\x2d\x04\x00\x01\x03\x08\x11"),
        ],
    )
    def test_set_sensitivity(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report
