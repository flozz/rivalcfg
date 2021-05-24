import argparse

import pytest

from rivalcfg.handlers import buttons


class TestBuildLayout(object):
    @pytest.fixture
    def layout(self):
        class Layout(object):
            layout = {
                "A": 0x01,
                "PlayPause": 0x02,
                ".": 0x03,
            }
            aliases = {
                "play": "PlayPause",
                "dot": ".",
            }

        return Layout()

    @pytest.fixture
    def layout_err(self):
        class Layout(object):
            layout = {
                "A": 0x01,
                "PlayPause": 0x02,
                ".": 0x03,
            }
            aliases = {
                "play": "Pause",
                "dot": ".",
            }

        return Layout()

    def test_build_layout(self, layout):
        full_layout = buttons.build_layout(layout)

        assert "a" in full_layout
        assert full_layout["a"] == 0x01

        assert "playpause" in full_layout
        assert full_layout["playpause"] == 0x02
        assert "play" in full_layout
        assert full_layout["play"] == 0x02

        assert "." in full_layout
        assert full_layout["."] == 0x03
        assert "dot" in full_layout
        assert full_layout["dot"] == 0x03

    def test_build_layout_with_wrong_alias(self, layout_err):
        with pytest.raises(ValueError):
            buttons.build_layout(layout_err)


class TestProcessValue(object):
    @pytest.fixture
    def setting_info1(self):
        return {
            "value_type": "buttons",
            "buttons": {
                "button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                "button2": {"id": 0x02, "offset": 0x03, "default": "button2"},
            },
            # fmt: off
            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,
            # fmt: on
            "button_field_length": 3,
        }

    @pytest.fixture
    def setting_info2(self):
        return {
            "value_type": "buttons",
            "buttons": {
                "button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                "button2": {"id": 0x02, "offset": 0x03, "default": "button2"},
                "button3": {"id": 0x03, "offset": 0x06, "default": "next"},
                "button4": {"id": 0x04, "offset": 0x09, "default": "dpi"},
            },
            # fmt: off
            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   0x31,
            "button_scroll_down": 0x32,
            # fmt: on
            "button_field_length": 3,
        }

    @pytest.mark.parametrize(
        "value,expected",
        [
            # fmt: off
            ("buttons(button1=button1)", [0x01, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=button2)", [0x02, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=button2; button2=button1)", [0x02, 0x00, 0x00, 0x01, 0x00, 0x00]),
            ("buttons(button1=default)", [0x01, 0x00, 0x00, 0x02, 0x00, 0x00]),
            # fmt: on
        ],
    )
    def test_string_values_buttons(self, setting_info1, value, expected):
        bytes_ = buttons.process_value(setting_info1, value)
        assert bytes_ == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("buttons(button1=A)", [0x51, 0x04, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(layout=qwerty; button1=A)", [0x51, 0x04, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=a)", [0x51, 0x04, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=1)", [0x51, 0x1E, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=Escape)", [0x51, 0x29, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=Esc)", [0x51, 0x29, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=equal)", [0x51, 0x2E, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=eq)", [0x51, 0x2E, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=F1)", [0x51, 0x3A, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=.)", [0x51, 0x37, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=DOT)", [0x51, 0x37, 0x00, 0x02, 0x00, 0x00]),
        ],
    )
    def test_string_values_keyboard_qwerty(self, setting_info1, value, expected):
        bytes_ = buttons.process_value(setting_info1, value)
        assert bytes_ == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("buttons(button1=Mute)", [0x61, 0xE2, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=Next)", [0x61, 0xB5, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=PlayPause)", [0x61, 0xCD, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=Previous)", [0x61, 0xB6, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=VolumeUp)", [0x61, 0xE9, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=VolumeDown)", [0x61, 0xEA, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=Vol+)", [0x61, 0xE9, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=vol+)", [0x61, 0xE9, 0x00, 0x02, 0x00, 0x00]),
        ],
    )
    def test_string_values_multimedia(self, setting_info1, value, expected):
        bytes_ = buttons.process_value(setting_info1, value)
        assert bytes_ == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("buttons(button1=ScrollUp)", [0x31, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=ScrollDown)", [0x32, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=scrollup)", [0x31, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=scrolldown)", [0x32, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=scrolldwn)", [0x32, 0x00, 0x00, 0x02, 0x00, 0x00]),
            ("buttons(button1=scrollDn)", [0x32, 0x00, 0x00, 0x02, 0x00, 0x00]),
        ],
    )
    def test_string_values_scroll(self, setting_info1, value, expected):
        bytes_ = buttons.process_value(setting_info1, value)
        assert bytes_ == expected

    def test_string_value_dpi(self, setting_info1):
        bytes_ = buttons.process_value(setting_info1, "buttons(button1=dpi)")
        # fmt: off
        assert bytes_ == [
            0x30, 0x00, 0x00,
            0x02, 0x00, 0x00,
        ]
        # fmt: on

    @pytest.mark.parametrize(
        "value",
        [
            "buttons(button1=disable)",
            "buttons(button1=disabled)",
        ],
    )
    def test_string_value_disable(self, setting_info1, value):
        bytes_ = buttons.process_value(setting_info1, value)
        # fmt: off
        assert bytes_ == [
            0x00, 0x00, 0x00,
            0x02, 0x00, 0x00,
        ]
        # fmt: on

    def test_dict_values(self, setting_info2):
        bytes_ = buttons.process_value(
            setting_info2,
            {
                "buttons": {
                    "button1": "button4",
                    "button2": "PlayPause",
                    "button3": "Enter",
                    "button4": "dpi",
                }
            },
        )
        # fmt: off
        assert bytes_ == [
            0x04, 0x00, 0x00,
            0x61, 0xCD, 0x00,
            0x51, 0x28, 0x00,
            0x30, 0x00, 0x00,
        ]
        # fmt: on

    @pytest.mark.parametrize(
        "value",
        [
            "buttons(layout=QWERTY)",
            "buttons(Layout=qwerty)",
            "buttons(button1=default)",
            "buttons(Button1=Default)",
            "buttons(button1=button1)",
            "default",
            {"buttons": {}},
        ],
    )
    def test_default_values(self, setting_info2, value):
        bytes_ = buttons.process_value(setting_info2, value)
        # fmt: off
        assert bytes_ == [
            0x01, 0x00, 0x00,
            0x02, 0x00, 0x00,
            0x61, 0xB5, 0x00,
            0x30, 0x00, 0x00,
        ]
        # fmt: on


class TestAddCliOption(object):
    @pytest.fixture
    def cli(self):
        cli = argparse.ArgumentParser()
        buttons.add_cli_option(
            cli,
            "buttons0",
            {
                "label": "Buttons mapping",
                "description": "Set the mapping of the buttons",
                "cli": ["-b", "--buttons", "--foobar"],
                "command": [0x31, 0x00],
                "value_type": "buttons",
                "buttons": {
                    "Button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                    "Button2": {"id": 0x02, "offset": 0x03, "default": "button2"},
                    "Button3": {"id": 0x03, "offset": 0x06, "default": "button3"},
                    "Button4": {"id": 0x04, "offset": 0x09, "default": "button4"},
                    "Button5": {"id": 0x05, "offset": 0x0C, "default": "button5"},
                    "Button6": {"id": 0x06, "offset": 0x0F, "default": "dpi"},
                },
                "button_disable": 0x00,
                "button_keyboard": 0x51,
                "button_multimedia": 0x61,
                "button_dpi_switch": 0x30,
                "button_scroll_up": 0x31,
                "button_scroll_down": 0x32,
                "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; layout=qwerty)",
            },
        )
        return cli

    def test_cli_options(self, cli):
        assert "-b" in cli.format_help()
        assert "--buttons" in cli.format_help()
        assert "--foobar" in cli.format_help()

    def test_cli_metavar(self, cli):
        assert "-b BUTTONS0" in cli.format_help()

    def test_default_value_displayed(self, cli):
        assert "buttons(" in cli.format_help()

    @pytest.mark.parametrize(
        "buttons",
        [
            "default",
            "buttons(layout=qwerty; button1=button1)",
        ],
    )
    def test_passing_valid_color_arguments(self, cli, buttons):
        params = cli.parse_args(["--buttons", buttons])
        assert params.BUTTONS0 == buttons

    @pytest.mark.parametrize(
        "buttons",
        [
            "hello",
            "buttons()",
            "buttons(button15=A)",
        ],
    )
    def test_passing_invalid_color_arguments(self, cli, buttons):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parse_args(["--buttons", buttons])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
