import pytest

from rivalcfg.handlers import rgbcolor


class TestProcessValue(object):

    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "rgbcolor",
            }

    @pytest.mark.parametrize("color", [
        "#FF2200", "#ff2200", "FF2200", "ff2200",
        "#F20", "#f20", "F20", "f20",
        ])
    def test_valid_color_hex_string(self, setting_info, color):
        bytes_ = rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0xFF, 0x22, 0x00]

    def test_not_valid_color_string(self, setting_info):
        with pytest.raises(ValueError):
            rgbcolor.process_value(setting_info, "hello")

    @pytest.mark.parametrize("color", [
        (0xFF, 0x18, 0x00),
        [0xFF, 0x18, 0x00],
        ])
    def test_valid_color_tuple(self, setting_info, color):
        bytes_ = rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0xFF, 0x18, 0x00]

    def test_not_valid_color_tuple_2_channels(self, setting_info):
        with pytest.raises(ValueError):
            rgbcolor.process_value(setting_info, [0xFF, 0x18])

    def test_not_valid_color_tuple_wrong_range(self, setting_info):
        with pytest.raises(ValueError):
            rgbcolor.process_value(setting_info, [-1, 256, 1337])

    def test_not_valid_color_ints_wrong_type(self, setting_info):
        with pytest.raises(ValueError):
            rgbcolor.process_value(setting_info, ["ff", "18", "00"])
