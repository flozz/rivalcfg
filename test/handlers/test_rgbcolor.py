import argparse

import pytest

from rivalcfg.handlers import rgbcolor


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "rgbcolor",
        }

    @pytest.mark.parametrize(
        "color",
        ["#FF2200", "#ff2200", "FF2200", "ff2200", "#F20", "#f20", "F20", "f20"],
    )
    def test_valid_color_hex_string(self, setting_info, color):
        bytes_ = rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0xFF, 0x22, 0x00]

    @pytest.mark.parametrize(
        "color,result",
        [
            # fmt: off
            ("white",   [0xFF, 0xFF, 0xFF]),
            ("silver",  [0xC0, 0xC0, 0xC0]),
            ("gray",    [0x80, 0x80, 0x80]),
            ("black",   [0x00, 0x00, 0x00]),
            ("red",     [0xFF, 0x00, 0x00]),
            ("maroon",  [0x80, 0x00, 0x00]),
            ("yellow",  [0xFF, 0xFF, 0x00]),
            ("olive",   [0x80, 0x80, 0x00]),
            ("lime",    [0x00, 0xFF, 0x00]),
            ("green",   [0x00, 0x80, 0x00]),
            ("aqua",    [0x00, 0xFF, 0xFF]),
            ("teal",    [0x00, 0x80, 0x80]),
            ("blue",    [0x00, 0x00, 0xFF]),
            ("navy",    [0x00, 0x00, 0x80]),
            ("fuchsia", [0xFF, 0x00, 0xFF]),
            ("purple",  [0x80, 0x00, 0x80]),
            # fmt: on
        ],
    )
    def test_named_colors(self, setting_info, color, result):
        bytes_ = rgbcolor.process_value(setting_info, color)
        assert bytes_ == result

    def test_not_valid_color_string(self, setting_info):
        with pytest.raises(ValueError):
            rgbcolor.process_value(setting_info, "hello")

    @pytest.mark.parametrize(
        "color",
        [
            (0xFF, 0x18, 0x00),
            [0xFF, 0x18, 0x00],
        ],
    )
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


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        rgbcolor.add_cli_option(
            cli,
            "color0",
            {
                "label": "LED color",
                "description": "Set the mouse backlight color",
                "cli": ["-c", "--color", "--foobar"],
                "command": [0x05, 0x00],
                "value_type": "rgbcolor",
                "default": "#FF1800",
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-c" in cli.format_help()
        assert "--color" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-c COLOR0" in cli.format_help()

    def test_default_value_displayed(self, cli):
        assert "#FF1800" in cli.format_help()

    @pytest.mark.parametrize(
        "color",
        [
            "#AABBCC",
            "#aaBBcc",
            "AAbbCC",
            "#ABC",
            "AbC",
            "red",
        ],
    )
    def test_passing_valid_color_arguments(self, cli, color):
        params = cli.parse_args(["--color", color])
        assert params.COLOR0 == color

    @pytest.mark.parametrize(
        "color",
        [
            "hello",
            "#AABBCCFF",
            "~AABBCC",
            "#HHIIFF",
            "fa0b",
        ],
    )
    def test_passing_invalid_color_arguments(self, cli, color):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--color", color])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
