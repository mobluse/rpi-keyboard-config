# RPi Keyboard Config with Flappy Bird Game for Raspberry Pi 500 w/o +

## Installation and Run of Game

```bash
git clone https://github.com/mobluse/rpi-keyboard-config
cd rpi-keyboard-config/src
python -m RPiKeyboardConfig.game
rpi-keyboard-config lock
```
On a Raspberry Pi 500 with updated keyboard firmware it will show the game animation in the terminal using VT100/ANSI escape codes.
I have not tested this with a Raspberry Pi 500+, but its code was not changed intentionally. 

## Original Introduction

A Python library and command-line tool for configuring Raspberry Pi keyboards, including keymap customisation and RGB LED control.

## Supported Keyboards

- **Raspberry Pi 500** (USB VID: 2e8a, PID: 0010)
- **Raspberry Pi 500+** (USB VID: 2e8a, PID: 0011)

## Features

- **Keymap Configuration**: Set custom keycodes for any key position
- **RGB LED Control**: Control individual LEDs
- **Effects**: Built-in lighting effects (solid, gradient, pinwheel, heatmap, reactive, etc.)
- **Presets**: Change the preset effects that can be cycled through by pressing Fn+F4
- **Key Monitoring**: Watch for key presses
- **Demos**: Flappy Bird game and LED random test pattern

## Installation

```bash
sudo apt install rpi-keyboard-config
```

The Debian package automatically installs udev rules.

### Keyboard Firmware

The keyboard must have the latest firmware to be compatible. Use <https://github.com/raspberrypi/keyboard-firmware> to update the firmware:

```bash
sudo rpi-keyboard-fw-update
```

## Command Line Usage

### Basic Information

```bash
# Show keyboard information
rpi-keyboard-config info

# Show keyboard information with ASCII art layout
rpi-keyboard-config info --ascii

# Get firmware version only
rpi-keyboard-config get-version
```

### Keymap Configuration

Key mappings can be dynamically changed using `rpi-keyboard-config key` or <https://vial.rocks/>.

```bash
# Get keycode for a specific key position
rpi-keyboard-config key get <row> <col> [--layer <layer>]

# Set keycode for a specific key position
rpi-keyboard-config key set <row> <col> <keycode> [--layer <layer>]

# List keycodes for all keys
rpi-keyboard-config key get-all [--layer <layer>]

# Examples
rpi-keyboard-config key get 2 3              # Get key at row 2, col 3
rpi-keyboard-config key set 2 3 KC_A         # Set key to 'A'
rpi-keyboard-config key get-all              # List all keys and their keycodes

# Reset keymap to defaults
rpi-keyboard-config reset-keymap
```

### Keyboard Lock/Unlock

Only required for a handful of operations e.g. key monitoring. See <https://get.vial.today/docs/security.html> for more details.

```bash
# Unlock keyboard
rpi-keyboard-config unlock

# Lock keyboard
rpi-keyboard-config lock
```

### Key Monitoring

Note: Key monitoring requires the keyboard to be unlocked first.

```bash
# Watch for key presses and show details
rpi-keyboard-config key watch [--layer <layer>] [--no-leds] [--exit-key <key>]

# Examples
rpi-keyboard-config key watch                   # Watch with LED feedback (Pi 500+ only)
rpi-keyboard-config key watch --no-leds         # Watch without LED feedback
```

### LED Control (Raspberry Pi 500+ only)

### Global Hue and Brightness Control

The default keys on the Pi 500+ to increase and decrease the global hue are Fn+F3 and Fn+Shift+F3 respectively.
The default keys on the Pi 500+ to increase and decrease the global brightness are Fn+F6 and Fn+F5 respectively.

```bash
# Get current global hue
rpi-keyboard-config hue

# Set global hue (affects compatible effects)
rpi-keyboard-config hue <0-255>

# Example
rpi-keyboard-config hue 85      # Set to green hue

# Get current global brightness
rpi-keyboard-config brightness

# Set global brightness
rpi-keyboard-config brightness <0-255>

# Example
rpi-keyboard-config brightness 255     # Set to maximum brightness
```

### RGB Effects

A selection of effects to control the RGB are available. The tool allows you to show an effect on the keyboard temporarily (until the keyboard shuts down, the Fn+F4 key is pressed or something triggers a new effect). A preset on the keyboard can also be set, which is an effect at a given preset index. Pressing Fn+F4 will cycle through the presets and the previously selected preset will be restored after reboot.
Temporary effects are stored at preset index 7 which cannot be cycled through.

```bash
# Show current effect
rpi-keyboard-config effect

# Set effect with parameters
rpi-keyboard-config effect <effect> [--hue <0-255>] [--sat <0-255>] [--speed <0-255>]
# Adding --hue will fix the hue at the specified value, otherwise the effect will use the global hue value

# Show available RGB effects
rpi-keyboard-config list-effects

# Examples
rpi-keyboard-config effect "Solid Color" --hue 0 --sat 255           # Solid red (fixed hue)
rpi-keyboard-config effect "Cycle Pinwheel" --speed 200     # Fast pinwheel
rpi-keyboard-config effect "Typing Heatmap"                  # Heat map effect
```

Note: The value component of HSV cannot be set, this is controlled by the brightness of the keyboard. Some effects may ignore the set hue and saturation.

### RGB Presets

Presets can be cycled through by default by pressing Fn+F4. The previously shown preset will be restored on reboot.

```bash
# Get current preset index
rpi-keyboard-config preset index

# Set preset index
rpi-keyboard-config preset index <0-7>

# Get preset configuration
rpi-keyboard-config preset get [index]               # If no index, shows all presets
rpi-keyboard-config preset get 2                     # Show preset 2 configuration

# Set preset configuration
rpi-keyboard-config preset set <index> [effect] [--hue <0-255>] [--sat <0-255>] [--speed <0-255>] [--startup-animation <animation>]

# Revert to saved preset index (useful after setting a temporary effect)
rpi-keyboard-config preset revert

# Examples
rpi-keyboard-config preset set 0 "Solid Color" --hue 0 --sat 255     # Set preset 0 to solid red
rpi-keyboard-config preset set 3 "Cycle Pinwheel" --speed 150        # Set preset 3 to medium-speed pinwheel
rpi-keyboard-config preset set 2 --hue 85 --sat 255                  # Change preset 2 hue to green, keep current effect
rpi-keyboard-config preset index 2                                   # Switch to preset 2

# Only cycle through the first 3 presets before looping back to the start
rpi-keyboard-config preset set 3 skip

# Set the startup animation
rpi-keyboard-config preset set 0 "Solid Color" --startup-animation "START_ANIM_W_FADE_SAT"
```

#### Startup animation options

| Animation Name             | Description                                 |
|---------------------------|---------------------------------------------|
| START_ANIM_NONE           | No startup animation                        |
| START_ANIM_B_NO_FADE      | Show the startup animation finishing with blank LEDs then go straight to the preset |
| START_ANIM_B_FADE_VAL     | START_ANIM_B_NO_FADE but fade in the preset with increasing brightness          |
| START_ANIM_W_NO_FADE      | Show the startup animation finishing with all the LEDs white then go straight to the preset |
| START_ANIM_W_FADE_SAT     | START_ANIM_W_NO_FADE but fade in with increasing saturation          |

#### LED Operations

If the currently shown preset is not the direct led effect then the keyboard will be set to a temporary direct led effect.

```bash
# Clear all LEDs
rpi-keyboard-config leds clear

# Set all LEDs to a colour (HSV format by default)
rpi-keyboard-config leds set --colour red
rpi-keyboard-config leds set --colour "128,255,255"     # HSV values
rpi-keyboard-config leds set --colour "#FF0000"         # RGB hex
rpi-keyboard-config leds set --colour "rgb(255,0,0)"    # RGB values

# Get current LED states
rpi-keyboard-config leds get

# Get saved LED states from EEPROM
rpi-keyboard-config leds get-saved

# Save current LED configuration to EEPROM
rpi-keyboard-config leds save

# Load saved LED configuration from EEPROM
rpi-keyboard-config leds load
```

#### Individual LED Control

```bash
# Set individual LED by index
rpi-keyboard-config led set <index> --colour <colour>

# Set LED by matrix position
rpi-keyboard-config led set <row>,<col> --colour <colour>

# Examples
rpi-keyboard-config led set 5 --colour blue        # Set LED index 5 to blue
rpi-keyboard-config led set 2,3 --colour green     # Set LED at matrix [2,3] to green
rpi-keyboard-config led set 10 --colour "170,255,255"  # Set LED 10 to cyan (HSV)
```

### Reset Operations

```bash
# Reset RGB presets and direct LEDs
rpi-keyboard-config reset-presets

# Reset keymap to defaults
rpi-keyboard-config reset-keymap
```

### Colour Formats

Colours can be specified in several formats:

- **Named colours**: `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `white`, `orange`, `purple`, `pink`
- **HSV values** (default): `128,255,255` (hue, saturation, value)
- **RGB Hex colours**: `#FF0000`
- **RGB values** (explicit): `rgb(255,0,0)` - must use `rgb()` prefix

### QMK Keycode Listing

```bash
# List all keycodes
rpi-keyboard-config list-keycodes

# Filter by category
rpi-keyboard-config list-keycodes --category basic      # Letters, numbers, basic symbols
rpi-keyboard-config list-keycodes --category modifiers  # Ctrl, Shift, Alt, etc.

# Search by name (case-insensitive)
rpi-keyboard-config list-keycodes --filter "slash"
```

### Games and Demos

```bash
# Play Flappy Bird game on the keyboard LEDs (Pi 500+ only)
rpi-keyboard-config game

# Run random LED test pattern (Pi 500+ only)
rpi-keyboard-config random-leds
```

## Python Library Usage

### Basic Setup

```python
from RPiKeyboardConfig import RPiKeyboardConfig

# Initialise the keyboard
keyboard = RPiKeyboardConfig()
```

### Keyboard Information

```python
# Get keyboard model and info
print(f"Model: {keyboard.model}")           # "PI500" or "PI500PLUS"
print(f"Variant: {keyboard.variant}")       # "ISO", "ANSI", or "JIS"

# Get firmware version
version = keyboard.get_firmware_version()
print(f"Firmware: {version[0]}.{version[1]}.{version[2]}")

# Get ASCII art of current keyboard layout
ascii_map = keyboard.get_ascii_keycode_map(layer=0)
print(ascii_map)
```

### Keymap Configuration

```python
# Get keycode for a key
keycode = keyboard.get_keycode(matrix=[2, 3], layer=0)
print(f"Key at [2,3] has keycode: {keycode}")

# Set keycode for a key
keyboard.set_keycode(matrix=[2, 3], layer=0, keycode=4)  # Set to 'A'

# Get keycodes for all keys
all_keynames = keyboard.get_all_keynames(layer=0)
for data in all_keynames:
    pos = data['position']
    print(f"Key at row {pos[0]:2d}, col {pos[1]:2d}: Keycode {data['keycode']:5d} -> {data['name']}")

# Reset keymap to defaults
keyboard.reset_keymap()
```

### Key Monitoring and Unlock

```python
# Check if keyboard needs unlocking
unlocked, unlock_in_progress, unlock_keys = keyboard.get_unlock_status()
if not unlocked:
    print("Unlocking keyboard...")
    keyboard.unlock()

# Get switch matrix state (currently pressed keys) - requires unlock
if unlocked:
    active_keys = keyboard.get_switch_matrix_state()
    print(f"Currently pressed keys: {active_keys}")

# Lock the keyboard
keyboard.lock()
```

### LED Control (Raspberry Pi 500+ only)

#### Basic LED Operations

```python
# Set LED direct control mode
keyboard.set_led_direct_effect()

# Set individual LED by index (HSV format: hue, saturation, value)
keyboard.set_led_by_idx(idx=5, colour=(0, 255, 255))      # Red
keyboard.set_led_by_idx(idx=6, colour=(85, 255, 255))     # Green
keyboard.set_led_by_idx(idx=7, colour=(170, 255, 255))    # Cyan

# Set LED by matrix position
keyboard.set_led_by_matrix(matrix=[2, 3], colour=(42, 255, 255))  # Orange

# Send LED updates to keyboard (required after setting colours)
keyboard.send_leds()

# Clear all LEDs
keyboard.rgb_clear()
```

#### Advanced LED Operations

```python
# Get current LED states
current_leds = keyboard.get_current_direct_leds()
for i, (h, s, v) in enumerate(current_leds):
    print(f"LED {i}: HSV({h}, {s}, {v})")

# Get individual LED info
led_info = keyboard.get_led_info(idx=5)
print(f"LED 5: {led_info}")

# Get all LED configurations
all_leds = keyboard.get_leds()
for led in all_leds:
    print(f"LED {led.idx}: matrix={led.matrix}, colour={led.colour}")

# Save current LED configuration to EEPROM
keyboard.save_direct_leds()

# Load saved LED configuration from EEPROM
keyboard.load_direct_leds()

# Get saved LED configurations
saved_leds = keyboard.get_saved_direct_leds()
```

### Global Hue and Brightness Control

```python
# Get current global hue
current_hue = keyboard.get_hue()
print(f"Current hue: {current_hue}")

# Set global hue (affects compatible effects)
keyboard.set_hue(85)  # Set to green hue

# Get current global brightness
current_brightness = keyboard.get_brightness()
print(f"Current brightness: {current_brightness}")

# Set global brightness
keyboard.set_brightness(128)  # Set to medium brightness
```

### RGB Effects and Presets

```python
# Get supported effects
effects = keyboard.get_supported_effects()
print(f"Supported effects: {effects}")

# Get current effect
current_effect = keyboard.get_current_effect()
print(f"Current effect: {current_effect}")

# Create and set a preset
from RPiKeyboardConfig.keyboard import Preset
from RPiKeyboardConfig.effects import get_vial_effect_id

# Create a solid red preset
solid_effect_id = get_vial_effect_id("solid color")
red_preset = Preset(
    effect=solid_effect_id,
    speed=128,
    hue=0,        # Red hue
    sat=255,      # Full saturation
    val=255,      # Full brightness
    fixed_hue=True,
    startup_animation="START_ANIM_B_FADE_VAL"
)

# Set preset at index 0
keyboard.set_preset(0, red_preset)

# Switch to preset
keyboard.set_current_preset_index(0, save_index=True)

# Get preset configuration
preset = keyboard.get_preset(0)
print(f"Preset 0: {preset}")

# Revert to saved preset
keyboard.revert_to_saved_preset()

# Reset all presets and direct LEDs
keyboard.reset_presets_and_direct_leds()
```

## QMK Keycode Reference

The library supports standard QMK keycodes. Use `rpi-keyboard-config list-keycodes` to see all available keycodes, or visit the [QMK documentation](https://docs.qmk.fm/#/keycodes) for complete reference.
