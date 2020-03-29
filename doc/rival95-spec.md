# SteelSeries Rival 95 gaming mouse's USB HID commands

Translated from http://blog.flozz.fr/2016-03-27/steelseries-rival-100-reverse-engineering-peripherique-usb/


## Devices infos

    USB class: HID
    VendorID: 1038
    ProductID: 1706
    HIDRAW interface no: 0

Similar to Rival 100 but without wheel led and logo light

## Commands

| Name              | Command  | Parameters                  | Descriptions                                   |
|-------------------|----------|-----------------------------|------------------------------------------------|
| set_sensitivity   | `0x03`   | `<preset> <value>`          | Set the sensitivity of the sensor              |
| set_polling_rate  | `0x04`   | `0x00 <rate>`               | Set the polling rate                           |
| save              | `0x09`   | -                           | Save the configuration to the mouse's memory   |
| set_btn6_action   | `0x0B`   | `<action>`                  | Set the action of button under the wheel       |

### set_sensitivity

The mouse can store two sensitivity presets (you can switch between them using
the button under the wheel).

    0x03 <preset> <value>

Params:

* `preset`: preset number:
  * `0x01`: first preset
  * `0x02`: second preset
* `value`: sensitivity:
  * `0x08`: 250 DPI
  * `0x07`: 500 DPI
  * `0x06`: 1000 DPI (default value of first preset)
  * `0x05`: 1250 DPI
  * `0x04`: 1500 DPI
  * `0x03`: 1750 DPI
  * `0x02`: 2000 DPI (default value of second preset)
  * `0x01`: 4000 DPI

### set_polling_rate

Defines the frequency at which the computer will poll the mouse for new
position. A low polling rate can makes the mouse laggy, a high one will use
more bandwidth on the USB bus and will use more CPU cycles.

    0x04 0x00 <rate>

Params:

* `0x00`: reserved (must be set to `0x00`)
* `rate`: the polling rate:
   * `0x04`: 125 Hz (8 ms)
   * `0x03`: 250 Hz (4 ms)
   * `0x02`: 500 Hz (2 ms)
   * `0x01`: 1000 Hz (1 ms, default)

### save

Save the current config to the mouse's internal memory.

    0x09

### set_btn6_action

    0x0B <action>

Params:

* `action`: button's action:
  * `0x00`: toggle sensitivity presets
  * `0x01`: allows the OS to handle the button (detected as "button 10" by `xev`)

