import pytest

import rivalcfg.mouse


PROFILE = {
    "name": "Fake Mouse",

    "vendor_id": 0x1038,
    "product_id": 0x0001,
    "interface_number": 0,

    "commands": {
        "choice_command": {
            "command": [0x01],
            "value_type": "choice",
            "choices": {
                1: 2,
                2: 4
            }
        },
        "rgbcolor_command": {
            "command": [0x02],
            "value_type": "rgbcolor",
        },
        "range_command": {
            "command": [0x03],
            "value_type": "range",
            "range_min": 4,
            "range_max": 10,
            "range_increment": 2
        },
        "none_command": {
            "command": [0x01, 0x02, 0x03],
            "value_type": None
        },
        "undefined_handler_command": {
            "command": [0x04],
            "value_type": "foo"
        }
    }
}


@pytest.fixture(scope="function")
def mouse(monkeypatch):
    monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
    monkeypatch.setattr("rivalcfg.debug.DRY", True)
    monkeypatch.setenv("RIVALCFG_PROFILE", "1038:0001")
    return rivalcfg.mouse.Mouse(PROFILE)


def _get_written_bytes(mouse):
    mouse._device.seek(0)
    result = mouse._device.read()
    if result[0:1] == b"\x00":
        result = result[1:]
    return result


class TestGetattr(object):

    def test_choice_handler(self, mouse):
        mouse.choice_command(2)
        assert _get_written_bytes(mouse) == b"\x01\x04"

    def test_rgbcolor_handler(self, mouse):
        mouse.rgbcolor_command(0xFF, 0x18, 0x00)
        assert _get_written_bytes(mouse) == b"\x02\xFF\x18\x00"

    def test_range_handler(self, mouse):
        mouse.range_command(10)
        assert _get_written_bytes(mouse) == b"\x03\x0A"

    def test_none_hanlder(self, mouse):
        mouse.none_command()
        assert _get_written_bytes(mouse) == b"\x01\x02\x03"

    def test_undefined_method(self, mouse):
        with pytest.raises(AttributeError):
            mouse.foo_command()

    def test_undefined_handler(self, mouse):
        with pytest.raises(Exception):
            mouse.undefined_handler_command()


class TestStrRepr(object):

    def test_str(self, mouse):
        assert str(mouse) == "<Mouse Fake Mouse (1038:0001:00)>"

    def test_repr(self, mouse):
        assert repr(mouse) == "<Mouse Fake Mouse (1038:0001:00)>"
