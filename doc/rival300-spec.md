# SteelSeries Rival 300 gaming mouse's USB HID commands

This mouse is expected to be the same as the Original Rival.


## Devices infos

    USB class: HID
    VendorID: 1038
    ProductID: 1710
    HIDRAW interface no: 0


## Commands

| Name              | Command  | Parameters                      | Descriptions                                   |
|-------------------|----------|---------------------------------|------------------------------------------------|
| set_sensitivity   | `0x03`   | `<preset> <value>`              | Set the sensitivity of the sensor              |
| set_polling_rate  | `0x04`   | `0x00 <rate>`                   | Set the polling rate                           |
| set_light_effect  | `0x07`   | `<led_id> <effect>`             | Set the light effect (static, breath,...)      |
| set_color         | `0x08`   | `<led_id> <red> <green> <blue>` | Set the wheel and logo backlight's             |
| save              | `0x09`   | -                               | Save the configuration to the mouse's memory   |

### set_sensitivity

The mouse can store two sensitivity presets (you can switch between them using
the button under the wheel).

    0x03 <preset> <value>

Params:

* `preset`: preset number:
  * `0x01`: first preset
  * `0x02`: second preset
* `value`: sensitivity (from 50 to 6500 with increment of 50)
  * `value = sensitivity / 50`
  * default value for first preset is 800 DPI (`value = 16`)
  * default value for second preset is 1600 DPI (`value = 32`)

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

### set_light_effect

Defines the effect applied on the lights?

    0x07 <led_id> <effect>

Params:

* `led_id`: the led on which to set the effect:
  * `0x01`: Le logo's led
  * `0x02`: Le wheel's led
* `effect`: the light effect:
  * `0x01`: static
  * `0x02`: pulsate (slow)
  * `0x03`: pulsate (called breath in the SteelSeries tool)
  * `0x04`: pulsate (quick)

### set_color

Set the mouse backlight color.

    0x08 <led_id> <red> <green> <blue>

Params:

* `led_id`: the led on which to set the color:
  * `0x01`: Le logo's led
  * `0x02`: Le wheel's led
* `red`: red channel of the RGB color (from `0x00` to `0xFF`)
* `green`: green channel of the RGB color (from `0x00` to `0xFF`)
* `blue`: blue channel of the RGB color (from `0x00` to `0xFF`)

### save

Save the current config to the mouse's internal memory.

    0x09

