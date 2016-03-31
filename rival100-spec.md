# SteelSeries Rival 100 gaming mouse's USB HID protocol spec

Translated from http://blog.flozz.fr/2016-03-27/steelseries-rival-100-reverse-engineering-peripherique-usb/


## Devices infos

    USB class: HID
    VendorID: 1038
    ProductID: 1702


## Commands

| Name              | Command  | Parameters                  | Descriptions                                   |
|-------------------|----------|-----------------------------|------------------------------------------------|
| set_sensitivity   | `0x03`   | `<preset> <value>`          | Set the sensitivity of the sensor              |
| set_polling_rate  | `0x04`   | `0x00 <rate>`               | Set the polling rate                           |
| set_color         | `0x05`   | `0x00 <red> <green> <blue>` | Set the mouse backlight's color                |
| set_light_effect  | `0x07`   | `0x00 <effect>`             | Set the light effect (static, breath,...)      |
| save              | `0x09`   | -                           | Save the configuration to the mouse's memory   |
| set_btn6_action   | `0x0B`   | `<action>`                  | Set the action of button under the wheel       |
| ???               | `0x16`   | ???                         | Sent when the mouse is plugged. Unknown effect |

### set_sensitivity

    0x03 <preset> <value>

Params:

* `preset`: preset number:
  * `0x01`: first preset
  * `0x02`: second
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

    0x04 0x00 <rate>

Params:

* `0x00`: reserved (must be set to `0x00`)
* `rate`: the polling rate:
   * `0x04`: 125 Hz (8 ms)
   * `0x03`: 250 Hz (4 ms)
   * `0x02`: 500 Hz (2 ms)
   * `0x01`: 1000 Hz (1 ms, default)

### set_color

    0x05 0x00 <red> <green> <blue>

Params:

* `0x00`: reserved (must be set to `0x00`)
* `red`: red channel of the RGB color (from `0x00` to `0xFF`)
* `green`: green channel of the RGB color (from `0x00` to `0xFF`)
* `blue`: blue channel of the RGB color (from `0x00` to `0xFF`)

### set_light_effect

    0x07 0x00 <effect>

Params:

* `0x00`: reserved (must be set to `0x00`)
* `effect`: the light effect:
  * `0x01`: static
  * `0x02`: pulsate (slow)
  * `0x03`: pulsate (called breath in the SteelSeries tool)
  * `0x04`: pulsate (quick)

### save

Save the current config to the mouse's internal memory.

    0x09

### set_btn6_action

    0x0B <action>

Params:

* `action`: button's action:
  * `0x00`: toggle sensitivity presets
  * `0x01`: allows the OS to handle the button (detected as "button 10" by `xev`)

