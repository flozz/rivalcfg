import argparse

import pytest

from rivalcfg.handlers import choice


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "choice",
            "choices": {
                "foo": 0xDD,
                0: 0xAA,
                10: 0xBB,
                20: 0xCC,
            },
        }

    def test_valid_choice_int(self, setting_info):
        assert choice.process_value(setting_info, 10) == [0xBB]

    def test_valid_choice_str_int(self, setting_info):
        assert choice.process_value(setting_info, "10") == [0xBB]

    def test_valid_choice_str(self, setting_info):
        assert choice.process_value(setting_info, "foo") == [0xDD]

    def test_not_valid_choice(self, setting_info):
        with pytest.raises(ValueError):
            choice.process_value(setting_info, 42)


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        choice.add_cli_option(
            cli,
            "light_effect0",
            {
                "label": "Light effect",
                "description": "Set the light effect",
                "cli": ["-e", "--light-effect", "--foobar"],
                "command": [0x07, 0x00],
                "value_type": "choice",
                "choices": {
                    "steady": 0x01,
                    "breath": 0x03,
                    1: 0x01,
                    2: 0x02,
                    3: 0x03,
                    4: 0x04,
                },
                "default": "steady",
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-e" in cli.format_help()
        assert "--light-effect" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-e LIGHT_EFFECT0" in cli.format_help()

    @pytest.mark.parametrize(
        "choice",
        [
            "steady",
            "breath",
            "3",
        ],
    )
    def test_passing_valid_value(self, cli, choice):
        params = cli.parse_args(["--light-effect", choice])
        assert params.LIGHT_EFFECT0 == choice

    @pytest.mark.parametrize(
        "choice",
        [
            "hello",
            "42",
        ],
    )
    def test_passing_invalid_value(self, cli, choice):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--light-effect", choice])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
