"""RPi Keyboard Config for managing keyboard settings and RGB lighting."""

import struct
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from .atco_s import at, co
from .hid import Device, enumerate_devices, HIDException
from .keycodes import qmk_keycode_to_key, keyboard_ascii_art
from .effects import get_vial_effect_id, get_vial_effect_name
from .switch_matrix import (
    convert_switch_matrix, SWITCH_MATRIX_PI500,
    SWITCH_MATRIX_CONVERSION_PI500_ISO, SWITCH_MATRIX_PI500PLUS_ISO,
    SWITCH_MATRIX_PI500PLUS_ANSI, SWITCH_MATRIX_PI500PLUS_JIS
)

USB_VID_RASPBERRYPI = 0x2e8a
USB_PID_PI500_KEYBOARD = 0x0010
USB_PID_PI500PLUS_KEYBOARD = 0x0011
USAGE_PAGE = 0xFF60
USAGE = 0x61

MSG_LEN = 32
VIAL_SERIAL_NUMBER = "vial:f64c2b3c"

VIALRGB_EFFECT_DIRECT = 1

CMD_GET_PROTOCOL_VERSION = 0x01
CMD_GET_KEYBOARD_VALUE = 0x02
CMD_SET_KEYBOARD_VALUE = 0x03
CMD_VIA_DYNAMIC_KEYMAP_GET_KEYCODE = 0x04
CMD_VIA_DYNAMIC_KEYMAP_SET_KEYCODE = 0x05
CMD_VIA_DYNAMIC_KEYMAP_RESET = 0x06
CMD_LIGHTING_SET_VALUE = 0x07
CMD_LIGHTING_GET_VALUE = 0x08
CMD_VIAL_COMMAND = 0xFE
CMD_RPI_COMMAND = 0xFC

KEYBOARD_VALUE_GET_UPTIME = 0x01
KEYBOARD_VALUE_GET_LAYOUT_OPTIONS = 0x02
KEYBOARD_VALUE_GET_SWITCH_MATRIX_STATE = 0x03

VIAL_GET_KEYBOARD_ID = 0x00
VIAL_GET_SIZE = 0x01
VIAL_GET_DEFINITION = 0x02
VIAL_GET_UNLOCK_STATUS = 0x05
VIAL_UNLOCK_START = 0x06
VIAL_UNLOCK_POLL = 0x07
VIAL_LOCK = 0x08

VIALRGB_GET_INFO = 0x40
VIALRGB_GET_MODE = 0x41
VIALRGB_GET_SUPPORTED = 0x42
VIALRGB_GET_NUMBER_LEDS = 0x43
VIALRGB_GET_LED_INFO = 0x44

VIALRGB_SET_MODE = 0x41
VIALRGB_DIRECT_FASTSET = 0x42

RPI_CMD_GET_VERSION = 0x01
RPI_CMD_RESET_EEPROM = 0x02
RPI_CMD_GET_CURRENT_MODE_INDEX = 0x03
RPI_CMD_SET_CURRENT_MODE_INDEX = 0x04
RPI_CMD_GET_MODE = 0x05
RPI_CMD_SET_MODE = 0x06
RPI_CMD_GET_HUE = 0x07
RPI_CMD_SET_HUE = 0x08
RPI_CMD_GET_BRIGHTNESS = 0x09
RPI_CMD_SET_BRIGHTNESS = 0x0A
RPI_CMD_GET_CURRENT_DIRECT_LEDS = 0x0B
RPI_CMD_GET_SAVED_DIRECT_LEDS = 0x0C
RPI_CMD_SAVE_DIRECT_LEDS = 0x0D
RPI_CMD_LOAD_DIRECT_LEDS = 0x0E

REPORT_LENGTH = 32


class LED:
    """Represents an LED with position, matrix coordinates, and colour properties."""

    def __init__(
        self, *, idx: int, matrix: List[int], flags: int, x: int, y: int
    ) -> None:
        """Initialise LED with index, matrix position, flags, and coordinates.

        Args:
            idx: LED index number
            matrix: Matrix position as [row, column]
            flags: LED flags
            x: X coordinate (0-224)
            y: Y coordinate (0-64)
        """
        self.idx = idx
        self.x = x
        self.y = y
        self.flags = flags
        self.matrix = matrix  # [row, column]
        self.colour = (0, 0, 0)  # (hue, saturation, value)

    def __repr__(self) -> str:
        """Return string representation of LED.
        
        Returns:
            String containing LED index, matrix position, flags, coordinates, and color
        """
        return (f"LED(idx:{self.idx}, matrix:{self.matrix},"
                f"flags:{self.flags}, x:{self.x}, y:{self.y}, colour:{self.colour})")

class Preset:
    """Represents a preset with led flags, effect id, speed,
    fixed hue, startup animation, hue, and saturation."""

    LED_FLAG_ALL = 0xFF
    LED_FLAG_NONE = 0x00

    animation_option = {
        "START_ANIM_NONE": 0x00,
        "START_ANIM_B_NO_FADE": 0x01,
        "START_ANIM_B_FADE_VAL": 0x02,
        "START_ANIM_W_NO_FADE": 0x03,
        "START_ANIM_W_FADE_SAT": 0x04
    }

    def __init__(
        self, *, effect, flags=LED_FLAG_ALL, speed=255,
        fixed_hue=False, 
        startup_animation=animation_option["START_ANIM_B_FADE_VAL"], 
        hue=255, sat=255
    ):
        """Initialise preset with mode index, flags, effect, speed, 
        fixed hue, startup animation, hue, and saturation."""
        self.flags = flags
        self.effect = effect
        self.speed = speed
        self.fixed_hue = fixed_hue
        self.startup_animation = startup_animation
        self.hue = hue
        self.sat = sat
    
    def __repr__(self) -> str:
        """Return string representation of Preset.
        
        Returns:
            String containing preset configuration details
        """
        animation_name = next(
            (name for name, code in Preset.animation_option.items() 
             if code == self.startup_animation), 
            f"Unknown ({self.startup_animation})"
        )
        return (f"Preset(effect: {self.effect}, speed: {self.speed},"
                f"fixed_hue: {'True' if self.fixed_hue else 'False'},"
                f"startup_animation: {animation_name}"
                f"hue: {self.hue}, sat: {self.sat})")


def get_pi_country_code() -> str:
    """Get country code from Raspberry Pi device tree.

    Returns:
        str: Country layout code (ANSI, JIS, or ISO)
    """
    with open("/proc/device-tree/chosen/rpi-country-code", "rb") as f:
        f.seek(3)
        country_code = ord(f.read(1))
    if country_code in (4, 14, 16):
        return "ANSI"
    if country_code == 7:
        return "JIS"
    return "ISO"


class NoKeyboardFoundError(Exception):
    """Raised when no compatible keyboard is found."""


class KeyboardNotCompatibleError(Exception):
    """Raised when the keyboard is not compatible with this config."""


class RPiKeyboardConfig():
    """Raspberry Pi Keyboard Config for managing settings and RGB lighting."""

    def __init__(self, path: Optional[str] = None) -> None:
        """Initialise the keyboard config.

        Args:
            path: Optional device path. If None, searches for compatible devices.
        """
        self.model = None
        self.variant = None
        self.switch_matrix = None
        self.conversion_switch_matrix = None
        self._led_map = None

        if path is None:
            path = self._search_devices()
        self._get_hid_interface(path)

        if self.model == "PI500":
            leds = []
            for idx in range(6*16):
               x, y, flags, matrix = (0, 0, 0, [idx//16, idx%16])
               leds.append(LED(idx=idx, matrix=matrix, flags=flags, x=x, y=y))
            self._led_map = leds
            self.switch_matrix = SWITCH_MATRIX_PI500
            country_code = get_pi_country_code()
            self.variant = country_code
            if country_code == "ANSI":
                self.conversion_switch_matrix = SWITCH_MATRIX_CONVERSION_PI500_ISO
            elif country_code == "JIS":
                self.conversion_switch_matrix = SWITCH_MATRIX_CONVERSION_PI500_ISO
            else:
                self.conversion_switch_matrix = SWITCH_MATRIX_CONVERSION_PI500_ISO
        elif self.model == "PI500PLUS":
            if self.variant == "ISO":
                self.switch_matrix = SWITCH_MATRIX_PI500PLUS_ISO
            elif self.variant == "ANSI":
                self.switch_matrix = SWITCH_MATRIX_PI500PLUS_ANSI
            elif self.variant == "JIS":
                self.switch_matrix = SWITCH_MATRIX_PI500PLUS_JIS

        # Check if keyboard was previously asked to unlock and is still waiting
        _unlocked, unlock_in_progress, _keys = self.get_unlock_status()
        if unlock_in_progress:
            print("Keyboard is waiting for unlock. Not usable until unlocked "
                  "or power cycled.")
            print()
            self.unlock(restricted_commands=True)

        via_protocol_version = self.get_via_protocol_version()
        vial_protocol_version, _keyboard_uid, flags = self.get_vial_information()
        rpi_version = self.get_firmware_version()

        # Must be Via protocol 9 or later
        if via_protocol_version < 9:
            raise KeyboardNotCompatibleError(
                "The keyboard does not support Via protocol 9 or later")

        # must be Vial protocl 4 or later
        if vial_protocol_version < 4:
            raise KeyboardNotCompatibleError(
                "The keyboard does not support Vial protocol 4 or later")
        
        if self.model == "PI500":
            if rpi_version < (1, 2, 0):
                raise KeyboardNotCompatibleError(
                    "The keyboard does not support firmware version 1.2.0 or later")
        elif self.model == "PI500PLUS":
            if rpi_version < (1, 2, 0):
                raise KeyboardNotCompatibleError(
                    "The keyboard does not support firmware version 1.2.0 or later")

        if self.model == "PI500PLUS":
            # must have VialRGB flag set
            if (flags & 1) == 0:
                print(
                    "The keyboard does not support VialRGB so RGB operations "
                    "will not be available."
                )

        if self.model == "PI500PLUS":
            self._led_map = self.get_leds()

    def _search_devices(self) -> str:
        """Search for compatible Raspberry Pi keyboards.

        Returns:
            Device path of the first compatible keyboard found.
        """
        rpi_keyboards = []
        for desc in enumerate_devices():
            if (desc['vendor_id'] == USB_VID_RASPBERRYPI
                and (desc['product_id'] == USB_PID_PI500_KEYBOARD
                     or desc['product_id'] == USB_PID_PI500PLUS_KEYBOARD)):
                rpi_keyboards.append(desc)

        if len(rpi_keyboards) == 0:
            raise NoKeyboardFoundError("No Raspberry Pi Keyboard found")

        rpi_vial_keyboards = []
        for desc in rpi_keyboards:
            if (desc['serial_number'] == VIAL_SERIAL_NUMBER
                    and desc['usage_page'] == USAGE_PAGE
                    and desc['usage'] == USAGE):
                rpi_vial_keyboards.append(desc)

        if len(rpi_vial_keyboards) == 0:
            raise KeyboardNotCompatibleError(
                "The Raspberry Pi Keyboard is not running compatible firmware. "
                "Please update the keyboard's firmware to continue.")

        if (len(rpi_vial_keyboards) > 1 and 
                len(rpi_vial_keyboards) != len(rpi_keyboards)):
            print("Multiple keyboards found, using the first compatible one.")
        elif len(rpi_vial_keyboards) > 1:
            print("Multiple keyboards found, using the first one.")

        return rpi_vial_keyboards[0]['path']

    def _get_hid_interface(self, path: str) -> Device:
        """Initialise HID interface with the keyboard device.

        Args:
            path: Device path for the HID interface.
        """
        try:
            self._device = Device(path=path)
        except HIDException as e:
            print(f"Error initialising HID interface: {e}")
            raise KeyboardNotCompatibleError(
                "Unable to connect to the keyboard. "
                "Try running with sudo or add udev rules."
            ) from e

        self._flush_hid_buffer()

        info = self._device.product

        # Extract model and variant information from product string
        if "Pi 500 Keyboard" in info:
            self.model = "PI500"
        elif "Pi 500+ Keyboard" in info:
            self.model = "PI500PLUS"

            if "ISO" in info:
                self.variant = "ISO"
            elif "ANSI" in info:
                self.variant = "ANSI"
            elif "JIS" in info:
                self.variant = "JIS"
        else:
            raise KeyboardNotCompatibleError("Unknown keyboard model")

    def _flush_hid_buffer(self) -> None:
        """Flush the HID buffer.
        
        Reads and discards any pending data from the HID device buffer.
        """
        empty = False
        while not empty:
            response = self._device.read(1, timeout=500)
            if response == b'':
                empty = True

    def close(self) -> None:
        """Close the HID device connection.
        
        Safely closes the HID device connection if it exists.
        """
        if hasattr(self, '_device'):
            self._device.close()

    def _send_command(self, command: List[int]) -> List[int]:
        """Send a command to the keyboard and return the response.

        Args:
            command: Command data to send (without report ID or padding).

        Returns:
            Response data from the keyboard.
        """
        # Add report ID (0x00) and pad to MSG_LEN
        if isinstance(command, bytes):
            command_data = command
        else:
            command_data = bytes(command)

        # All hid reports begin with a report ID of 0x00 followed by 
        # MSG_LEN bytes of data
        padded_command = struct.pack(f'<B{len(command_data)}s{MSG_LEN - len(command_data)}x',
                                     0x00, command_data)

        self._device.write(padded_command)
        response = self._device.read(MSG_LEN, timeout=1000)
        return response

    def _send_check_command(self, cmd:int, subcmd:int=None, data:bytes=None) -> bytes:
        """Send a command and check the response.
        
        Args:
            cmd: Main command byte
            subcmd: Optional subcommand byte
            data: Optional data payload
            
        Returns:
            Response data from the keyboard
        """
        payload = cmd.to_bytes(1, byteorder="little")
        if not subcmd is None:
            payload += subcmd.to_bytes(1, byteorder="little")
        if not data is None:
            payload += data
        raw_data = self._send_command(payload)
        rsubcmd = None
        if subcmd is None:
            rcmd = struct.unpack("B", raw_data[0:1])[0]
        else:
            rcmd, rsubcmd = struct.unpack("<BB", raw_data[0:2])
        flush_limit = 5
        flush_count = 0
        while (rcmd != cmd or rsubcmd != subcmd):
            raw_data = self._send_command(payload)
            rcmd, rsubcmd = struct.unpack("<BB", raw_data[0:2])
            flush_count += 1
            if flush_count > flush_limit:
                print(f"Keyboard is not responding as expected. Raw response: {raw_data}")
                raise KeyboardNotCompatibleError(
                    "Keyboard is not responding as expected."
                )
        return raw_data

    def get_firmware_version(self) -> str:
        """Get the Raspberry Pi keyboard firmware version.
        
        Returns:
            Tuple of (major, minor, patch) version numbers
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_VERSION)
        version_x = int.from_bytes(raw_data[2:3], byteorder="little")
        version_y = int.from_bytes(raw_data[3:4], byteorder="little") >> 4
        version_z = int.from_bytes(raw_data[3:4], byteorder="little") & 0x0F
        return (version_x, version_y, version_z)

    def get_via_protocol_version(self) -> Tuple[int, int]:
        """Get the Via protocol version from the keyboard.

        Returns:
            Via protocol version number.
        """
        raw_data = self._send_check_command(CMD_GET_PROTOCOL_VERSION, 0)
        via_protocol_version = struct.unpack(">H", raw_data[1:3])[0]
        return via_protocol_version

    def get_vial_information(self) -> Dict[str, Any]:
        """Get Vial protocol information from the keyboard.

        Returns:
            Tuple of (vial_protocol, keyboard_uid, vialrgb_flag).
        """
        raw_data = self._send_command(struct.pack("BB", CMD_VIAL_COMMAND, VIAL_GET_KEYBOARD_ID))
        vial_protocol, keyboard_uid, vialrgb_flag = struct.unpack("<IQB", raw_data[0:13])
        return vial_protocol, keyboard_uid, vialrgb_flag

    def get_vialrgb_info(self) -> Dict[str, Any]:
        """Get VialRGB information from the keyboard.

        Returns:
            Tuple of (vialrgb_protocol_version, maximum_brightness).
        """
        raw_data = self._send_check_command(CMD_LIGHTING_GET_VALUE, VIALRGB_GET_INFO)
        vialrgb_protocol_version, maximum_brightness = struct.unpack(
            "<HB", raw_data[2:5])
        return vialrgb_protocol_version, maximum_brightness

    def _reset_rpi_eeprom(self) -> None:
        """Reset the Raspberry Pi section of the EEPROM.
        
        Resets keyboard configuration stored in EEPROM to factory defaults.
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_RESET_EEPROM)
    
    def reset_presets_and_direct_leds(self) -> None:
        """Reset RGB presets and direct LED configurations.
        
        Clears all custom RGB effects and LED color settings.
        """
        self._reset_rpi_eeprom()
    
    def reset_keymap(self) -> None:
        """Reset the VIA dynamic keymap to defaults.
        
        Restores all key mappings to their default values.
        """
        self._send_check_command(CMD_VIA_DYNAMIC_KEYMAP_RESET)

    def get_uptime(self) -> int:
        """Get the keyboard uptime.

        Returns:
            Uptime in milliseconds.
        """
        raw_data = self._send_check_command(CMD_GET_KEYBOARD_VALUE, KEYBOARD_VALUE_GET_UPTIME)
        uptime = struct.unpack(">I", raw_data[2:6])[0]
        return uptime

    def get_supported_effects(self) -> List[str]:
        """Get the list of supported RGB effects.

        Returns:
            List of supported effect IDs.
        """
        if self.model == "PI500":
            raise KeyboardNotCompatibleError("PI500 does not support RGB operations")

        effects = [0x0000, 0xFFFF] # All support off and skip effect
        max_effect = 0
        while max_effect < 0xFFFF:
            raw_data = self._send_check_command(CMD_LIGHTING_GET_VALUE, VIALRGB_GET_SUPPORTED, max_effect.to_bytes(2, byteorder="little"))
            effects_data = list(struct.unpack("<15H", raw_data[2:]))
            for effect in effects_data:
                if effect == 0xFFFF:
                    return effects
                effects.append(effect)
                max_effect = effect
        return effects

    def get_keycode(self, *, matrix: List[int], layer: int, dont_convert: bool = False) -> int:
        """Get the keycode for a specific matrix position and layer.

        Args:
            matrix: Matrix position as [row, col].
            layer: Layer number (default 0).

        Returns:
            Keycode value.
        """
        if self.conversion_switch_matrix is None or dont_convert:
            row, col = matrix
        else:
            row, col = convert_switch_matrix(matrix, self.conversion_switch_matrix, self.switch_matrix)

        raw_data = self._send_check_command(CMD_VIA_DYNAMIC_KEYMAP_GET_KEYCODE, data=struct.pack(">BBB", layer, row, col))
        layer, row, col, keycode = struct.unpack(">BBBH", raw_data[1:6])
        return keycode

    def set_keycode(self, *, matrix: List[int], layer: int, keycode: int, dont_convert: bool = False) -> None:
        """Set the keycode for a specific matrix position and layer.

        Args:
            matrix: Matrix position as [row, col].
            keycode: Keycode value to set.
            layer: Layer number (default 0).
        """
        if self.conversion_switch_matrix is None or dont_convert:
            row, col = matrix
        else:
            row, col = convert_switch_matrix(matrix, self.conversion_switch_matrix, self.switch_matrix)

        raw_data = self._send_check_command(CMD_VIA_DYNAMIC_KEYMAP_SET_KEYCODE, data=struct.pack(">BBBH", layer, row, col, keycode))
        layer, row, col, keycode = struct.unpack(">BBBH", raw_data[1:6])

    def get_ascii_keycode_map(self, layer: int = 0, width: int = 81) -> str:
        """Get ASCII art representation of the keyboard with keycodes.

        Args:
            layer: Layer number to display (default: 0).

        Returns:
            ASCII art string showing the keyboard layout with keycode names.
        """
        keynames = []
        for position in self.switch_matrix:
            keycode = self.get_keycode(matrix=position, layer=layer, dont_convert=True)
            keynames.append(qmk_keycode_to_key.get(keycode, "USER"))
        return keyboard_ascii_art(self.model, self.variant, keynames, width=width)

    def get_all_keynames(self, layer: int = 0) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """Get the keynames for all keys on a layer.

        Args:
            layer: Layer number to display (default: 0).

        Returns:
            List of keynames.
        """
        keynames = []
        for position in self.switch_matrix:
            keycode = self.get_keycode(matrix=position, layer=layer, dont_convert=True)
            keynames.append({
                "position": position,
                "keycode": keycode,
                "name": qmk_keycode_to_key.get(keycode, "USER")
            })
        return keynames

    def led_matrix_to_idx(self, *, matrix: Tuple[int, int]) -> int:
        """Convert a matrix position to an LED index.
        
        Args:
            matrix: Matrix position as [row, col].

        Returns:
            LED index.
        """
        if self.conversion_switch_matrix is None or self.model == "PI500":
            position = matrix
        else:
            position = convert_switch_matrix(matrix, self.conversion_switch_matrix, self.switch_matrix)
        for led in self._led_map:
            if led.matrix == position:
                return led.idx
        raise ValueError(f"LED not found at matrix position {matrix}")

    def get_number_leds(self) -> int:
        """Get the number of LEDs in the keyboard.

        Returns:
            Number of LEDs.
        """
        if self.model == "PI500":
            #raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
            return 6*16
        raw_data = self._send_check_command(CMD_LIGHTING_GET_VALUE, VIALRGB_GET_NUMBER_LEDS)
        num_leds = struct.unpack("<H", raw_data[2:4])[0]
        return num_leds

    def get_led_info(self, idx: int) -> LED:
        """Get information about a specific LED.

        Args:
            idx: LED index.

        Returns:
            Tuple of (x, y, flags, row, col).
        """
        if self.model == "PI500":
            raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
        raw_data = self._send_check_command(CMD_LIGHTING_GET_VALUE, VIALRGB_GET_LED_INFO, idx.to_bytes(1, byteorder="little"))
        x, y, flags, row, col = struct.unpack("<BBBBB", raw_data[2:7])
        
        if self.conversion_switch_matrix is None:
            position = [row, col]
        else:
            position = convert_switch_matrix([row, col], self.conversion_switch_matrix, self.switch_matrix)
        
        return x, y, flags, position

    def get_leds(self) -> List[LED]:
        """Get LED information for all LEDs in the keyboard.

        Returns:
            List of LED objects with position and matrix information.
        """
        if self.model == "PI500":
            raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
        num_leds = self.get_number_leds()

        leds = []
        for idx in range(num_leds):
            x, y, flags, matrix = self.get_led_info(idx)
            leds.append(LED(idx=idx, matrix=matrix, flags=flags, x=x, y=y))

        return leds

    def send_leds(self) -> None:
        """Send LED color data to the keyboard.
        
        Transmits all pending LED colour changes to the keyboard hardware.
        Must be called after setting LED colours to apply changes.
        """
        if self.model == "PI500":
            #raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
            leds = self._led_map
            col = 7
            for led in leds:
                if led.colour == (60, 255, 255): # BIRD_COLOUR
                    col = 3
                elif led.colour == (120, 255, 200): # PIPE_COLOUR
                    col = 6
                elif led.colour == (0, 0, 0): # BG_COLOUR
                    col = 9
                elif led.colour == (190, 255, 255): # SCORE_COLOUR
                    col = 5
                elif led.colour == (0, 255, 255): # Red
                    col = 1
                print(end='%s%s '%(at(led.matrix[0], led.matrix[1]),co(0,col)))
            print(end='%s%s'%(at(8, 0), co(0, 7)), flush=True)
            return

        leds = self._led_map
        send_per_packet = 9
        sent = 0

        while sent < len(leds):
            buffer = []
            leds_to_send = leds[sent:sent + send_per_packet]

            for led in leds_to_send:
                buffer.extend([led.colour[0], led.colour[1], led.colour[2]])

            payload = struct.pack("<HB", sent, len(leds_to_send))
            payload += b"".join(x.to_bytes(1, byteorder="little") for x in buffer)

            self._send_check_command(CMD_LIGHTING_SET_VALUE,VIALRGB_DIRECT_FASTSET, data=payload)

            sent += len(leds_to_send)
    
    def send_led_by_idx(self, led_idx: int) -> None:
        """Send a single LED color update to the keyboard.
        
        Args:
            led_idx: Index of the LED to update
        """
        if self.model == "PI500":
            raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
        
        leds = self._led_map
        send_per_packet = 9
        sent = 0
        
        buffer = [leds[led_idx].colour[0], leds[led_idx].colour[1], leds[led_idx].colour[2]]
        
        payload = struct.pack("<HB", led_idx, 1)
        payload += b"".join(x.to_bytes(1, byteorder="little") for x in buffer)

        self._send_check_command(CMD_LIGHTING_SET_VALUE,VIALRGB_DIRECT_FASTSET, data=payload)
    
    def send_led_by_matrix(self, *, matrix: Tuple[int, int]) -> None:
        """Send a single LED color update by matrix position.
        
        Args:
            matrix: Matrix position as (row, col) tuple
        """
        self.send_led_by_idx(led_idx=self.led_matrix_to_idx(matrix=matrix))

    def set_led_by_idx(self, *, idx: int, colour: Tuple[int, int, int]) -> None:
        """Set the colour of a specific LED by index.

        Args:
            idx: LED index.
            colour: Colour as tuple of (hue, saturation, value).
        """
        self._led_map[idx].colour = colour

    def set_led_by_matrix(self, *, matrix: List[int], colour: Tuple[int, int, int]) -> None:
        """Set LED colour by matrix position.

        Args:
            matrix: Matrix position as [row, col].
            colour: Colour as tuple of (hue, saturation, value).
        """
        self.set_led_by_idx(idx=self.led_matrix_to_idx(matrix=matrix), colour=colour)

    def rgb_clear(self) -> None:
        """Clear all LED colors by setting them to black.
        
        Sets all LEDs to (0, 0, 0) HSV values, effectively turning them off.
        """
        for idx in range(len(self._led_map)):
            self.set_led_by_idx(idx=idx, colour=(0, 0, 0))
        self.send_leds()


    def get_hue(self) -> int:
        """Get the current global hue setting.
        
        Returns:
            Current hue value (0-255)
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_HUE)
        hue = int.from_bytes(raw_data[2:3], byteorder="little")
        return hue
    
    def set_hue(self, hue: int) -> None:
        """Set the global hue for keyboard effects.
        
        Args:
            hue: Hue value to set (0-255)
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_SET_HUE, data=hue.to_bytes(1, byteorder="little"))
    
    def get_brightness(self) -> int:
        """Get the current global brightness setting.
        
        Returns:
            Current brightness value (0-255)
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_BRIGHTNESS)
        brightness = int.from_bytes(raw_data[2:3], byteorder="little")
        return brightness
    
    def set_brightness(self, brightness: int) -> None:
        """Set the global brightness for keyboard effects.
        
        Args:
            brightness: Brightness value to set (0-255)
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_SET_BRIGHTNESS, data=brightness.to_bytes(1, byteorder="little"))

    def get_current_direct_leds(self) -> List[LED]:
        """Get current direct LED color values.
        
        Returns:
            List of LED objects with saved color configurations
        """
        leds = self._led_map.copy()
        leds_per_packet = 9
        retrieved = 0

        while retrieved < len(leds):
            raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_CURRENT_DIRECT_LEDS, data=struct.pack("<HB", retrieved, leds_per_packet))
            
            for i in range(leds_per_packet):
                if retrieved + i < len(leds):
                    leds[retrieved + i].colour = struct.unpack("<BBB", raw_data[5 + i * 3:8 + i * 3])
            retrieved += leds_per_packet

        return leds
    
    def get_saved_direct_leds(self) -> List[LED]:
        """Get saved direct LED configurations from the keyboard's EEPROM.
        
        Returns:
            List of LED objects with saved color configurations
        """
        leds = self._led_map.copy()
        leds_per_packet = 9
        retrieved = 0

        while retrieved < len(leds):
            raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_SAVED_DIRECT_LEDS, data=struct.pack("<HB", retrieved, leds_per_packet))
            
            for i in range(leds_per_packet):
                if retrieved + i < len(leds):
                    leds[retrieved + i].colour = struct.unpack("<BBB", raw_data[5 + i * 3:8 + i * 3])
            retrieved += leds_per_packet

        return leds
    
    def save_direct_leds(self) -> None:
        """Save current LED colors to the keyboard's EEPROM.
        
        Stores the current LED color configuration persistently.
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_SAVE_DIRECT_LEDS)
    
    def load_direct_leds(self) -> None:
        """Load saved LED colors from the keyboard's EEPROM.
        
        Restores previously saved LED color configuration.
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_LOAD_DIRECT_LEDS)

    def get_current_preset_index(self) -> int:
        """Get the current RGB preset index.
        
        Returns:
            Current preset index (0-7)
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_CURRENT_MODE_INDEX)
        current_index, saved_index = struct.unpack("<BB", raw_data[2:4])
        return current_index
    
    def get_saved_preset_index(self) -> int:
        """Get the saved RGB preset index from EEPROM.
        
        Returns:
            Saved preset index (0-7)
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_CURRENT_MODE_INDEX)
        current_index, saved_index = struct.unpack("<BB", raw_data[2:4])
        return saved_index
    
    def set_current_preset_index(self, preset_index: int, save_index: bool = True) -> None:
        """Set the current RGB preset index.
        
        Args:
            preset_index: Preset index to set (0-7)
            save_index: Whether to save the index to EEPROM
        """
        cmd_data = struct.pack("<BB", preset_index, save_index)
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_SET_CURRENT_MODE_INDEX, data=cmd_data)
    
    def revert_to_saved_preset(self) -> None:
        """Revert to the saved RGB preset index.
        
        Restores the preset index from EEPROM, discarding current changes.
        """
        self.set_current_preset_index(self.get_saved_preset_index(), save_index=True)

    def get_preset(self, preset_index: int) -> Preset:
        """Get RGB preset configuration by index.
        
        Args:
            preset_index: Preset index to retrieve (0-7)
            
        Returns:
            Preset object containing effect configuration
        """
        raw_data = self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_GET_MODE, data=preset_index.to_bytes(1, byteorder="little"))
        preset_index, flags, effect, speed, fixed_hue, startup_animation, hue, sat = struct.unpack("<BBHBBBBB", raw_data[2:11])
        preset = Preset(flags=flags, effect=effect, speed=speed, fixed_hue=fixed_hue, startup_animation=startup_animation, hue=hue, sat=sat)
        return preset
    
    def set_preset(self, preset_index: int, preset: Preset) -> None:
        """Set RGB preset configuration.
        
        Args:
            preset_index: Preset index to set (0-7)
            preset: Preset object with effect configuration
        """
        self._send_check_command(CMD_RPI_COMMAND, RPI_CMD_SET_MODE,
            data=struct.pack("<BBHBBBBB", 
                            preset_index,
                            preset.flags,
                            preset.effect,
                            preset.speed,
                            preset.fixed_hue,
                            preset.startup_animation,
                            preset.hue,
                            preset.sat))
        return

    def set_led_direct_effect(self) -> None:
        """Enable direct LED control mode.
        
        Sets the keyboard to direct LED control mode, allowing individual
        LED colors.
        """
        if self.model == "PI500":
            #raise KeyboardNotCompatibleError("PI500 does not support RGB operations")
            return
        direct_effect = get_vial_effect_id("VIALRGB_EFFECT_DIRECT")
        preset = Preset(effect=direct_effect, speed=255, fixed_hue=True, hue=255, sat=255)
        self.set_temp_effect(preset=preset)

    def get_current_effect(self) -> Preset:
        """Get the current RGB effect configuration.
        
        Returns:
            Preset object representing the current effect
        """
        preset_index = self.get_current_preset_index()
        preset = self.get_preset(preset_index)
        if not preset.fixed_hue:
            preset.hue = self.get_hue()
        return preset

    def get_temp_effect(self) -> Preset:
        """Get the current RGB effect settings.

        Returns:
            Preset object representing the current effect
        """
        preset_index = 7
        preset = self.get_preset(preset_index)
        return preset
    
    def set_temp_effect(self, *, preset: Preset) -> None:
        """Set the current RGB effect settings.

        Args:
            preset: Preset object.
        """
        preset_index = 7
        self.set_preset(preset_index, preset)
        self.set_current_preset_index(preset_index, save_index=False)

    def get_switch_matrix_state(self) -> List[List[bool]]:
        """Get the current state of the switch matrix.

        Returns:
            List of active matrix positions as [row, col] pairs.
        """
        rows = max(switch[0] for switch in self.switch_matrix) + 1
        cols = max(switch[1] for switch in self.switch_matrix) + 1
        raw_data = self._send_check_command(CMD_GET_KEYBOARD_VALUE, KEYBOARD_VALUE_GET_SWITCH_MATRIX_STATE)

        if cols <= 8:
            row_states = list(struct.unpack(f">{rows}B", raw_data[2:2 + rows * 1]))
        elif cols <= 16:
            row_states = list(struct.unpack(f">{rows}H", raw_data[2:2 + rows * 2]))
        elif cols <= 24:
            row_states = []
            chunk_size = 3
            for i in range(rows):
                start = 2 + i * chunk_size
                end = start + chunk_size
                value = int.from_bytes(raw_data[start:end], byteorder='big')
                row_states.append(value)
        else:
            row_states = list(struct.unpack(f">{rows}I", raw_data[2:2 + rows * 4]))

        active = []
        for switch in self.switch_matrix:
            row = switch[0]
            col = switch[1]
            if (row_states[row] & (1 << col)) != 0:
                if self.conversion_switch_matrix is None:
                    position = [row, col]
                else:
                    position = convert_switch_matrix(
                        [row, col], self.switch_matrix, self.conversion_switch_matrix
                    )
                active.append(position)
        return active

    def get_unlock_status(self) -> Tuple[bool, bool, List[List[int]]]:
        """Get the unlock status of the keyboard.

        Returns:
            Tuple of (unlocked, unlock_in_progress, keys).
        """
        raw_data = self._send_command(struct.pack("BB", CMD_VIAL_COMMAND, VIAL_GET_UNLOCK_STATUS))
        unlocked, unlock_in_progress = struct.unpack("<BB", raw_data[0:2])
        keys = []
        for i in range(2, len(raw_data), 2):
            row, col = struct.unpack("<BB", raw_data[i:i + 2])
            if row != 0xFF and col != 0xFF:
                if self.conversion_switch_matrix is None:
                    position = [row, col]
                else:
                    position = convert_switch_matrix(
                        [row, col], self.switch_matrix, self.conversion_switch_matrix
                    )
                keys.append(position)
        return unlocked, unlock_in_progress, keys

    def request_unlock(self) -> None:
        """Start the Vial unlock process."""
        self._send_check_command(CMD_VIAL_COMMAND,VIAL_UNLOCK_START)

    def unlock_poll(self) -> Tuple[bool, bool, int]:
        """Poll the unlock process status.

        Returns:
            Tuple of (unlocked, unlock_in_progress, unlock_counter).
        """
        raw_data = self._send_command(struct.pack("BB", CMD_VIAL_COMMAND, VIAL_UNLOCK_POLL))
        unlocked, unlock_in_progress, unlock_counter = struct.unpack("<BBB", raw_data[0:3])
        return unlocked, unlock_in_progress, unlock_counter

    def lock(self) -> None:
        """Lock the keyboard using Vial protocol."""
        self._send_check_command(CMD_VIAL_COMMAND,VIAL_LOCK)

    def unlock(self, restricted_commands: bool = False) -> None:
        """Unlock the keyboard with visual feedback.

        Args:
            restricted_commands: If True, then do not use keyboard commands other than
            those accepted when an unlock is in progress (i.e. dont control the LEDs)
        """
        use_leds = self.model == "PI500PLUS" and not restricted_commands
        unlocked, unlock_in_progress, keys = self.get_unlock_status()
        if use_leds:
            self.set_led_direct_effect()
        if unlocked:
            print("Keyboard is already unlocked")
            return
        print("Press and hold the unlock keys until the counter reaches 0.")
        print("The unlock keys are:")
        if not restricted_commands and not unlock_in_progress:
            if use_leds:
                self.rgb_clear()
            for key in keys:
                keycode = self.get_keycode(matrix=key, layer=0)
                keycode_name = qmk_keycode_to_key.get(keycode, str(keycode))
                print(f"    Row: {key[0]}, Col: {key[1]} -> Keycode on layer 0: {keycode_name}")
                if use_leds:
                    self.set_led_by_matrix(matrix=key, colour=(255, 255, 255))
            if use_leds:
                self.send_leds()
        else:
            for key in keys:
                print(f"    Row: {key[0]}, Col: {key[1]}")

        self.request_unlock()
        unlocked, unlock_in_progress, keys = self.get_unlock_status()
        last_counter = -1
        while unlock_in_progress:
            unlocked, unlock_in_progress, unlock_counter = self.unlock_poll()
            if unlock_counter != last_counter:
                print(f"Unlock counter: {unlock_counter}")
                last_counter = unlock_counter
            time.sleep(0.1)
        if use_leds:
            self.revert_to_saved_preset()
        unlocked, unlock_in_progress, keys = self.get_unlock_status()
        if unlocked and not unlock_in_progress:
            print("Keyboard is unlocked")
        else:
            print("Something went wrong whilst trying to unlock.")
            if unlock_in_progress:
                raise Exception(
                    "Unlock process is still in progress. "
                    "Nothing can be done until it is complete."
                )
