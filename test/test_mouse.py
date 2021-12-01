import pytest

from rivalcfg import mouse
from rivalcfg import usbhid
from rivalcfg import mouse_settings


FAKE_PROFILE = {
    "name": "Fake Mouse",
    "vendor_id": 0x1038,
    "product_id": 0xBAAD,
    "endpoint": 2,
    "settings": {
        "setting1": {
            "label": "Setting 1",
            "description": "A setting with no value",
            "cli": ["-1", "--setting1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0xAA, 0xBB],
            "value_type": None,
        },
        "setting2": {
            "label": "Setting 2",
            "description": "A setting with a simple choice value",
            "cli": ["-2", "--setting2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0xCC],
            "value_type": "choice",
            "choices": {
                "foo": 0x01,
                "bar": 0x02,
            },
            "default": "bar",
        },
        "setting3": {
            "label": "Setting 3",
            "description": "A setting that uses HID feature report",
            "cli": ["-3", "--setting3"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0xC0, 0x10, 0x25],
            "value_type": None,
        },
        "setting4": {
            "label": "Setting 4",
            "description": "A setting that use a fixed packet length",
            "cli": ["-4", "--setting4"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x11, 0x22],
            "packet_length": 10,
            "value_type": None,
        },
        "setting5": {
            "label": "Setting 5",
            "description": "A setting with a command suffix",
            "cli": ["-5", "--setting5"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x11, 0x22],
            "command_suffix": [0x33, 0x44],
            "value_type": "choice",
            "choices": {
                42: 0xAA,
            },
            "default": 42,
        },
        "setting6": {
            "label": "Setting 6",
            "description": "A setting with no value",
            "cli": ["-6", "--setting6"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x20, 0x2E],
            "value_type": "none",
        },
        "setting_readback": {
            "label": "Setting with readback",
            "description": "A setting with no value",
            "cli": ["-7", "--setting7"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x20, 0x2F],
            "value_type": "none",
            "readback_length": 42,
        },
        "setting_no_readback": {
            "label": "Setting without readback",
            "description": "A setting with no value",
            "cli": ["-8", "--setting8"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x20, 0x2F],
            "value_type": "none",
            "readback_length": 0,
        },
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x5A, 0x0E],
    },
}

FAKE_PROFILE2 = {
    "name": "Fake Mouse 2",
    "vendor_id": 0x1038,
    "product_id": 0xBAD2,
    "endpoint": 2,
    "settings": {},
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "packet_length": 4,
        "command": [0x5A, 0x0E],
    },
}


class TestGetMouse(object):
    def test_get_mouse_returns_mouse_instance_with_desired_profil(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DRY", "1")
        rival100 = mouse.get_mouse(vendor_id=0x1038, product_id=0x1702)
        assert rival100.mouse_profile["vendor_id"] == 0x1038
        assert rival100.mouse_profile["product_id"] == 0x1702

    def test_get_mouse_vendor_id_param_optional(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DRY", "1")
        rival100 = mouse.get_mouse(product_id=0x1702)
        assert rival100.mouse_profile["vendor_id"] == 0x1038
        assert rival100.mouse_profile["product_id"] == 0x1702

    def test_get_mouse_raise_error_if_no_product_id(self):
        with pytest.raises(ValueError):
            mouse.get_mouse()

    @pytest.mark.skip("Not implemented yet")
    def test_get_mouse_raise_error_if_profile_does_not_exists(self):
        pass  # TODO


class TestMouse(object):
    @pytest.fixture
    def mouse(self, monkeypatch):
        return mouse.Mouse(
            usbhid.FakeDevice(),
            FAKE_PROFILE,
            mouse_settings.FakeMouseSettings(0x1038, 0xBAAD, FAKE_PROFILE),
        )

    @pytest.fixture
    def mouse2(self, monkeypatch):
        return mouse.Mouse(
            usbhid.FakeDevice(),
            FAKE_PROFILE2,
            mouse_settings.FakeMouseSettings(0x1038, 0xBAD2, FAKE_PROFILE2),
        )

    def test_name(self, mouse):
        assert mouse.name == "Fake Mouse"

    def test_product_id(self, mouse):
        assert mouse.product_id == 0xBAAD

    def test_firmware_version_tuple(self, mouse):
        assert mouse.firmware_version_tuple == (0,)

    def test_firmware_version(self, mouse):
        assert mouse.firmware_version == "0"

    def test_save(self, mouse):
        mouse.save()
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == b"\x02\x00\x5A\x0E"

    def test_save_fixed_packet_length(self, mouse2):
        mouse2.save()
        mouse2._hid_device.bytes.seek(0)
        data = mouse2._hid_device.bytes.read()
        assert len(data) == 6
        assert data == b"\x02\x00\x5A\x0E\x00\x00"

    def test_reset_settings(self, mouse):
        mouse.reset_settings()
        mouse._hid_device.bytes.seek(0)
        hid_report = mouse._hid_device.bytes.read()
        assert b"\x02\x00\x5A\x0E" not in hid_report  # No save command
        assert b"\x02\x00\xAA\xBB" in hid_report  # setting1
        assert b"\x02\x00\xCC\x02" in hid_report  # setting2
        assert b"\x03\x00\xC0\x10\x25" in hid_report  # setting3

    def test_repr(self, mouse):
        assert str(mouse) == "<Mouse Fake Mouse (1038:baad:02)>"
        assert repr(mouse) == "<Mouse Fake Mouse (1038:baad:02)>"

    @pytest.mark.parametrize(
        "report_type,expected_hid_report",
        [
            (usbhid.HID_REPORT_TYPE_OUTPUT, b"\x02\x00"),
            (usbhid.HID_REPORT_TYPE_FEATURE, b"\x03\x00"),
        ],
    )
    def test__hid_write_with_a_valid_report_type(
        self, mouse, report_type, expected_hid_report
    ):
        mouse._hid_write(report_type=report_type)
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == expected_hid_report

    def test__hid_write_with_a_wrong_report_type(self, mouse):
        with pytest.raises(ValueError):
            mouse._hid_write(report_type=0x42)

    def test__hid_write_with_data(self, mouse):
        mouse._hid_write(
            report_type=usbhid.HID_REPORT_TYPE_OUTPUT,
            report_id=0x42,
            data=[0xDA, 0x7A],
        )
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == b"\x02\x42\xDA\x7A"

    def test__hid_write_with_fixed_packet_length(self, mouse):
        mouse._hid_write(packet_length=4)
        mouse._hid_device.bytes.seek(0)
        data = mouse._hid_device.bytes.read()
        assert len(data) == 6
        assert data == b"\x02\x00\x00\x00\x00\x00"

    # Virtual methods dependent to the loaded profile

    def test_set_setting1_is_available(self, mouse):
        assert hasattr(mouse, "set_setting1")

    def test_set_setting1(self, mouse):
        mouse.set_setting1()
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == b"\x02\x00\xAA\xBB"

    def test_set_setting2_is_available(self, mouse):
        assert hasattr(mouse, "set_setting2")

    @pytest.mark.parametrize(
        "value,expected_hid_report",
        [
            ("foo", b"\x02\x00\xCC\x01"),
            ("bar", b"\x02\x00\xCC\x02"),
        ],
    )
    def test_setting2(self, mouse, value, expected_hid_report):
        mouse.set_setting2(value)
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == expected_hid_report

    def test_set_setting3_is_available(self, mouse):
        assert hasattr(mouse, "set_setting3")

    def test_set_setting3(self, mouse):
        mouse.set_setting3()
        mouse._hid_device.bytes.seek(0)
        assert mouse._hid_device.bytes.read() == b"\x03\x00\xC0\x10\x25"

    def test_set_setting4_packet_length(self, mouse):
        mouse.set_setting4()
        mouse._hid_device.bytes.seek(0)
        data = mouse._hid_device.bytes.read()
        assert len(data) == 12
        assert data == b"\x02\x00\x11\x22\x00\x00\x00\x00\x00\x00\x00\x00"

    def test_set_setting5_command_suffix(self, mouse):
        mouse.set_setting5(42)
        mouse._hid_device.bytes.seek(0)
        data = mouse._hid_device.bytes.read()
        assert data == b"\x02\x00\x11\x22\xAA\x33\x44"

    def test_an_unexisting_setting(self, mouse):
        assert not hasattr(mouse, "set_xxx")
        with pytest.raises(AttributeError):
            mouse.set_xxx()

    def test_readback(self, mouse):
        response = mouse.set_setting_readback()
        assert len(response) == 42

    def test_no_readback(self, mouse):
        response = mouse.set_setting_no_readback()
        assert response is None
        response = mouse.set_setting6()
        assert response is None
