import argparse

import pytest

from rivalcfg.handlers import reactive_rgbcolor


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "reactive_rgbcolor",
        }

    @pytest.mark.parametrize(
        "color",
        [
            "#FF0000",
            "ff0000",
            "red",
            [0xFF, 0x00, 0x00],
        ],
    )
    def test_valid_color(self, setting_info, color):
        bytes_ = reactive_rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0x01, 0x00, 0xFF, 0x00, 0x00]

    def test_not_valid_color_string(self, setting_info):
        with pytest.raises(ValueError):
            reactive_rgbcolor.process_value(setting_info, "hello")

    @pytest.mark.parametrize(
        "color",
        [
            "off",
            "OFF",
            "disable",
            "DisabLe",
            None,
        ],
    )
    def test_disabling_effect(self, setting_info, color):
        bytes_ = reactive_rgbcolor.process_value(setting_info, color)
        assert bytes_ == [0x00, 0x00, 0x00, 0x00, 0x00]


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        reactive_rgbcolor.add_cli_option(
            cli,
            "color0",
            {
                "label": "Reactive color",
                "description": "Set the color of the LEDs in reaction to a button click",
                "cli": ["-a", "--reactive-color", "--foobar"],
                "command": [0x26],
                "value_type": "reactive_rgbcolor",
                "default": "off",
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-a" in cli.format_help()
        assert "--reactive-color" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-a COLOR0" in cli.format_help()

    def test_default_value_displayed(self, cli):
        assert "off" in cli.format_help()

    @pytest.mark.parametrize(
        "color",
        [
            "#AABBCC",
            "#aaBBcc",
            "AAbbCC",
            "#ABC",
            "AbC",
            "red",
            "off",
            "oFf",
            "disable",
        ],
    )
    def test_passing_valid_arguments(self, cli, color):
        params = cli.parse_args(["--reactive-color", color])
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
    def test_passing_invalid_arguments(self, cli, color):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--reactive-color", color])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
