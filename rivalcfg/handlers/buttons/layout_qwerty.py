"""
This file contains the layout for QWERTY (en_US) keyboards.
"""

# fmt: off

#: The layout
layout = {

    # Alphanumeric

    "A": 0x04,
    "B": 0x05,
    "C": 0x06,
    "D": 0x07,
    "E": 0x08,
    "F": 0x09,
    "G": 0x0A,
    "H": 0x0B,
    "I": 0x0C,
    "J": 0x0D,
    "K": 0x0E,
    "L": 0x0F,
    "M": 0x10,
    "N": 0x11,
    "O": 0x12,
    "P": 0x13,
    "Q": 0x14,
    "R": 0x15,
    "S": 0x16,
    "T": 0x17,
    "U": 0x18,
    "V": 0x19,
    "W": 0x1A,
    "X": 0x1B,
    "Y": 0x1C,
    "Z": 0x1D,

    "1": 0x1E,
    "2": 0x1F,
    "3": 0x20,
    "4": 0x21,
    "5": 0x22,
    "6": 0x23,
    "7": 0x24,
    "8": 0x25,
    "9": 0x26,
    "0": 0x27,

    # Editing

    "Enter":     0x28,
    "Escape":    0x29,
    "BackSpace": 0x2A,
    "Tab":       0x2B,
    "Space":     0x2C,
    "Delete":    0x4C,

    # Symbols

    "-": 0x2D,
    "=": 0x2E,
    "[": 0x2F,
    "]": 0x30,
    "\\": 0x31,
    "#": 0x32,  # International!?
    ";": 0x33,
    "'": 0x34,
    "`": 0x35,
    ",": 0x36,
    ".": 0x37,
    "/": 0x38,
    "\\(inter)": 0x64,  # International!?

    # Typing Mode

    "CapsLock":    0x39,
    "ScrollLock":  0x47,
    "Insert":      0x49,
    "NumLock":     0x53,

    # Functions

    "F1":  0x3A,
    "F2":  0x3B,
    "F3":  0x3C,
    "F4":  0x3D,
    "F5":  0x3E,
    "F6":  0x3F,
    "F7":  0x40,
    "F8":  0x41,
    "F9":  0x42,
    "F10": 0x43,
    "F11": 0x44,
    "F12": 0x45,
    "F13": 0x68,
    "F14": 0x69,
    "F15": 0x6A,
    "F16": 0x6B,
    "F17": 0x6C,
    "F18": 0x6D,
    "F19": 0x6E,
    "F20": 0x6F,
    "F21": 0x70,
    "F22": 0x71,
    "F23": 0x72,
    "F24": 0x73,

    # Commands

    "PrintScreen": 0x46,
    "PauseBreak":  0x48,
    "ContextMenu": 0x65,

    # Navigation

    "Home":     0x4A,
    "PageUp":   0x4B,
    "End":      0x4D,
    "PageDown": 0x4E,

    # Arrows

    "Right": 0x4F,
    "Left":  0x50,
    "Down":  0x51,
    "Up":    0x52,

    # Numpad

    "Keypad/": 0x54,
    "Keypad*": 0x55,
    "Keypad-": 0x56,
    "Keypad+": 0x57,
    "KeypadEnter": 0x58,
    "Keypad1": 0x59,
    "Keypad2": 0x5A,
    "Keypad3": 0x5B,
    "Keypad4": 0x5C,
    "Keypad5": 0x5D,
    "Keypad6": 0x5E,
    "Keypad7": 0x5F,
    "Keypad8": 0x60,
    "Keypad9": 0x61,
    "Keypad0": 0x62,
    "Keypad.": 0x63,
    "Keypad,": 0x85,  # ??
    "Keypad=": 0x86,  # ??

    # Modifiers

    "LeftCtrl":   0xE0,
    "LeftShift":  0xE1,
    "LeftAlt":    0xE2,
    "LeftSuper":  0xE3,  # Command / Win logo
    "RightCtrl":  0xE4,
    "RightShift": 0xE5,
    "RightAlt":   0xE6,
    "RightSuper": 0xE7,  # Command / Win logo

}

#: Alias for some keys of the layout
aliases = {
    "esc": "Escape",
    "bksp": "BackSpace",
    "bkspace": "BackSpace",
    "del": "Delete",

    "dash": "-",
    "minus": "-",
    "equal": "=",
    "eq": "=",
    "leftbracket": "[",
    "rightbracket": "]",
    "backslash": "\\",
    "hash": "#",
    "semicolon": ";",
    "semi": ";",
    "quote": "'",
    "backtick": "`",
    "backquote": "`",
    "comma": ",",
    "dot": ".",
    "point": ".",
    "slash": "/",

    "capslck": "CapsLock",
    "capslk": "CapsLock",
    "cpslck": "CapsLock",
    "cpslk": "CapsLock",
    "scrolllck": "ScrollLock",
    "scrolllk": "ScrollLock",
    "scrllck": "ScrollLock",
    "scrllk": "ScrollLock",
    "scrlck": "ScrollLock",
    "scrlk": "ScrollLock",
    "ins": "Insert",
    "num": "NumLock",
    "numlck": "NumLock",
    "numlk": "NumLock",

    "prntscr": "PrintScreen",
    "prtscr": "PrintScreen",
    "prtsc": "PrintScreen",
    "psbrk": "PauseBreak",
    "psbr": "PauseBreak",
    "ctx": "ContextMenu",
    "menu": "ContextMenu",
    "ctxmenu": "ContextMenu",
    "ctxmn": "ContextMenu",

    "pgup": "PageUp",
    "pgdown": "PageDown",
    "pgdwn": "PageDown",
    "pgdn": "PageDown",

    "lctrl": "LeftCtrl",
    "lshift": "LeftShift",
    "lalt": "LeftAlt",
    "alt": "LeftAlt",
    "super": "LeftSuper",
    "lsuper": "LeftSuper",
    "windows": "LeftSuper",
    "leftwindows": "LeftSuper",
    "win": "LeftSuper",
    "lwin": "LeftSuper",
    "command": "LeftSuper",
    "leftcommand": "LeftSuper",
    "cmd": "LeftSuper",
    "lcmd": "LeftSuper",
    "rctrl": "RightCtrl",
    "rshift": "RightShift",
    "ralt": "RightAlt",
    "altgr": "RightAlt",
    "rsuper": "RightSuper",
    "rightwindows": "RightSuper",
    "rwin": "RightSuper",
    "rightcommand": "RightSuper",
    "rcmd": "RightSuper",
}

# fmt: on
