import sys
from optparse import OptionParser

from helpers import find_hidraw_device_path
from rival100 import Rival100, VENDOR_ID, PRODUCT_ID


parser = OptionParser("Usage: rivalcfg [options]")

parser.add_option("-s", "--sensitivity1",
        help="Set sensitivity preset 1 (allowed values are 250, 500, 1000, 1250, 1500, 1750, 2000 and 4000; default value is 1000)",
        metavar="SENSITIVITY",
        choices=["250", "500", "1000", "1250", "1500", "1750", "2000", "4000"]
        )

parser.add_option("-S", "--sensitivity2",
        help="Set sensitivity preset 2 (allowed values are 250, 500, 1000, 1250, 1500, 1750, 2000 and 4000; default value is 2000)",
        metavar="SENSITIVITY",
        choices=["250", "500", "1000", "1250", "1500", "1750", "2000", "4000"]
        )

parser.add_option("-p", "--polling-rate",
        help="Set polling rate in Hz (allowed values are 125, 250, 500 and 1000; default value is 1000)",
        choices=["125", "250", "500", "1000"]
        )

parser.add_option("-c", "--color",
        help="Set the mouse backlight color (color can be an hexadecimal color or a nammed color; e.g. ff0000, f00, #ff0000, #f00, red,...)"
        )

parser.add_option("-e", "--light-effect",
        help="Set the light effect (allowed values are 1 or static, 2, 3 or breath, 4)",
        choices=["static", "breath", "1", "2", "3", "4"]
        )

parser.add_option("-b", "--btn6-action",
        help="Set the action of the button under the wheel (allowed values are default and os)",
        metavar="ACTION",
        choices=["default", "os", "0", "1"]
        )

parser.add_option("-r", "--reset",
        help="Reset all options to their default values",
        action="store_true"
        )

options, args = parser.parse_args();


device_path = find_hidraw_device_path(VENDOR_ID, PRODUCT_ID)

if not device_path:
    print("E: Unable to find any SteelSeries Rival 100 gaming mouse connected to the computer")
    sys.exit(1)

rival = Rival100(device_path)


if options.reset:
    rival.set_default()
    rival.save()
    sys.exit(0)


option_setted = False

if options.sensitivity1 != None:
    option_setted = True
    rival.set_sensitivity(1, int(options.sensitivity1))

if options.sensitivity2 != None:
    option_setted = True
    rival.set_sensitivity(2, int(options.sensitivity2))

if options.polling_rate != None:
    option_setted = True
    rival.set_polling_rate(int(polling_rate))

if options.color != None:
    option_setted = True
    try:
        rival.set_color(options.color)
    except ValueError:
        print("E: Invalid color")
        sys.exit(1)

if options.light_effect != None:
    option_setted = True
    effects = {
        "1": 0x01,
        "2": 0x02,
        "3": 0x03,
        "4": 0x04,
        "static": rival.EFFECT_STATIC,
        "breath": rival.EFFECT_BREATH,
    }
    rival.set_light_effect(effects[options.light_effect])

if options.btn6_action != None:
    option_setted = True
    actions = {
        "default": rival.BTN_ACTION_DEFAULT,
        "os": rival.BTN_ACTION_OS,
    }
    rival.set_btn6_action(actions[options.btn6_action])

if option_setted:
    rival.save()
else:
    print("E: No options provided")
    print("type `rivalcfg -h' to display the options")
    sys.exit(1)

