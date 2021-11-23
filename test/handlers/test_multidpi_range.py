import argparse

import pytest

from rivalcfg.handlers import multidpi_range


class TestProcessValue(object):
    @pytest.fixture
    def setting_info(self):
        return {
            "value_type": "multidpi_range",
            "input_range": [100, 2000, 100],
            "output_range": [1, 20, 1],
            "max_preset_count": 5,
            "dpi_length_byte": 1,
            "first_preset": 1,
            "count_mode": "number",
        }

    @pytest.fixture
    def setting_info2(self):
        return {
            "value_type": "multidpi_range",
            "input_range": [100, 2000, 100],
            "output_range": [1, 20, 1],
            "max_preset_count": 5,
            "dpi_length_byte": 2,
            "first_preset": 1,
            "count_mode": "flag",
        }

    @pytest.fixture
    def setting_info3(self):
        return {
            "value_type": "multidpi_range",
            "input_range": [100, 2000, 100],
            "output_range": [1, 20, 1],
            "max_preset_count": 5,
            "dpi_length_byte": 1,
            "first_preset": 0,
            "count_mode": "number",
        }

    @pytest.mark.parametrize(
        "input_,expected_output",
        [
            (100, [0x01, 0x01, 0x01]),
            ("100", [0x01, 0x01, 0x01]),
            ([100, 200, 300], [0x03, 0x01, 0x01, 0x02, 0x03]),
            ("100, 200, 300", [0x03, 0x01, 0x01, 0x02, 0x03]),
            ("100,200,300", [0x03, 0x01, 0x01, 0x02, 0x03]),
            ("100,200,300,400,500", [0x05, 0x01, 0x01, 0x02, 0x03, 0x04, 0x05]),
        ],
    )
    def test_values(self, setting_info, input_, expected_output):
        assert multidpi_range.process_value(setting_info, input_) == expected_output

    @pytest.mark.parametrize(
        "input_",
        [
            "100, 200, 300, 400, 500, 600",
            [100, 200, 300, 400, 500, 600],
        ],
    )
    def test_too_many_pressets(self, setting_info, input_):
        with pytest.raises(ValueError):
            multidpi_range.process_value(setting_info, input_)

    def test_too_fiew_pressets(self, setting_info):
        with pytest.raises(ValueError):
            multidpi_range.process_value(setting_info, [])

    @pytest.mark.parametrize(
        "selected",
        [0, 1, 2, 3, 4],
    )
    def test_selected_preset(self, setting_info, selected):
        assert (
            multidpi_range.process_value(
                setting_info,
                "100,200,300,400,500",
                selected_preset=selected,
            )
            == [0x05, selected + 1, 0x01, 0x02, 0x03, 0x04, 0x05]
        )

    def test_selected_preset_out_of_range(self, setting_info):
        with pytest.raises(ValueError):
            multidpi_range.process_value(
                setting_info,
                "100,200",
                selected_preset=2,
            )

    def test_count_format_flag(self, setting_info2):
        # fmt: off
        assert (
            multidpi_range.process_value(setting_info2, "100,200")
            == [0b00000011, 0x01, 0x01, 0x00, 0x02, 0x00]
            # . COUNT,      SEL,  PRESSET1,   PRESSET2
        )
        # fmt: on

    def test_first_preset(self, setting_info3):
        # fmt: off
        assert (
            multidpi_range.process_value(setting_info3, "100,200")
            == [0x02, 0x00, 0x01, 0x02]
            # . CNT,  SEL,  PST1, PST2
        )
        # fmt: on


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        multidpi_range.add_cli_option(
            cli,
            "sensitivity42",
            {
                "label": "Sensibility presets",
                "description": "Set sensitivity presets (DPI)",
                "cli": ["-s", "--sensitivity", "--foobar"],
                "command": [0x03, 0x01],
                "value_type": "range",
                "input_range": [200, 7200, 100],
                "output_range": [0x04, 0xA7, 2.33],
                "max_preset_count": 5,
                "default": 1000,
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-s" in cli.format_help()
        assert "--sensitivity" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-s SENSITIVITY42" in cli.format_help()

    @pytest.mark.parametrize(
        "value",
        [
            "200",
            "210",
            "7200, 400",
        ],
    )
    def test_passing_valid_value(self, cli, value):
        params = cli.parse_args(["--sensitivity", value])
        assert params.SENSITIVITY42 == value

    def test_passing_invalid_value(self, cli):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--sensitivity", "hello"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_passing_too_much_values(self, cli):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--sensitivity", "1,2,3,4,5,6"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
