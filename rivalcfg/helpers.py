import re

import pyudev


NAMED_COLORS = {
      "white": (0x00, 0x00, 0x00),
     "silver": (0xC0, 0xC0, 0xC0),
       "gray": (0x80, 0x80, 0x80),
      "black": (0x00, 0x00, 0x00),
        "red": (0xFF, 0x00, 0x00),
     "maroon": (0x80, 0x00, 0x00),
     "yellow": (0xFF, 0xFF, 0x00),
      "olive": (0x80, 0x80, 0x00),
       "lime": (0x00, 0xFF, 0x00),
      "green": (0x00, 0x80, 0x00),
       "aqua": (0x00, 0xFF, 0xFF),
       "teal": (0x00, 0x80, 0x80),
       "blue": (0x00, 0x00, 0xFF),
       "navy": (0x00, 0x00, 0x80),
    "fuchsia": (0xFF, 0x00, 0xFF),
     "purple": (0x80, 0x00, 0x80),

    # Rival 300 CS:GO Fade Edition presets
    "preset1": (0xFF, 0x52, 0x00),
    "preset2": (0x1D, 0xC5, 0xFF),
    "preset3": (0x64, 0x03, 0xFC),
    "preset4": (0xFF, 0xF2, 0x00),
    "preset5": (0xFF, 0x00, 0x00),
}
#Button support for Heroes of the Storm (Sensei Raw)
NAMED_KEYS = {
    "lctrl": [0x10,0xE0,0x00],
    "lshift": [0x10, 0xE1,0x00],
    "lalt": [0x10,0xE2,0x00],
    "lcmd": [0x10,0xE3,0x00],
    "rctrl": [0x10,0xE4,0x00],
    "rshift": [0x10,0xE5,0x00],
    "ralt": [0x10,0xE6,0x00],
    "rcmd": [0x10,0xE7,0x00],
    "pgdn": [0x10,0x4B,0x00],
    "pgup": [0x10,0x4E,0x00],
    #home and end in b/w pageup and down i.e. 4C, 4D ; don't remember the order.
    "senst": [0x30,0x00,0x00],
    "mouse1": [0x01,0x00,0x00],
    "mouse2": [0x02,0x00,0x00],
    "mouse3": [0x03,0x00,0x00],
    "mouse4": [0x04,0x00,0x00],
    "mouse5": [0x05,0x00,0x00],
    "mouse6": [0x06,0x00,0x00],
    "mouse7": [0x07,0x00,0x00],
    "mouse8": [0x08,0x00,0x00],  
}

def usb_device_is_connected(vendor_id, product_id):
    """Checks if the given device is connected to the USB bus.

    Arguments:
    vendor_id -- the vendor id of the device
    product_id -- the product id of the device
    """
    ctx = pyudev.Context()
    devices = ctx.list_devices(ID_VENDOR_ID=vendor_id)

    for device in devices:
        if (device["ID_MODEL_ID"] == product_id):
            return True
    return False


def find_hidraw_device_path(vendor_id, product_id, interface_num=0):
    """
    Find the first HID interface for the given USB vendor id and product id.

    Arguments:
    vendor_id -- the vendor id of the device
    product_id -- the product id of the device
    interface_num -- the interface number (default: 0)
    """
    ctx = pyudev.Context()
    devices = ctx.list_devices(ID_VENDOR_ID=vendor_id)

    for device in devices:
        if (device["ID_MODEL_ID"] != product_id):
            continue
        if (device["SUBSYSTEM"] != "hidraw"):
            continue
        if int(device["ID_USB_INTERFACE_NUM"]) != interface_num:
            continue

        return device["DEVNAME"]

    # Old Kernels...
    devices = ctx.list_devices(SUBSYSTEM="hidraw")
    deviceMatcher = re.compile(r"^.*/usb[0-9]+/[0-9/.-]+:[0-9]+\.%i/[0-9]+:%s:%s.*$" % (
        interface_num,
        vendor_id.upper(),
        product_id.upper()
        ))
    for device in devices:
        if not deviceMatcher.match(device["DEVPATH"]):
            continue

        return device["DEVNAME"]



def is_color(string):
    """Checks if the given string is a valid color.

    Arguments:
    string -- the string to check
    """
    return string in NAMED_COLORS or bool(re.match(r"^#?[0-9a-f]{3}([0-9a-f]{3})?$", string, re.IGNORECASE))


def color_string_to_rgb(color_string):
    """Converts the color string into an RGB tuple.

    Arguments:
    color_string -- the string to converts

    Returns:
    an (R, G, B) tuple
    """
    # Named color
    if color_string in NAMED_COLORS:
        return NAMED_COLORS[color_string]
    # #f00 or #ff0000 -> f00 or ff0000
    if color_string.startswith("#"):
        color_string = color_string[1:]
    # f00 -> ff0000
    if len(color_string) == 3:
        color_string = color_string[0] * 2 + color_string[1] * 2 + color_string[2] * 2
    # ff0000 -> (255, 0, 0)
    return (
        int(color_string[0:2], 16),
        int(color_string[2:4], 16),
        int(color_string[4:], 16)
        )


def keymap_to_string(kstring):
    """Converts a sequence of keymaps to a list of keymap settings for each button.
    Returns a list of strings
    """
    kstring=kstring.split()
    outlist = []
 
    #the list of commands to be outputted
    if not len(kstring) == 8:
        raise ValueError("Invalid length of argument to Set Button Commands!")
    for x in range(0, 8):
        #kstring[0] = kstring[0][1:] #First char of first string is '=' for some reason 
        dd = kstring[x].lower()
        if dd in NAMED_KEYS:
            outlist.append(NAMED_KEYS[kstring[x]])
            
            continue
        if len(dd) == 1 and 0 <= ord(dd)-ord('a') <= 25:
            outlist.append([0x10, ord(dd)-ord('a')+4, 0x00])
                     
            continue
        if len(dd) == 1 and 0 <= ord(dd)-ord('0') <= 9:
            if(dd=='0'):
                outlist.append([0x10, 0x27, 0x00])
                
            else:
                outlist.append([0x10,ord(dd)-ord('1')+0x1E, 0x00])
                    
            continue

        raise ValueError("Invalid entry key name: %s" % dd) 
    
    return outlist #It is a list of lists.
#keymap_to_string ends

def choices_to_list(choices):
    """Transforms choices dict to an ordered string list.

    Arguments:
    choices -- the dict containing available choices
    """
    return list(map(str, sorted(choices.keys(), key=lambda v: v if type(v) == int else -1)))


def choices_to_string(choices):
    """Transforms choices dict to a printable string.

    Arguments:
    choices -- the dict containing available choices
    """
    return ", ".join(choices_to_list(choices))


def merge_bytes(*args):
    """Merge byte and list of byte into a single list of byte."""
    result = []
    for arg in args:
        if type(arg) in [list, tuple]:
            result.extend(arg)
        else:
            result.append(arg)
    return result

