import pytest

from rivalcfg.__main__ import main


class TestMainCLI(object):
    def test_print_help(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(["--help"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(["-h"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_print_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(["--version"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_print_list(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(["--list"])
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_no_save(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_DRY", "1")
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        main(["--reset"])
        main(["-r"])
        # just expecting to have no error here... to boring to monkeypatch
        # the module to check if realy work...
