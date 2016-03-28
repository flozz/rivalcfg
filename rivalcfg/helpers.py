import pyudev

def find_hidraw_device_path(vendor_id, product_id):
    """
    Find the first HID interface for the given USB vendor id and product id

    arguments:
    vendor_id -- the vendor id of the device
    product_id -- the product id of the device
    """
    ctx = pyudev.Context();
    devices = ctx.list_devices(ID_VENDOR_ID=vendor_id)

    for device in devices:
        if (device["ID_MODEL_ID"] != product_id):
            continue
        if (device["SUBSYSTEM"] != "hidraw"):
            continue

        return device["DEVNAME"]

