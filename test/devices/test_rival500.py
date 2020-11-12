import pytest

from rivalcfg import usbhid
from rivalcfg import mouse
from rivalcfg.devices import rival500


class TestDevice(object):

    @pytest.fixture
    def mouse(self):
        return mouse.Mouse(usbhid.FakeDevice(), rival500.profile)

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x03\x00\x01\x00\x00\x42"),
        (200, b"\x02\x00\x03\x00\x01\x01\x00\x42"),
        (1000, b"\x02\x00\x03\x00\x01\x09\x00\x42"),
        (12000, b"\x02\x00\x03\x00\x01\x77\x00\x42"),
        ])
    def test_set_sensitivity1(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity1(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (100, b"\x02\x00\x03\x00\x02\x00\x00\x42"),
        (200, b"\x02\x00\x03\x00\x02\x01\x00\x42"),
        (1000, b"\x02\x00\x03\x00\x02\x09\x00\x42"),
        (12000, b"\x02\x00\x03\x00\x02\x77\x00\x42"),
        ])
    def test_set_sensitivity2(self, mouse, value, expected_hid_report):
        mouse.set_sensitivity2(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        (125, b"\x02\x00\x04\x00\x04"),
        (250, b"\x02\x00\x04\x00\x03"),
        (500, b"\x02\x00\x04\x00\x02"),
        (1000, b"\x02\x00\x04\x00\x01"),
        ])
    def test_set_polling_rate(self, mouse, value, expected_hid_report):
        mouse.set_polling_rate(value)
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert hid_report == expected_hid_report

    # @pytest.mark.parametrize("value,expected_hid_report", [
        # ("#ABCDEF", b"\x03\x00\x05\x00\x00\xAB\xCD\xEF\xFF\x32\xC8\xC8\x00\x00\x01"),  # noqa
        # ("red", b"\x03\x00\x05\x00\x00\xFF\x00\x00\xFF\x32\xC8\xC8\x00\x00\x01"),  # noqa
        # ])
    # def test_set_logo_color(self, mouse, value, expected_hid_report):
        # mouse.set_logo_color(value)
        # mouse._hid_device.bytes.seek(0)
        # hid_report = mouse._hid_device.bytes.read()
        # assert hid_report == expected_hid_report

    # @pytest.mark.parametrize("value,expected_hid_report", [
        # ("#ABCDEF", b"\x03\x00\x05\x00\x01\xAB\xCD\xEF\xFF\x32\xC8\xC8\x00\x01\x01"),  # noqa
        # ("red", b"\x03\x00\x05\x00\x01\xFF\x00\x00\xFF\x32\xC8\xC8\x00\x01\x01"),  # noqa
        # ])
    # def test_set_wheel_color(self, mouse, value, expected_hid_report):
        # mouse.set_wheel_color(value)
        # mouse._hid_device.bytes.seek(0)
        # hid_report = mouse._hid_device.bytes.read()
        # assert hid_report == expected_hid_report

    @pytest.mark.parametrize("value,expected_hid_report", [
        ("default", b"\x02\x00\x31\x00\x01\x00\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x06\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33\x00\x00\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00"),  # noqa
        ("buttons(button2=button6)", b"\x02\x00\x31\x00\x01\x00\x00\x00\x00\x06\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x00\x05\x00\x00\x00\x00\x06\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33\x00\x00\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00"),  # noqa
        ])
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
