# SteelSeries Heroes of the Storm (Sensei Raw) gaming mouse's USB HID commands

This mouse is expected to be the same as the Sensei Raw. 
Button Layout:

        `*Btn8` (Below the wheel (mouse3))
    
    `*Btn5` (Left Top)       `*Btn7` (Right Top) 
    
    `*Btn4` (Left Bottom)    `*Btn6` (Right Bottom)

## Devices infos

    USB class: HID
    VendorID: 1038
    ProductID: 1390
    HIDRAW interface no: 0


## Commands

| Name                  | Command    | Parameters                  | Descriptions                                                |
|-----------------------|------------|-----------------------------|-------------------------------------------------------------|
| set_sensitivity       | `0x03`     | `<preset> <value>`          | Set the sensitivity of the sensor                           |
| set_light_effect      | `0x07 0x01`| `<effect>`                  | Set the light effect (static, breath,...)                   |
| set_light_brightness  | `0x05 0x01`| `<effect>`                  | Set the light brightness (low, medium, high)                |
| set_mouse_btn_action  | `0x31``0x00`| `<8 3 Byte Values>`         | Configure what the mouse buttons do on press (all 8 at once)| 
| save                  | `0x09`     | -                           | Save the configuration to the mouse's memory                |

### set_sensitivity

The mouse can store two sensitivity presets (you can switch between them using
the button under the wheel (Mouse8)).

    0x03 <preset> <value>

Params:

* `preset`: preset number:
  * `0x01`: first preset
  * `0x02`: second preset
* `value`: sensitivity (from 90 to 5400 (Maybe 5670, but I have considered 5400) with increment of 90)
  * `value = sensitivity / 90`
  * default value for first preset is 1530 DPI (`value = 1560`)
  * default value for second preset is 1600 DPI (`value = 2520`)


### set_light_effect

Defines the effect applied on the lights

    0x07 <led_id> <effect>

Params:

* `led_id`: the led on which to set the effect:
  * `0x01`: The logo's led
* `effect`: the light effect:
  * `0x01`: static
  * `0x02`: pulsate (slow)
  * `0x03`: pulsate (called breath in the SteelSeries tool)
  * `0x04`: pulsate (quick)
  * `0x05`: trigger    

### set_light_brightness

Sets the brightness of the light

    0x05 <0x01> <effect>

Params:

* `led_id`: the led on which to set the effect:
  * `0x01`: The logo's led
* `effect`: the light effect:
  * `0x01`: off (DISABLE ILLUMINATION)
  * `0x02`: low
  * `0x03`: medium
  * `0x04`: high

### set_mouse_btn_action

Sets what each keypress does

    0x31 <0x00> <8 x 3 Byte Values, One for each button>

Params:
* Mouse 1 to Mouse 8 instructions are listed in serial order.
* Alphanumeric keys: a: `0x10` `0x04` `0x00`, b: `0x10` `0x05` `0x00`, so on ... till 1, 2, 3, .. 0 :`0x10` `0x27` `0x00`
* `0x10` stands for keyboard key

* Other special keys: 
```
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
    "senst": [0x30,0x00,0x00], #SENSITIVITY TOGGLER!
    "mouse1": [0x01,0x00,0x00],
    "mouse2": [0x02,0x00,0x00],
    "mouse3": [0x03,0x00,0x00],
    "mouse4": [0x04,0x00,0x00],
    "mouse5": [0x05,0x00,0x00],
    "mouse6": [0x06,0x00,0x00],
    "mouse7": [0x07,0x00,0x00],
    "mouse8": [0x08,0x00,0x00]
```
### save

Save the current config to the mouse's internal memory.

    0x09

