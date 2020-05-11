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
                20: 0xCC
                }
            }

    def test_valid_choice_int(self, setting_info):
        assert choice.process_value(setting_info, 10) == [0xBB]

    def test_valid_choice_str(self, setting_info):
        assert choice.process_value(setting_info, "foo") == [0xDD]

    def test_not_valid_choice(self, setting_info):
        with pytest.raises(ValueError):
            choice.process_value(setting_info, 42)
