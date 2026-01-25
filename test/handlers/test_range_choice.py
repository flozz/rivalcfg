import argparse

import pytest

from rivalcfg.handlers import range_choice


class Test_find_nearest_choice(object):
    @pytest.fixture
    def choices(self):
        return {
            100: 0x00,
            200: 0x02,
            300: 0x03,
            400: 0x05,
            500: 0x06,
            600: 0x08,
            700: 0x10,
            800: 0x11,
            900: 0x13,
            1000: 0x1A,
        }

    @pytest.mark.parametrize(
        "input_,expected_output",
        [
            (99, 100),
            (100, 100),
            (150, 100),
            (151, 200),
            (999, 1000),
            (1000, 1000),
            (3000, 1000),
        ],
    )
    def test_values(self, choices, input_, expected_output):
        assert (
            range_choice.find_nearest_choice(choices.keys(), input_) == expected_output
        )


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "range",
            "input_range": [100, 1000, 100],
            "output_choices": {
                100: 0x00,
                200: 0x02,
                300: 0x03,
                400: 0x06,
                500: 0x10,
                600: 0x1A,
                700: 0x2B,
                800: 0xCC,
                900: 0xDD,
                1000: 0xFF,
            },
        }

    @pytest.fixture
    def setting_info2(self):
        return {
            "value_type": "range",
            "input_range": [100, 1000, 100],
            "output_choices": {
                100: 0x00,
                200: 0x02,
                300: 0x03,
                400: 0x06,
                500: 0x10,
                600: 0x1A,
                700: 0x2B,
                800: 0xCC,
                900: 0xDD,
                1000: 0xFFEE,
            },
            "range_length_byte": 2,
        }

    @pytest.mark.parametrize(
        "input_,expected_output",
        [
            (100, 0x00),
            (200, 0x02),
            (1000, 0xFF),
            (150, 0x00),
            (151, 0x02),
            ("300", 0x03),
        ],
    )
    def test_range_values(self, setting_info, input_, expected_output):
        assert range_choice.process_value(setting_info, input_) == [expected_output]

    @pytest.mark.parametrize(
        "input_,expected_output",
        [
            (100, [0x00, 0x00]),
            (200, [0x02, 0x00]),
            (500, [0x10, 0x00]),
            (1000, [0xEE, 0xFF]),
        ],
    )
    def test_range_values2(self, setting_info2, input_, expected_output):
        assert range_choice.process_value(setting_info2, input_) == expected_output


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        range_choice.add_cli_option(
            cli,
            "sensitivity42",
            {
                "label": "Sensibility preset 1",
                "description": "Set sensitivity preset 1 (DPI)",
                "cli": ["-s", "--sensitivity1", "--foobar"],
                "command": [0x03, 0x01],
                "value_type": "range_choice",
                "input_range": [199, 1000, 100],
                "output_choices": {
                    100: 0x00,
                    200: 0x02,
                    300: 0x03,
                    400: 0x06,
                    500: 0x10,
                    600: 0x1A,
                    700: 0x2B,
                    800: 0xCC,
                    900: 0xDD,
                    1000: 0xFF,
                },
                "default": 200,
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-s" in cli.format_help()
        assert "--sensitivity1" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-s SENSITIVITY42" in cli.format_help()

    @pytest.mark.parametrize(
        "value",
        [
            "200",
            "210",
            "7200",
        ],
    )
    def test_passing_valid_value(self, cli, value):
        params = cli.parse_args(["--sensitivity1", value])
        assert params.SENSITIVITY42 == int(value)

    def test_passing_invalid_value(self, cli):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--sensitivity1", "hello"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
