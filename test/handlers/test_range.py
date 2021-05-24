import argparse

import pytest

from rivalcfg.handlers import range as range_


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "range",
            "input_range": [100, 2000, 100],
            "output_range": [2, 40, 2],
        }

    @pytest.mark.parametrize(
        "input_,expected_output",
        [
            (100, 2),
            (200, 4),
            (2000, 40),
            (149, 2),
            (150, 4),
            ("300", 6),
        ],
    )
    def test_range_values(self, setting_info, input_, expected_output):
        assert range_.process_value(setting_info, input_) == [expected_output]


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        range_.add_cli_option(
            cli,
            "sensitivity42",
            {
                "label": "Sensibility preset 1",
                "description": "Set sensitivity preset 1 (DPI)",
                "cli": ["-s", "--sensitivity1", "--foobar"],
                "command": [0x03, 0x01],
                "value_type": "range",
                "input_range": [200, 7200, 100],
                "output_range": [0x04, 0xA7, 2.33],
                "default": 1000,
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
