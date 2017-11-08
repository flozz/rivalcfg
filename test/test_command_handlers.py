import pytest

import rivalcfg.command_handlers


class TestTransform(object):

    def test_one_argument(self):
        value = rivalcfg.command_handlers._transform(
                {"value_transform": lambda v: v * 2}, 4)
        assert value == 8

    def test_multiple_arguments(self):
        values = rivalcfg.command_handlers._transform(
                {"value_transform": lambda a, b: (a * 2, b * 4)}, 8, 4)
        assert values == (16, 16)

    def test_one_argument_with_no_transform_function(self):
        value = rivalcfg.command_handlers._transform({}, 4)
        assert value == 4

    def test_multiple_arguments_with_no_transform_function(self):
        values = rivalcfg.command_handlers._transform({}, 8, 4)
        assert values == (8, 4)


class TestChoiceHandler(object):

    @pytest.fixture
    def choice_command(self):
        return {
            "command": [0x01, 0x02],
            "choices": {
                0: 0xAA,
                10: 0xBB,
                20: 0xCC
                }
            }

    @pytest.fixture
    def choice_command_transform(self):
        return {
            "command": [0x02],
            "choices": {1: 0xAB},
            "value_transform": lambda v: v - 1
            }

    def test_valid_choice(self, choice_command):
        bytes_ = rivalcfg.command_handlers.choice_handler(choice_command, 10)
        assert bytes_ == [0x01, 0x02, 0xBB]

    def test_not_valid_choice(self, choice_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.choice_handler(choice_command, 42)

    def test_value_tranform(self, choice_command_transform):
        bytes_ = rivalcfg.command_handlers.choice_handler(
                choice_command_transform, 1)
        assert bytes_ == [0x02, 0xAA]


class TestRgbcolorHandler(object):

    @pytest.fixture
    def rgbcolor_command(self):
        return {"command": [0x01, 0x02]}

    @pytest.fixture
    def rgbcolor_command_transform(self):
        return {
            "command": [0x02],
            "value_transform": lambda r, g, b: (r-1, g+2, b+10)
            }

    def test_valid_color_string(self, rgbcolor_command):
        bytes_ = rivalcfg.command_handlers.rgbcolor_handler(
                rgbcolor_command, "#ff1800")
        assert bytes_ == [0x01, 0x02, 0xFF, 0x18, 0x00]

    def test_not_valid_color_string(self, rgbcolor_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.rgbcolor_handler(
                    rgbcolor_command, "hello")

    def test_valid_color_ints(self, rgbcolor_command):
        bytes_ = rivalcfg.command_handlers.rgbcolor_handler(
                rgbcolor_command, 0xFF, 0x18, 0x00)
        assert bytes_ == [0x01, 0x02, 0xFF, 0x18, 0x00]

    def test_not_valid_color_ints_2_channels(self, rgbcolor_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.rgbcolor_handler(
                    rgbcolor_command, 0xFF, 0x18)

    def test_not_valid_color_ints_wrong_range(self, rgbcolor_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.rgbcolor_handler(
                    rgbcolor_command, -1, 256, 1337)

    def test_not_valid_color_ints_wrong_type(self, rgbcolor_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.rgbcolor_handler(
                    rgbcolor_command, "ff", "18", "00")

    def test_color_command_with_transform(self, rgbcolor_command_transform):
        bytes_ = rivalcfg.command_handlers.rgbcolor_handler(
                rgbcolor_command_transform,  0xFF, 0x18, 0x00)
        assert bytes_ == [0x02, 0xFE, 0x1A, 0x0A]


class TestRgbcolorshiftHandler(object):

    @pytest.fixture
    def rgbcolorshift_command(self):
        return {"command": [0x01, 0x02]}

    @pytest.fixture
    def rgbcolorshift_command_transform(self):
        return {
            "command": [0x02],
            "value_transform": lambda cs, s: (
                (cs[0]+1, cs[1]+1, cs[2]+1, cs[3]+1, cs[4]+1, cs[5]+1), s+1)
            }

    def test_valid_colors(self, rgbcolorshift_command):
        bytes_ = rivalcfg.command_handlers.rgbcolorshift_handler(
                rgbcolorshift_command,
                [[0x01, 0x02, 0x03], [0x06, 0x05, 0x04]],
                0x88)
        assert bytes_ == [
                0x01, 0x02, 0x01, 0x02, 0x03, 0x06, 0x05, 0x04, 0x88, 0x00]
        bytes_ = rivalcfg.command_handlers.rgbcolorshift_handler(
                rgbcolorshift_command, ["010203", "#060504"], 0x88)
        assert bytes_ == [
                0x01, 0x02, 0x01, 0x02, 0x03, 0x06, 0x05, 0x04, 0x88, 0x00]

    def test_valid_colors_and_no_with_tranform(self, rgbcolorshift_command_transform):  # noqa
        bytes_ = rivalcfg.command_handlers.rgbcolorshift_handler(
                rgbcolorshift_command_transform,
                [[0x01, 0x02, 0x03], [0x06, 0x05, 0x04]],
                0x88)
        assert bytes_ == [0x02, 0x02, 0x03, 0x04, 0x07, 0x06, 0x05, 0x89, 0x00]


class TestRangeHandler(object):

    @pytest.fixture
    def range_command(self):
        return {
            "command": [0x01, 0x02],
            "range_min": 50,
            "range_max": 150
            }

    @pytest.fixture
    def range_command_increment(self):
        return {
            "command": [0x02],
            "range_min": 50,
            "range_max": 150,
            "range_increment": 50
            }

    @pytest.fixture
    def range_command_transform(self):
        return {
            "command": [0x03],
            "range_min": 50,
            "range_max": 150,
            "value_transform": lambda v: v * 2
            }

    def test_valid_value(self, range_command):
        bytes_ = rivalcfg.command_handlers.range_handler(range_command, 0x88)
        assert bytes_ == [0x01, 0x02, 0x88]

    def test_value_smaller_than_min(self, range_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.range_handler(range_command, 42)

    def test_value_greater_than_max(self, range_command):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.range_handler(range_command, 151)

    def test_value_multiple_of_increment(self, range_command_increment):
        bytes_ = rivalcfg.command_handlers.range_handler(
                range_command_increment, 0x96)
        assert bytes_ == [0x02, 0x96]

    def test_value_not_multiple_of_increment(self, range_command_increment):
        with pytest.raises(ValueError):
            rivalcfg.command_handlers.range_handler(
                    range_command_increment, 101)

    def test_range_command_with_transform(self, range_command_transform):
        bytes_ = rivalcfg.command_handlers.range_handler(
                range_command_transform, 0x70)
        assert bytes_ == [0x03, 0xE0]


class TestHNoneHandler(object):

    @pytest.fixture
    def none_command(self):
        return {"command": [0x01, 0x02]}

    def test_command_with_no_argument(self, none_command):
        bytes_ = rivalcfg.command_handlers.none_handler(none_command)
        assert bytes_ == [0x01, 0x02]
