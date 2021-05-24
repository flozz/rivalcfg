from rivalcfg import devices


class TestListPluggedDevice(object):
    def test_debug_devices(self, monkeypatch):
        monkeypatch.setenv("RIVALCFG_PROFILE", "1038:1702")
        devices_list = list(devices.list_plugged_devices())
        debug_device_found = False
        for device in devices_list:
            if (
                device["vendor_id"] == 0x1038
                and device["product_id"] == 0x1702
                and device["name"] == "SteelSeries Rival 100"
            ):
                debug_device_found = True
        assert debug_device_found
