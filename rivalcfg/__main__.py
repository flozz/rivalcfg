import sys

from helpers import find_hidraw_device_path
from rival100 import Rival100, VENDOR_ID, PRODUCT_ID

device_path = find_hidraw_device_path(VENDOR_ID, PRODUCT_ID)

if not device_path:
    print("E: Unable to find any SteelSeries Rival 100 gaming mouse connected to the computer")
    sys.exit(1);

