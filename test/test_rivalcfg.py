import rivalcfg


class TestListSupportedMice(object):

    def test_returns_the_supported_mice(self):
        assert len(list(rivalcfg.list_supported_mice())) > 0

    def test_returns_name_vendorid_productid_of_each_mouse(self):
        for mouse in rivalcfg.list_supported_mice():
            assert len(mouse) == 3
            assert mouse.name
            assert mouse.product_id
            assert mouse.vendor_id


class TestListAvailableMice(object):

    def test_not_available_mouse(self, monkeypatch):
        monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:0001")
        assert len(list(rivalcfg.list_available_mice())) == 0

    def test_debug_available_mouse(self, monkeypatch):
        monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1710")
        assert len(list(rivalcfg.list_available_mice())) > 0


class TestGetMouseProfile(object):

    def test_supported_mouse(self):
        assert rivalcfg.get_mouse_profile(0x1038, 0x1710)

    def test_unsupported_mouse(self):
        assert rivalcfg.get_mouse_profile(0x0000, 0x0000) is None


class TestGetMouse(object):

    def test_unsuported_mouse(self):
        assert not rivalcfg.get_mouse(0x1038, 0x0001)

    def test_supported_mouse(self, monkeypatch):
        monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
        monkeypatch.setattr("rivalcfg.debug.DRY", True)
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1710")
        assert rivalcfg.get_mouse(0x1038, 0x1710)


class TestGetFirstMouse(object):

    def test_unsuported_mouse(self, monkeypatch):
        monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
        monkeypatch.setattr("rivalcfg.debug.DRY", True)
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:0001")
        assert not rivalcfg.get_first_mouse()

    def test_supported_mouse(self, monkeypatch):
        monkeypatch.setattr("rivalcfg.debug.DEBUG", True)
        monkeypatch.setattr("rivalcfg.debug.DRY", True)
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1710")
        assert rivalcfg.get_first_mouse()
