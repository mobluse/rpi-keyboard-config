#!/usr/bin/env python3
"""Command-line interface for RPi Keyboard Config."""

import argparse
import re
import os
import sys
import time
from typing import Optional, Tuple

from .game import main as game_main
from .random_leds import main as random_leds_main
from .keycodes import qmk_key_to_keycode, qmk_keycode_to_key
from .keyboard import (
    RPiKeyboardConfig, Preset, get_vial_effect_id, 
    get_vial_effect_name
)


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB values (0-255) to HSV values (0-255).
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255) 
        b: Blue component (0-255)
        
    Returns:
        Tuple of (hue, saturation, value) where each is 0-255
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn
    if diff == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = diff / mx
    v = mx
    return int(h * 255 / 360), int(s * 255), int(v * 255)


def parse_colour(colour_str: str) -> Tuple[int, int, int]:
    """Parse colour string in various formats and return HSV tuple.
    
    Args:
        colour_str: Color specification as named colours (\"red\", \"blue\"),
                    HSV values (\"128,255,255\"), RGB hex values (\"#FF0000\"),
                    or rgb values (\"rgb(255,0,0)\")
                   
    Returns:
        Tuple of (hue, saturation, value) where each is 0-255
        
    Raises:
        ValueError: If colour_str format is invalid or unrecognized
    """
    colour_str = colour_str.strip().lower()
    # Named colours stored as HSV values (H,S,V) where each is 0-255
    named_colours = {
        'red': (0, 255, 255),        # Red in HSV
        'green': (85, 255, 255),     # Green in HSV  
        'blue': (170, 255, 255),     # Blue in HSV
        'white': (0, 0, 255),        # White in HSV
        'black': (0, 0, 0),          # Black in HSV
        'yellow': (43, 255, 255),    # Yellow in HSV
        'cyan': (128, 255, 255),     # Cyan in HSV
        'magenta': (213, 255, 255),  # Magenta in HSV
        'orange': (21, 255, 255),    # Orange in HSV
        'purple': (213, 127, 128),   # Purple in HSV
        'pink': (234, 76, 255),      # Pink in HSV
    }

    if colour_str in named_colours:
        return named_colours[colour_str]

    # Support RGB hex input (convert to HSV)
    if colour_str.startswith('#'):
        colour_str = colour_str[1:]
    if len(colour_str) == 6:
        try:
            r = int(colour_str[0:2], 16)
            g = int(colour_str[2:4], 16)
            b = int(colour_str[4:6], 16)
            return rgb_to_hsv(r, g, b)
        except ValueError:
            pass

    # Support comma-separated values - treat as HSV first, then RGB if specified
    if ',' in colour_str:
        try:
            parts = [int(x.strip()) for x in colour_str.split(',')]
            if len(parts) == 3:
                h, s, v = parts
                if all(0 <= x <= 255 for x in [h, s, v]):
                    return (h, s, v)  # Direct HSV input
        except ValueError:
            pass

    # Support RGB format if explicitly prefixed
    if colour_str.startswith('rgb(') and colour_str.endswith(')'):
        rgb_values = colour_str[4:-1]
        try:
            parts = [int(x.strip()) for x in rgb_values.split(',')]
            if len(parts) == 3:
                r, g, b = parts
                if all(0 <= x <= 255 for x in [r, g, b]):
                    return rgb_to_hsv(r, g, b)
        except ValueError:
            pass

    raise ValueError(
        f"Invalid colour format: {colour_str}. "
        f"Use named colours (\"red\", \"blue\"), HSV values (\"128,255,255\"), "
        f"RGB hex values (\"#FF0000\"), or rgb values (\"rgb(255,0,0)\")"
    )


VIALRGB_EFFECT_SKIP = get_vial_effect_id("VIALRGB_EFFECT_SKIP")
VIALRGB_EFFECT_OFF = get_vial_effect_id("VIALRGB_EFFECT_OFF")

def parse_preset_data(
    keyboard: RPiKeyboardConfig, 
    effect_str: str, 
    speed_str: str, 
    hue_str: Optional[str], 
    sat_str: str, 
    startup_animation_str: str
) -> 'Preset':
    """Parse and validate preset data to create a Preset object.
    
    Args:
        keyboard: The keyboard config instance
        effect_str: Effect name or ID as string
        speed_str: Effect speed as string (0-255)
        hue_str: Hue value as string (0-255) or None for auto
        sat_str: Saturation value as string (0-255)
        startup_animation_str: Startup animation name or ID
        
    Returns:
        Configured Preset object
        
    Raises:
        ValueError: If any parameter is invalid or effect not supported
    """
    if effect_str.isdigit():
        effect_id =  int(effect_str)
    else:
        effect_name = effect_str.strip().lower()
        effect_id = get_vial_effect_id(effect_name)
        if effect_id is None:
            raise ValueError(
                f"Invalid effect: '{effect_str}'. Use list-effects to see all available effects."
            )
    supported_effects = keyboard.get_supported_effects()
    if effect_id not in supported_effects:
        raise ValueError(
            f"Invalid effect: '{effect_str}'. Use list-effects to see all available effects."
        )

    try:
        speed = int(speed_str)
        if not 0 <= speed <= 255:
            raise ValueError(f"Invalid speed: '{speed_str}'")
    except ValueError:
        raise ValueError(f"Invalid speed: '{speed_str}'")
    
    
    if hue_str is None:
        fixed_hue = False
        hue = 0
    else:
        fixed_hue = True
        try:
            hue = int(hue_str)
            if not 0 <= hue <= 255:
                raise ValueError(f"Invalid hue: '{hue_str}'")
        except ValueError:
            raise ValueError(f"Invalid hue: '{hue_str}'")
    
    try:
        sat = int(sat_str)
        if not 0 <= sat <= 255:
            raise ValueError(f"Invalid saturation: '{sat_str}'")
    except ValueError:
        raise ValueError(f"Invalid saturation: '{sat_str}'")
    
    if startup_animation_str not in Preset.animation_option.keys():
        try:
            if int(startup_animation_str) in Preset.animation_option.values():
                startup_animation = int(startup_animation_str)
            else:
                raise ValueError(
                    f"Invalid startup animation: '{startup_animation_str}'"
                )
        except ValueError:
            raise ValueError(f"Invalid startup animation: '{startup_animation_str}'")
    else:
        startup_animation = Preset.animation_option[startup_animation_str]
    
    return Preset(effect=effect_id, speed=speed, hue=hue, sat=sat,
                  startup_animation=startup_animation, fixed_hue=fixed_hue)

def pretty_print_effect(preset: 'Preset') -> None:
    """Print only the effect components of a preset. 
    
    Args:
        preset: The Preset object representing the effect to display
    """
    if preset.effect == VIALRGB_EFFECT_SKIP:
        print("   This is a skip preset")
    else:
        print(f"  Effect: {get_vial_effect_name(preset.effect)} (ID {preset.effect})")
        
        if preset.effect != VIALRGB_EFFECT_OFF:
            print(f"  Speed: {preset.speed}")
            print(f"  Sat: {preset.sat}")
            if preset.fixed_hue:
                print(f"  Hue fixed at: {preset.hue}")
            else:
                print(f"  Hue not fixed")

def pretty_print_preset(preset: 'Preset') -> None:
    """Print a formatted display of a preset's configuration.
    
    Args:
        preset: The Preset object to display
    """
    animation_name = next(
            (name for name, code in Preset.animation_option.items()
            if code == preset.startup_animation), 
            f"Unknown ({preset.startup_animation})"
        )
    if preset.effect == VIALRGB_EFFECT_SKIP:
        print("   This is a skip preset")
    else:
        print(f"  Effect: {get_vial_effect_name(preset.effect)} (ID {preset.effect})")
        
        if preset.effect != VIALRGB_EFFECT_OFF:
            print(f"  Speed: {preset.speed}")
            print(f"  Sat: {preset.sat}")
            if preset.fixed_hue:
                print(f"  Hue fixed at: {preset.hue}")
            else:
                print(f"  Hue not fixed")
        
        print(f"  Startup Animation: {animation_name}")
        # print(f"  Flags: {'All' if preset.flags == Preset.LED_FLAG_ALL "
        #       f"else 'None' if preset.flags == Preset.LED_FLAG_NONE "
        #       f"else preset.flags}")

def parse_keycode(keycode_str: str) -> int:
    """Parse keycode string (QMK name or numeric value) and return keycode value.
    
    Args:
        keycode_str: Keycode as QMK name (KC_A, KC_ENTER), 
                    decimal number (65), or hex (0x41)
                    
    Returns:
        Integer keycode value for keyboard programming
        
    Raises:
        ValueError: If keycode_str is not a valid keycode format
    """
    try:
        return int(keycode_str)
    except ValueError:
        pass

    if keycode_str.lower().startswith('0x'):
        try:
            return int(keycode_str, 16)
        except ValueError:
            pass

    keycode_name = keycode_str.strip().upper()
    if not keycode_name.startswith('KC_') and not keycode_name.startswith('QK_'):
        test_name = f"KC_{keycode_name}"
        if test_name in qmk_key_to_keycode:
            return qmk_key_to_keycode[test_name]

    if keycode_name in qmk_key_to_keycode:
        return qmk_key_to_keycode[keycode_name]

    basic_examples = ['KC_A', 'KC_ENTER', 'KC_SPACE', 'KC_ESCAPE', 'KC_F1']
    raise ValueError(
        f"Invalid keycode: '{keycode_str}'. Use a numeric value, hex (0x1234), "
        f"or QMK keycode name like: {', '.join(basic_examples)}"
    )


def get_keycode_name(keycode_value: int) -> str:
    """Get QMK keycode name from numeric value.
    
    Args:
        keycode_value: Integer keycode value
        
    Returns:
        QMK keycode name (e.g. 'KC_A') or hex representation if unknown
    """
    return qmk_keycode_to_key.get(keycode_value, f"0x{keycode_value:04X}")


def list_keycodes(
    name_filter: Optional[str] = None, 
    category: Optional[str] = None
) -> None:
    """List available QMK keycodes with optional filtering.
    
    Args:
        name_filter: Optional substring to filter keycode names
        category: Optional category ('basic', 'modifiers', 'function', 
                 'system', 'media', 'mouse')
    """
    # Define categories for better organisation
    categories = {
        'basic': {
            'name': 'Basic Keys',
            'patterns': [
                'KC_[A-Z]$', 'KC_[0-9]$', 'KC_SPACE', 'KC_TAB', 'KC_ENTER', 
                'KC_ESCAPE', 'KC_BACKSPACE', 'KC_DELETE', 'KC_INSERT', 
                'KC_MINUS', 'KC_EQUAL', 'KC_LEFT_BRACKET', 'KC_RIGHT_BRACKET', 
                'KC_BACKSLASH', 'KC_SEMICOLON',
                         'KC_QUOTE', 'KC_GRAVE', 'KC_COMMA', 'KC_DOT', 'KC_SLASH']
        },
        'modifiers': {
            'name': 'Modifier Keys',
            'patterns': [
                'KC_LEFT_(CTRL|SHIFT|ALT|GUI)', 'KC_RIGHT_(CTRL|SHIFT|ALT|GUI)']
        },
        'function': {
            'name': 'Function Keys',
            'patterns': ['KC_F[0-9]+', 'KC_PRINT_SCREEN', 'KC_SCROLL_LOCK', 'KC_PAUSE']
        },
        'system': {
            'name': 'System & Navigation',
            'patterns': [
                'KC_(UP|DOWN|LEFT|RIGHT)', 'KC_(HOME|END|PAGE_UP|PAGE_DOWN)',
                         'KC_CAPS_LOCK', 'KC_NUM_LOCK', 'KC_SCROLL_LOCK']
        },
        'media': {
            'name': 'Media Keys',
            'patterns': ['KC_(AUDIO|MEDIA)', 'KC_(VOLUME|BRIGHTNESS)', 'KC_MUTE']
        }
    }

    # Get all keycodes
    all_keycodes = list(qmk_key_to_keycode.items())

    # Apply name filter
    if name_filter:
        filtered_keycodes = [(name, code) for name, code in all_keycodes
                             if name_filter.lower() in name.lower()]
    else:
        filtered_keycodes = all_keycodes

    # Apply category filter
    if category and category in categories:
        category_patterns = categories[category]['patterns']
        category_keycodes = []
        for name, code in filtered_keycodes:
            for pattern in category_patterns:
                if re.search(pattern, name):
                    category_keycodes.append((name, code))
                    break
        filtered_keycodes = category_keycodes

    # Sort keycodes by their numeric value (QMK ordering)
    filtered_keycodes.sort(key=lambda x: x[1])

    # Display results
    if category and category in categories:
        print(f"{categories[category]['name']}:")
    elif name_filter:
        print(f"QMK Keycodes matching '{name_filter}':")
    else:
        print("All Available QMK Keycodes:")

    print()
    if not filtered_keycodes:
        print("No keycodes found matching the specified criteria.")
        return

    # Display in columns for better readability
    max_name_len = max(len(name) for name, _ in filtered_keycodes)

    for name, code in filtered_keycodes:
        print(f"  {name:<{max_name_len}} = 0x{code:04X} ({code:5d})")

    print(f"\nTotal: {len(filtered_keycodes)} keycodes")
    if not category and not name_filter:
        print("\nUse --category to filter by type, or --filter to search by name.")
        print("Available categories: basic, modifiers, function, system, media, mouse")


def main() -> None:
    """Handle command-line interface operations.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Raspberry Pi Keyboard Config CLI"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    #########################################################
    # Commands for keyboard control
    #########################################################
    info_parser = subparsers.add_parser('info', help='Show keyboard information')
    info_parser.add_argument(
        '-a', '--ascii', action='store_true',
        help='Show keyboard ASCII art'
    )

    subparsers.add_parser('unlock', help='Unlock the keyboard')

    subparsers.add_parser('lock', help='Lock the keyboard')

    subparsers.add_parser('reset-keymap', help='Reset the keymap')

    subparsers.add_parser('reset-presets', help='Reset the presets and direct LEDs')

    subparsers.add_parser('get-version', help='Get the version of the keyboard')

    subparsers.add_parser('help', help='Show help message (same as -h)')


    #########################################################
    # Commands for all LEDs
    #########################################################
    leds_parser = subparsers.add_parser('leds', help='Commands for all LEDs')
    leds_subparsers = leds_parser.add_subparsers(
        dest='leds_command', help='LEDs operations'
    )
    leds_subparsers.add_parser('clear', help='Clear all LEDs')
    leds_set_parser = leds_subparsers.add_parser('set', help='Set all LEDs to a colour')
    leds_set_parser.add_argument(
        '-c', '--colour', '--color', default='red',
        help='colour in various formats: named (\"red\", \"blue\"), '
             'HSV values (\"128,255,255\"), RGB hex values (\"#FF0000\"), '
             'or rgb values (\"rgb(255,0,0)\"). Default: red'
    )
    leds_subparsers.add_parser('get', help='Get the current direct LEDs')
    leds_subparsers.add_parser(
        'get-saved', help='Get the saved direct LEDs from EEPROM'
    )
    leds_subparsers.add_parser('save', help='Save the current direct LEDs to EEPROM')
    leds_subparsers.add_parser('load', help='Load the saved direct LEDs from EEPROM')

    #########################################################
    # Commands for individual LED
    #########################################################
    led_parser = subparsers.add_parser('led', help='Commands for individual LEDs')
    led_subparsers = led_parser.add_subparsers(
        dest='led_command', help='LED operations'
    )
    led_set_parser = led_subparsers.add_parser('set', help='Set LED colour')
    led_set_parser.add_argument(
        'position',
        help='LED index (e.g. 5) or matrix position as row,col (e.g. 2,3)'
    )
    led_set_parser.add_argument(
        '-c', '--colour', '--color', default='red',
        help='colour in various formats: named (\"red\", \"blue\"), '
             'HSV values (\"128,255,255\"), RGB hex values (\"#FF0000\"), '
             'or rgb values (\"rgb(255,0,0)\"). Default: red'
    )


    #########################################################
    # Commands for Hue and Brightness of the keyboard
    #########################################################
    hue_parser = subparsers.add_parser('hue', help='Get or set the hue of the keyboard')
    hue_parser.add_argument(
        'hue', nargs='?', type=int, 
        help='Hue (0-255). If not provided, shows current hue.'
    )

    brightness_parser = subparsers.add_parser('brightness', help='Get or set the brightness of the keyboard')
    brightness_parser.add_argument(
        'brightness', nargs='?', type=int, 
        help='Brightness (0-255). If not provided, shows current brightness.'
    )


    #########################################################
    # Commands for RGB effects
    #########################################################
    effect_parser = subparsers.add_parser(
        'effect', help='Get current effect or set RGB effects'
    )
    effect_parser.add_argument(
        'effect', nargs='?',
        help='Effect ID (integer) or name (solid, pinwheel, heatmap, etc.). '
             'If not provided, shows current effect.'
    )
    effect_parser.add_argument(
        '-u', '--hue', default=None,
        help='Hue (0-255). If not provided, hue is set by the keyboard.'
    )
    effect_parser.add_argument(
        '-s', '--sat', default=255,
        help='Saturation (0-255). Default: 255'
    )
    effect_parser.add_argument(
        '-r', '--speed', type=int, default=128,
        help='Effect speed (0-255). Default: 128'
    )

    subparsers.add_parser('list-effects', help='List all supported RGB effects')


    #########################################################
    # Commands for RGB presets
    #########################################################
    preset_parser = subparsers.add_parser(
        'preset', help='Commands for RGB presets'
    )
    preset_subparsers = preset_parser.add_subparsers(
        dest='preset_command', help='Preset operations'
    )

    preset_subparsers.add_parser(
        'revert', help='Revert the current preset to the saved preset index'
    )

    preset_index_parser = preset_subparsers.add_parser(
        'index', help='Get the current preset index or set the preset index'
    )
    preset_index_parser.add_argument(
        'index', nargs='?',
        help='Preset index (0-7). If not provided, shows current preset index.'
    )

    preset_get_parser = preset_subparsers.add_parser(
        'get', help='Get the effect of a preset by index'
    )
    preset_get_parser.add_argument(
        'index', nargs='?',
        help='Preset index (0-7). If not provided, shows all presets.'
    )

    preset_set_parser = preset_subparsers.add_parser(
        'set', help='Set the effect of a preset at index'
    )
    preset_set_parser.add_argument(
        'index', type=int, help='Preset index (0-7)'
    )
    preset_set_parser.add_argument(
        'effect', nargs='?',
        help='Effect ID (integer) or name (solid, pinwheel, heatmap, etc.). '
    )
    preset_set_parser.add_argument(
        '-u', '--hue', default=None,
        help='Hue (0-255). If not provided, hue is set by the keyboard.'
    )
    preset_set_parser.add_argument(
        '-s', '--sat', default=255,
        help='Saturation (0-255). Default: 255'
    )
    preset_set_parser.add_argument(
        '-r', '--speed', type=int, default=128,
        help='Effect speed (0-255). Default: 128'
    )
    preset_set_parser.add_argument(
        '-a', '--startup-animation', type=str, default="START_ANIM_B_FADE_VAL",
        help='Startup animation. Default: START_ANIM_B_FADE_VAL. '
             'Options: ' + ', '.join(Preset.animation_option.keys())
    )
    

    #########################################################
    # Commands for Demos
    #########################################################
    subparsers.add_parser('game', help='Run a game')
    subparsers.add_parser('random-leds', help='Randomly test LEDs')


    #########################################################
    # Commands for keys
    #########################################################
    list_keycodes_parser = subparsers.add_parser(
        'list-keycodes', help='List all available QMK keycodes'
    )
    list_keycodes_parser.add_argument(
        '--filter', help='Filter keycodes by name (case-insensitive substring)'
    )
    list_keycodes_parser.add_argument(
        '--category',
        choices=['basic', 'modifiers', 'function', 'system', 'media', 'mouse'],
        help='Filter keycodes by category'
    )

    key_parser = subparsers.add_parser('key', help='Commands for key keycodes')
    key_subparsers = key_parser.add_subparsers(
        dest='key_command', help='Key operations'
    )

    key_get_all_parser = key_subparsers.add_parser('get-all', help='List the keycodes for all keys')
    key_get_all_parser.add_argument(
        '-l', '--layer', type=int, default=0, help='Layer number (default: 0)'
    )

    key_get_parser = key_subparsers.add_parser('get', help='Get keycode for a key')
    key_get_parser.add_argument('row', type=int, help='Key row in matrix')
    key_get_parser.add_argument('col', type=int, help='Key column in matrix')
    key_get_parser.add_argument(
        '-l', '--layer', type=int, default=0, help='Layer number (default: 0)'
    )

    key_set_parser = key_subparsers.add_parser('set', help='Set keycode for a key')
    key_set_parser.add_argument('row', type=int, help='Key row in matrix')
    key_set_parser.add_argument('col', type=int, help='Key column in matrix')
    key_set_parser.add_argument(
        'keycode',
        help='Keycode: QMK name (KC_A, KC_ENTER), number (65), or hex (0x41)'
    )
    key_set_parser.add_argument(
        '-l', '--layer', type=int, default=0, help='Layer number (default: 0)'
    )

    key_watch_parser = key_subparsers.add_parser(
        'watch', help='Watch for key presses and show their details'
    )
    key_watch_parser.add_argument(
        '-l', '--layer', type=int, default=0,
        help='Layer number to check (default: 0)'
    )
    key_watch_parser.add_argument(
        '--no-leds', action='store_true',
        help='Disable LED feedback when keys are pressed'
    )
    key_watch_parser.add_argument(
        '--exit-key', default='KC_ESCAPE',
        help='Key to exit watch mode (default: KC_ESCAPE)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        keyboard = RPiKeyboardConfig()

        #########################################################
        # Commands for keyboard control
        #########################################################
        if args.command == 'info':
            print(f"Keyboard Model: {keyboard.model}")
            if keyboard.variant:
                print(f"Keyboard Variant: {keyboard.variant}")

            uptime = keyboard.get_uptime()
            print(f"Uptime: {int(uptime / 1000)} seconds")

            rpi_version = keyboard.get_firmware_version()
            print(
                f"Raspberry Pi Keyboard Firmware Version: "
                f"{rpi_version[0]}.{rpi_version[1]}.{rpi_version[2]}"
            )

            unlocked, unlock_in_progress, unlock_keys = keyboard.get_unlock_status()
            print("Keyboard unlock keys:")
            for key in unlock_keys:
                keycode_name = get_keycode_name(
                    keyboard.get_keycode(matrix=key, layer=0)
                )
                print(
                    f"    Row: {key[0]}, Col: {key[1]} -> "
                    f"Keycode on layer 0: {keycode_name}"
                )
            if not unlocked:
                if unlock_in_progress:
                    print(
                        "Keyboard is currently in unlock process. "
                        "Please complete the unlock process or power cycle the keyboard."
                    )
                else:
                    print("Keyboard is locked.")
            else:
                print("Keyboard is unlocked.")

            if args.ascii:
                width = os.get_terminal_size().columns
                ascii_map = keyboard.get_ascii_keycode_map(width=width)
                print(ascii_map)

        elif args.command == 'unlock':
            keyboard.unlock()
            print("Keyboard unlocked")

        elif args.command == 'lock':
            keyboard.lock()
            print("Keyboard locked")
        
        elif args.command == 'reset-keymap':
            keyboard.reset_keymap()
            print("Keyboard keymap reset")
        
        elif args.command == 'reset-presets':
            keyboard.reset_presets_and_direct_leds()
            print("Keyboard presets and direct LEDs reset")
        
        elif args.command == 'get-version':
            version = keyboard.get_firmware_version()
            print(f"Keyboard version: {version[0]}.{version[1]}.{version[2]}")

        elif args.command == 'help':
            parser.print_help()
            return 0

        #########################################################
        # Commands for all LEDs
        #########################################################
        elif args.command == 'leds':
            if keyboard.model == "PI500":
                print("PI500 does not support LED operations")
                return 1

            if not args.leds_command:
                print("Please specify a LEDs command: clear, set, or info")
                print("Usage: rpi-keyboard-config leds {clear,set,info}")
                return 1

            if args.leds_command == 'clear':
                current_effect = keyboard.get_current_effect()
                if current_effect.effect != get_vial_effect_id("VIALRGB_EFFECT_DIRECT"):
                    keyboard.set_led_direct_effect()
                keyboard.rgb_clear()
                print("All LEDs cleared")
            elif args.leds_command == 'set':
                current_effect = keyboard.get_current_effect()
                if current_effect.effect != get_vial_effect_id("VIALRGB_EFFECT_DIRECT"):
                    keyboard.set_led_direct_effect()

                try:
                    hue, sat, val = parse_colour(args.colour)
                except ValueError as e:
                    print(f"Error: {e}")
                    return 1

                num_leds = keyboard.get_number_leds()
                for idx in range(num_leds):
                    keyboard.set_led_by_idx(idx=idx, colour=(hue, sat, val))
                keyboard.send_leds()
                print(
                    f"All {num_leds} LEDs set to colour: {args.colour} -> "
                    f"HSV({hue}, {sat}, {val})"
                )

            elif args.leds_command == 'get':
                leds = keyboard.get_current_direct_leds()
                for led in leds:
                    print(f""
                        f"LED {led.idx:2d}: matrix=[{led.matrix[0]:1d}, {led.matrix[1]:2d}], HSV=({led.colour[0]:3d}, {led.colour[1]:3d}, {led.colour[2]:3d})"
                    )
            elif args.leds_command == 'get-saved':
                leds = keyboard.get_saved_direct_leds()
                for led in leds:
                    print(f""
                        f"LED {led.idx:2d}: matrix=[{led.matrix[0]:1d}, {led.matrix[1]:2d}], HSV=({led.colour[0]:3d}, {led.colour[1]:3d}, {led.colour[2]:3d})"
                    )
            elif args.leds_command == 'save':
                keyboard.save_direct_leds()
                print("Current direct LEDs saved to EEPROM")
            elif args.leds_command == 'load':
                keyboard.load_direct_leds()
                print("Saved direct LEDs loaded from EEPROM")

        #########################################################
        # Commands for individual LED
        #########################################################
        elif args.command == 'led':
            if keyboard.model == "PI500":
                print("PI500 does not support LED operations")
                return 1

            if not args.led_command:
                print("Please specify a LED command: set")
                print("Usage: rpi-keyboard-config led {set}")
                return 1

            if args.led_command == 'set':
                current_effect = keyboard.get_current_effect()
                if current_effect.effect != get_vial_effect_id("VIALRGB_EFFECT_DIRECT"):
                    keyboard.set_led_direct_effect()

                position_str = args.position.strip()

                try:
                    hue, sat, val = parse_colour(args.colour)
                except ValueError as e:
                    print(f"ValueError: {e}")
                    return 1

                if ',' in position_str:
                    try:
                        parts = [int(x.strip()) for x in position_str.split(',')]
                        if len(parts) != 2:
                            print(
                                "Error: Matrix position must be exactly two values: row,col"
                            )
                            return 1
                        row, col = parts

                        keyboard.set_led_by_matrix(
                            matrix=[row, col], colour=(hue, sat, val)
                        )
                        keyboard.send_led_by_matrix(matrix=[row, col])
                        print(
                            f"LED at matrix position [{row}, {col}] set to colour: "
                            f"{args.colour} -> HSV({hue}, {sat}, {val})"
                        )
                    except ValueError as e:
                        print(f"ValueError: {e}")
                        return 1
                else:
                    try:
                        led_idx = int(position_str)
                    except ValueError:
                        print("Error: LED index must be an integer")
                        return 1

                    num_leds = keyboard.get_number_leds()
                    if not 0 <= led_idx < num_leds:
                        print(f"Error: LED index must be between 0 and {num_leds - 1}")
                        return 1

                    keyboard.set_led_by_idx(idx=led_idx, colour=(hue, sat, val))
                    keyboard.send_led_by_idx(led_idx)
                    print(
                        f"LED {led_idx} set to colour: {args.colour} -> "
                        f"HSV({hue}, {sat}, {val})"
                    )

        #########################################################
        # Commands for Hue and Brightness of the keyboard
        #########################################################
        elif args.command == 'hue':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            if args.hue is None:
                hue = keyboard.get_hue()
                print(f"Current hue: {hue} (0-255)")
            else:
                keyboard.set_hue(args.hue)
                print(f"Hue set to {args.hue} (0-255)")

        elif args.command == 'brightness':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            if args.brightness is None:
                brightness = keyboard.get_brightness()
                print(f"Current brightness: {brightness} (0-255)")
            else:
                keyboard.set_brightness(args.brightness)
                print(f"Brightness set to {args.brightness} (0-255)")

        #########################################################
        # Commands for RGB effects
        #########################################################
        elif args.command == 'list-effects':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1
            supported_effects = keyboard.get_supported_effects()

            print("Supported RGB Effects:")
            for effect_id in sorted(supported_effects):
                effect_name = get_vial_effect_name(effect_id, pretty_name=True)
                if effect_name is not None:
                    print(f"  ID {effect_id:2d}: {effect_name}")
                else:
                    print(f"  ID {effect_id:2d}: (no name)")
            print(f"\nTotal effects supported: {len(supported_effects)}")
            print(
                "\nYou can use either the ID number or any of the names listed above."
            )

        elif args.command == 'effect':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            if args.effect is None:
                try:
                    preset = keyboard.get_current_effect()
                    pretty_print_effect(preset)

                except Exception as e:
                    print(f"Error getting current effect: {e}")
                    return 1
            else:
                default_startup_animation = Preset.animation_option["START_ANIM_B_FADE_VAL"]
                preset = parse_preset_data(
                    keyboard, args.effect, args.speed, args.hue, 
                    args.sat, default_startup_animation
                )

                keyboard.set_temp_effect(preset=preset)
                print("Effect set successfully:")
                pretty_print_effect(preset)

        #########################################################
        # Commands for RGB presets
        #########################################################
        elif args.command == 'preset':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            if args.preset_command == 'index':
                if args.index is None:
                    preset_index = keyboard.get_current_preset_index()
                    saved_preset_index = keyboard.get_saved_preset_index()
                    if preset_index == 7:
                        print("Currently showing temporary effect")
                        print(f"Saved preset index: {saved_preset_index}")
                    elif preset_index != saved_preset_index:
                        print(f"Current preset index: {preset_index}")
                        print(f"Saved preset index: {saved_preset_index}")
                    else:
                        print(f"Current preset index: {preset_index}")
                else:
                    preset_index = int(args.index)
                    keyboard.set_current_preset_index(preset_index)
                    print(f"Preset index set to {preset_index}")
            
            elif args.preset_command == 'revert':
                keyboard.revert_to_saved_preset()
                print("Preset reverted to saved preset")

            elif args.preset_command == 'get':
                if args.index is None:
                    for preset_index in range(7):
                        preset_effect = keyboard.get_preset(preset_index)
                        print(f"Preset at index {preset_index}:")
                        pretty_print_preset(preset_effect)
                        print()
                    preset_effect = keyboard.get_preset(7)
                    print(f"The temporary effect was last set to:")
                    pretty_print_preset(preset_effect)
                    print()
                else:
                    preset_index = int(args.index)
                    if preset_index > 7:
                        raise ValueError(f"Preset index must be between 0 and 7")
                    preset = keyboard.get_preset(preset_index)
                    print(f"Preset at index {preset_index}:")
                    pretty_print_preset(preset)

            elif args.preset_command == 'set':
                preset_index = int(args.index)
                if preset_index > 6:
                    raise ValueError(f"Preset index must be between 0 and 6")
                
                if args.effect is None:
                    preset = keyboard.get_preset(preset_index)
                    effect_str = str(preset.effect)
                else:
                    effect_str = args.effect
                
                preset = parse_preset_data(
                    keyboard, effect_str, args.speed, args.hue, 
                    args.sat, args.startup_animation
                )
                
                if preset_index == 0 and preset.effect == VIALRGB_EFFECT_SKIP:
                    raise ValueError("Cannot set preset 0 to skip effect")
                if preset_index == 7 and preset.effect == VIALRGB_EFFECT_SKIP:
                    raise ValueError("Cannot set custom effect to skip effect")
                keyboard.set_preset(preset_index, preset)
                print(f"Preset {preset_index} set to:")
                pretty_print_preset(preset)

            else:
                print("Please specify a preset command: index, get, or set")
                print("Usage: rpi-keyboard-config preset {index,get,set}")
                return 1

        #########################################################
        # Commands for Demos
        #########################################################
        elif args.command == 'game':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            game_main()

        elif args.command == 'random-leds':
            if keyboard.model == "PI500":
                print("PI500 does not support RGB operations")
                return 1

            random_leds_main()

        #########################################################
        # Commands for keys
        #########################################################
        elif args.command == 'list-keycodes':
            list_keycodes(args.filter, args.category)

        elif args.command == 'key':
            if not args.key_command:
                print("Please specify a key command: get, set, or watch")
                print("Usage: rpi-keyboard-config key {get,set,watch}")
                return 1

            if args.key_command == 'get':
                row = args.row
                col = args.col
                layer = args.layer

                try:
                    keycode = keyboard.get_keycode(matrix=[row, col], layer=layer)
                    keycode_name = get_keycode_name(keycode)
                    print(f"Key at row {row}, col {col}, layer {layer}:")
                    print(f"  Keycode: {keycode} (0x{keycode:04X})")
                    print(f"  QMK Name: {keycode_name}")
                except Exception as e:
                    print(f"Error getting keycode: {e}")
                    return 1

            elif args.key_command == 'get-all':
                keynames = keyboard.get_all_keynames(args.layer)
                for data in keynames:
                    print(f"Key at row {data['position'][0]:2d}, col {data['position'][1]:2d}:"
                          f"  Keycode: {data['keycode']:5d} (0x{data['keycode']:04X}) -> {data['name']}")

            elif args.key_command == 'set':
                row = args.row
                col = args.col
                layer = args.layer
                keycode_input = args.keycode

                try:
                    keycode = parse_keycode(keycode_input)
                except ValueError as e:
                    print(f"Error: {e}")
                    return 1

                if not 0 <= keycode <= 0xFFFF:
                    print("Error: Keycode must be between 0 and 65535 (0xFFFF)")
                    return 1

                try:
                    keyboard.set_keycode(
                        matrix=[row, col], layer=layer, keycode=keycode
                    )
                    keycode_name = get_keycode_name(keycode)
                    print(
                        f"Key at row {row}, col {col}, layer {layer} set successfully:"
                    )
                    print(f"  Input: {keycode_input}")
                    print(f"  Keycode: {keycode} (0x{keycode:04X})")
                    print(f"  QMK Name: {keycode_name}")
                except Exception as e:
                    print(f"Error setting keycode: {e}")
                    return 1

            elif args.key_command == 'watch':
                if not args.no_leds and keyboard.model == "PI500":
                    print("PI500 does not support LED operations for key feedback")
                    use_leds = False
                else:
                    use_leds = not args.no_leds

                layer = args.layer

                unlocked, unlock_in_progress, unlock_keys = keyboard.get_unlock_status()
                if not unlocked:
                    if unlock_in_progress:
                        print("ERROR: Keyboard is currently in unlock process.")
                        print(
                            "Please complete the unlock process or power cycle the keyboard."
                        )
                        return 1
                    print(
                        "ERROR: Keyboard is locked and cannot be used for key monitoring."
                    )
                    print(
                        "Please run 'rpi-keyboard-config unlock' first to unlock the keyboard."
                    )
                    return 1

                try:
                    exit_keycode = parse_keycode(args.exit_key)
                except ValueError as e:
                    print(f"Error parsing exit key: {e}")
                    return 1

                print("Key press monitor started")
                print(f"Layer: {layer}")
                print(f"Exit key: {args.exit_key} (keycode {exit_keycode})")
                if use_leds:
                    print("LED feedback: enabled (use --no-leds to disable)")
                    current_effect = keyboard.get_current_effect()
                    if current_effect.effect != get_vial_effect_id("VIALRGB_EFFECT_DIRECT"):
                        keyboard.set_led_direct_effect()
                    keyboard.rgb_clear()
                else:
                    print("LED feedback: disabled")
                print("Press Ctrl+C or the exit key to stop...")
                print()

                try:
                    active_keys_prev = []

                    while True:
                        active_keys = keyboard.get_switch_matrix_state()

                        newly_pressed = [
                            matrix for matrix in active_keys 
                            if matrix not in active_keys_prev
                        ]
                        for matrix in newly_pressed:
                            try:
                                keycode = keyboard.get_keycode(
                                    matrix=matrix, layer=layer
                                )
                                keycode_name = get_keycode_name(keycode)
                                print(
                                    f"PRESS   Row {matrix[0]:2d}, Col {matrix[1]:2d} -> "
                                    f"Keycode: {keycode:5d} (0x{keycode:04X}) -> {keycode_name}"
                                )

                                if keycode == exit_keycode:
                                    print(
                                        f"Exit key ({keycode_name}) pressed. Stopping..."
                                    )
                                    if use_leds:
                                        keyboard.rgb_clear()
                                    return 0

                                if use_leds:
                                    keyboard.set_led_by_matrix(
                                        matrix=matrix, colour=(255, 255, 255)
                                    )
                            except Exception as e:
                                print(f"Error reading key at {matrix}: {e}")

                        newly_released = [
                            matrix for matrix in active_keys_prev 
                            if matrix not in active_keys
                        ]
                        for matrix in newly_released:
                            try:
                                keycode = keyboard.get_keycode(
                                    matrix=matrix, layer=layer
                                )
                                keycode_name = get_keycode_name(keycode)
                                print(
                                    f"RELEASE Row {matrix[0]:2d}, Col {matrix[1]:2d} -> "
                                    f"Keycode: {keycode:5d} (0x{keycode:04X}) -> {keycode_name}"
                                )

                                if use_leds:
                                    keyboard.set_led_by_matrix(
                                        matrix=matrix, colour=(0, 0, 0)
                                    )
                            except Exception as e:
                                print(f"Error reading released key at {matrix}: {e}")

                        if use_leds and (newly_pressed or newly_released):
                            keyboard.send_leds()

                        active_keys_prev = active_keys.copy()
                        time.sleep(0.01)

                except KeyboardInterrupt:
                    print("\nStopping key monitor...")
                    if use_leds:
                        keyboard.rgb_clear()
                        keyboard.revert_to_saved_preset()
                    print("Key monitor stopped")

        else:
            parser.print_help()
            return 1

        keyboard.close()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
        keyboard.close()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
