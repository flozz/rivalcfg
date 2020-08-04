import argparse

import pytest

from rivalcfg.handlers import multi_rgbcolor


class TestProcessValue(object):

    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "multi_rgbcolor",
            "color_count": 4,
            }

    @pytest.mark.parametrize("color", [
        "#FF2200", "#ff2200", "FF2200", "ff2200",
        "#F20", "#f20", "F20", "f20",
        ])
    def test_valid_single_color_hex_string(self, setting_info, color):
        bytes_ = multi_rgbcolor.process_value(setting_info, color)
        assert bytes_ == [
                0xFF, 0x22, 0x00,
                0xFF, 0x22, 0x00,
                0xFF, 0x22, 0x00,
                0xFF, 0x22, 0x00]

    def test_valid_multiple_color_hex_string(self, setting_info):
        bytes_ = multi_rgbcolor.process_value(
                setting_info,
                "#112233,#456,778899,AaBbCc")
        assert bytes_ == [
            0x11, 0x22, 0x33,
            0x44, 0x55, 0x66,
            0x77, 0x88, 0x99,
            0xAA, 0xBB, 0xCC,
        ]

    @pytest.mark.parametrize("color,result", [
        ("white",   [
            0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF]),
        ("red",     [
            0xFF, 0x00, 0x00,
            0xFF, 0x00, 0x00,
            0xFF, 0x00, 0x00,
            0xFF, 0x00, 0x00]),
        ("purple,red,lime,blue",  [
            0x80, 0x00, 0x80,
            0xFF, 0x00, 0x00,
            0x00, 0xFF, 0x00,
            0x00, 0x00, 0xFF]),
        ])
    def test_named_colors(self, setting_info, color, result):
        bytes_ = multi_rgbcolor.process_value(setting_info, color)
        assert bytes_ == result

    def test_not_valid_color_string(self, setting_info):
        with pytest.raises(ValueError):
            multi_rgbcolor.process_value(setting_info, "hello")

    @pytest.mark.parametrize("color", [
        (0xFF, 0x18, 0x00),
        [0xFF, 0x18, 0x00],
        [[0xFF, 0x18, 0x00]],
        ])
    def test_valid_color_tuple(self, setting_info, color):
        bytes_ = multi_rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0xFF, 0x18, 0x00] * 4

    def test_valid_color_tuples_mixed_with_strings(self, setting_info):
        bytes_ = multi_rgbcolor.process_value(setting_info, [
            (255, 0, 0), [0, 255, 00], "blue", "#ff1800"
            ])
        assert bytes_ == [
                0xFF, 0x00, 0x00,
                0x00, 0xFF, 0x00,
                0x00, 0x00, 0xFF,
                0xFF, 0x18, 0x00]

    def test_not_valid_color_tuple_2_channels(self, setting_info):
        with pytest.raises(ValueError):
            multi_rgbcolor.process_value(setting_info, [0xFF, 0x18])

    def test_not_valid_color_tuple_wrong_range(self, setting_info):
        with pytest.raises(ValueError):
            multi_rgbcolor.process_value(setting_info, [-1, 256, 1337])

    def test_not_valid_color_ints_wrong_type(self, setting_info):
        with pytest.raises(ValueError):
            multi_rgbcolor.process_value(setting_info, ["ff", "18", "00"])

    @pytest.mark.parametrize("colors", [
        ((0xFF, 0x18, 0x00), "red"),
        "red, green, blue",
        "aqua, lime, yellow, purple, black",
        ])
    def test_wrong_color_count(self, setting_info, colors):
        with pytest.raises(ValueError):
            multi_rgbcolor.process_value(setting_info, colors)


class TestAddCliOption(object):

    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        multi_rgbcolor.add_cli_option(cli, "color0", {
                "label": "LED color",
                "description": "Set the mouse backlight color",
                "cli": ["-c", "--color", "--foobar"],
                "command": [0x05, 0x00],
                "value_type": "multi_rgbcolor",
                "color_count": 4,
                "default": "#FF1800"
            })
        return cli

    def test_cli_options(self, cli):
        assert "-c" in cli.format_help()
        assert "--color" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-c COLOR0" in cli.format_help()

    def test_default_value_displayed(self, cli):
        assert "#FF1800" in cli.format_help()

    @pytest.mark.parametrize("color", [
        "#AABBCC",
        "#aaBBcc",
        "AAbbCC",
        "#ABC",
        "AbC",
        "red",
        ])
    def test_passing_valid_color_arguments(self, cli, color):
        params = cli.parse_args(["--color", color])
        assert params.COLOR0 == color

    @pytest.mark.parametrize("color", [
        "hello",
        "#AABBCCFF",
        "~AABBCC",
        "#HHIIFF",
        "fa0b",
        "red,green",
        ])
    def test_passing_invalid_color_arguments(self, cli, color):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--color", color])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
