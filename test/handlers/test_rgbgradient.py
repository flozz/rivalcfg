import argparse

import pytest

from rivalcfg.handlers import rgbgradient


class TestProcessValue(object):
    @pytest.fixture
    def setting_info1(self):
        return {
            "value_type": "rgbgradient",
            "rgbgradient_header": {
                "header_length": 26,
                "led_id_offsets": [0],
                "duration_offset": 1,
                "duration_length": 2,
                "repeat_offset": 17,
                "triggers_offset": 21,
                "color_count_offset": 25,
            },
            "led_id": 2,
        }

    # Color string

    @pytest.mark.parametrize(
        "color",
        ["#FF2200", "#ff2200", "FF2200", "ff2200", "#F20", "#f20", "F20", "f20"],
    )
    def test_valid_color_hex_string(self, setting_info1, color):
        bytes_ = rgbgradient.process_value(setting_info1, color)
        # fmt: off
        assert bytes_ == [
            0x02, 0xe8, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            # led| duration |
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
            #                                 | rept|
            0x00,   0x00, 0x00, 0x00, 0x01,
            # trig|                 | color_count |
            0xFF, 0x22, 0x00, 0xFF, 0x22, 0x00, 0x00,
            # initial_color | color1          | pos1|
        ]
        # fmt: on

    # Named colors string

    def test_named_colors(self, setting_info1):
        bytes_ = rgbgradient.process_value(setting_info1, "red")
        # fmt: off
        assert bytes_ == [
            0x02, 0xe8, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            # led| duration |
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
            #                                 | rept|
            0x00,   0x00, 0x00, 0x00, 0x01,
            # trig|                 | color_count |
            0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00,
            # initial_color | color1          | pos1|
        ]
        # fmt: on

    def test_not_valid_color_string(self, setting_info1):
        with pytest.raises(ValueError):
            rgbgradient.process_value(setting_info1, "hello")

    # Color tuple

    @pytest.mark.parametrize(
        "color",
        [
            (0xFF, 0x18, 0x00),
            [0xFF, 0x18, 0x00],
        ],
    )
    def test_valid_color_tuple(self, setting_info1, color):
        bytes_ = rgbgradient.process_value(setting_info1, color)
        # fmt: off
        assert bytes_ == [
            0x02, 0xe8, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            # led| duration |
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
            #                                 | rept|
            0x00,   0x00, 0x00, 0x00, 0x01,
            # trig|                 | color_count |
            0xFF, 0x18, 0x00, 0xFF, 0x18, 0x00, 0x00,
            # initial_color | color1          | pos1|
        ]
        # fmt: on

    def test_not_valid_color_tuple_2_channels(self, setting_info1):
        with pytest.raises(ValueError):
            rgbgradient.process_value(setting_info1, [0xFF, 0x18])

    def test_not_valid_color_tuple_wrong_range(self, setting_info1):
        with pytest.raises(ValueError):
            rgbgradient.process_value(setting_info1, [-1, 256, 1337])

    def test_not_valid_color_ints_wrong_type(self, setting_info1):
        with pytest.raises(ValueError):
            rgbgradient.process_value(setting_info1, ["ff", "18", "00"])

    # RGB Gradient dict

    def test_valid_rgbgradient_dict(self, setting_info1):
        bytes_ = rgbgradient.process_value(
            setting_info1,
            {
                "duration": 1000,
                "colors": [
                    {"pos": 0, "color": "red"},
                    {"pos": 33, "color": "#00FF00"},
                    {"pos": 66, "color": (0, 0, 0xFF)},
                ],
            },
        )
        # fmt: off
        assert bytes_ == [
            0x02, 0xe8, 0x03, 0x00, 0x00, 0x00,
            # led| duration |
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            #
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04,
            #   | rept|                 | trig|                 | color_count |
            0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00,
            # initial_color | color1          | pos1| | color2        |
            0x54,   0x00, 0x00, 0xFF, 0x54, 0xFF, 0x00, 0x00, 0x57,
            # pos2| color3          | pos3| color4 (=color1)| pos4|
        ]
        # fmt: on

    # RGB Gradient String

    @pytest.mark.parametrize(
        "color",
        [
            "rgbgradient(colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            "rgbgradient(colors=0: #ff0000, 33: #00ff00, 66: #0000ff)",
            "rgbgradient(colors=0:#ff0000,33:#00ff00,66:#0000ff)",
            "rgbgradient(colors=0%: red, 33%: lime, 66%: blue)",
            "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            "rgbgradient(colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff; duration=1000)",
        ],
    )
    def test_valid_rgbgradient(self, setting_info1, color):
        bytes_ = rgbgradient.process_value(setting_info1, color)
        # fmt: off
        assert bytes_ == [
            0x02, 0xe8, 0x03, 0x00, 0x00, 0x00,
            # led| duration |
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            #
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04,
            #   | rept|                 | trig|                 | color_count |
            0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00,
            # initial_color | color1          | pos1| | color2        |
            0x54,   0x00, 0x00, 0xFF, 0x54, 0xFF, 0x00, 0x00, 0x57,
            # pos2| color3          | pos3| color4 (=color1)| pos4|
        ]
        # fmt: on

    # TODO Test different header layouts


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        rgbgradient.add_cli_option(
            cli,
            "color0",
            {
                "label": "Logo LED colors and effects",
                "description": "Set the colors and the effects of the logo LED",
                "cli": ["-c", "--logo-color", "--foobar"],
                "report_type": 0x03,  # FEATURE REPORT
                "command": [0x5B, 0x00, 0x00],
                "value_type": "rgbgradient",
                "rgbgradient_header": {
                    "header_length": 26,
                    "led_id_offsets": [0],
                    "duration_offset": 1,
                    "duration_length": 2,
                    "repeat_offset": 17,
                    "triggers_offset": 21,
                    "color_count_offset": 25,
                },
                "led_id": 0x02,
                "default": "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-c" in cli.format_help()
        assert "--logo-color" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-c COLOR0" in cli.format_help()

    def test_default_value_displayed(self, cli):
        assert "rgbgradient(" in cli.format_help()

    @pytest.mark.parametrize(
        "color",
        [
            "#AABBCC",
            "#aaBBcc",
            "AAbbCC",
            "#ABC",
            "AbC",
            "red",
            "rgbgradient(duration=1000; colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            "rgbgradient(colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff; duration=1000;)",
            "rgbgradient(colors=0%: #ff0000, 33%: #00ff00, 66%: #0000ff)",
            "rgbgradient(colors=0:red,33:#0f0,66:00f)",
        ],
    )
    def test_passing_valid_color_arguments(self, cli, color):
        params = cli.parse_args(["--logo-color", color])
        assert params.COLOR0 == color

    @pytest.mark.parametrize(
        "color",
        [
            "hello",
            "#AABBCCFF",
            "~AABBCC",
            "#HHIIFF",
            "fa0b",
            "rgbgradient()",
        ],
    )
    def test_passing_invalid_color_arguments(self, cli, color):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--logo-color", color])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
