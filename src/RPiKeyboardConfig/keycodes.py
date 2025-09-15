"""QMK keycode mappings and conversion utilities."""

from typing import Dict, List, Optional

qmk_key_to_keycode: Dict[str, int] = {
    "KC_NO": 0x0000,
    "KC_TRANSPARENT": 0x0001,
    "KC_A": 0x0004,
    "KC_B": 0x0005,
    "KC_C": 0x0006,
    "KC_D": 0x0007,
    "KC_E": 0x0008,
    "KC_F": 0x0009,
    "KC_G": 0x000A,
    "KC_H": 0x000B,
    "KC_I": 0x000C,
    "KC_J": 0x000D,
    "KC_K": 0x000E,
    "KC_L": 0x000F,
    "KC_M": 0x0010,
    "KC_N": 0x0011,
    "KC_O": 0x0012,
    "KC_P": 0x0013,
    "KC_Q": 0x0014,
    "KC_R": 0x0015,
    "KC_S": 0x0016,
    "KC_T": 0x0017,
    "KC_U": 0x0018,
    "KC_V": 0x0019,
    "KC_W": 0x001A,
    "KC_X": 0x001B,
    "KC_Y": 0x001C,
    "KC_Z": 0x001D,
    "KC_1": 0x001E,
    "KC_2": 0x001F,
    "KC_3": 0x0020,
    "KC_4": 0x0021,
    "KC_5": 0x0022,
    "KC_6": 0x0023,
    "KC_7": 0x0024,
    "KC_8": 0x0025,
    "KC_9": 0x0026,
    "KC_0": 0x0027,
    "KC_ENTER": 0x0028,
    "KC_ESCAPE": 0x0029,
    "KC_BACKSPACE": 0x002A,
    "KC_TAB": 0x002B,
    "KC_SPACE": 0x002C,
    "KC_MINUS": 0x002D,
    "KC_EQUAL": 0x002E,
    "KC_LEFT_BRACKET": 0x002F,
    "KC_RIGHT_BRACKET": 0x0030,
    "KC_BACKSLASH": 0x0031,
    "KC_NONUS_HASH": 0x0032,
    "KC_SEMICOLON": 0x0033,
    "KC_QUOTE": 0x0034,
    "KC_GRAVE": 0x0035,
    "KC_COMMA": 0x0036,
    "KC_DOT": 0x0037,
    "KC_SLASH": 0x0038,
    "KC_CAPS_LOCK": 0x0039,
    "KC_F1": 0x003A,
    "KC_F2": 0x003B,
    "KC_F3": 0x003C,
    "KC_F4": 0x003D,
    "KC_F5": 0x003E,
    "KC_F6": 0x003F,
    "KC_F7": 0x0040,
    "KC_F8": 0x0041,
    "KC_F9": 0x0042,
    "KC_F10": 0x0043,
    "KC_F11": 0x0044,
    "KC_F12": 0x0045,
    "KC_PRINT_SCREEN": 0x0046,
    "KC_SCROLL_LOCK": 0x0047,
    "KC_PAUSE": 0x0048,
    "KC_INSERT": 0x0049,
    "KC_HOME": 0x004A,
    "KC_PAGE_UP": 0x004B,
    "KC_DELETE": 0x004C,
    "KC_END": 0x004D,
    "KC_PAGE_DOWN": 0x004E,
    "KC_RIGHT": 0x004F,
    "KC_LEFT": 0x0050,
    "KC_DOWN": 0x0051,
    "KC_UP": 0x0052,
    "KC_NUM_LOCK": 0x0053,
    "KC_KP_SLASH": 0x0054,
    "KC_KP_ASTERISK": 0x0055,
    "KC_KP_MINUS": 0x0056,
    "KC_KP_PLUS": 0x0057,
    "KC_KP_ENTER": 0x0058,
    "KC_KP_1": 0x0059,
    "KC_KP_2": 0x005A,
    "KC_KP_3": 0x005B,
    "KC_KP_4": 0x005C,
    "KC_KP_5": 0x005D,
    "KC_KP_6": 0x005E,
    "KC_KP_7": 0x005F,
    "KC_KP_8": 0x0060,
    "KC_KP_9": 0x0061,
    "KC_KP_0": 0x0062,
    "KC_KP_DOT": 0x0063,
    "KC_NONUS_BACKSLASH": 0x0064,
    "KC_APPLICATION": 0x0065,
    "KC_KB_POWER": 0x0066,
    "KC_KP_EQUAL": 0x0067,
    "KC_F13": 0x0068,
    "KC_F14": 0x0069,
    "KC_F15": 0x006A,
    "KC_F16": 0x006B,
    "KC_F17": 0x006C,
    "KC_F18": 0x006D,
    "KC_F19": 0x006E,
    "KC_F20": 0x006F,
    "KC_F21": 0x0070,
    "KC_F22": 0x0071,
    "KC_F23": 0x0072,
    "KC_F24": 0x0073,
    "KC_EXECUTE": 0x0074,
    "KC_HELP": 0x0075,
    "KC_MENU": 0x0076,
    "KC_SELECT": 0x0077,
    "KC_STOP": 0x0078,
    "KC_AGAIN": 0x0079,
    "KC_UNDO": 0x007A,
    "KC_CUT": 0x007B,
    "KC_COPY": 0x007C,
    "KC_PASTE": 0x007D,
    "KC_FIND": 0x007E,
    "KC_KB_MUTE": 0x007F,
    "KC_KB_VOLUME_UP": 0x0080,
    "KC_KB_VOLUME_DOWN": 0x0081,
    "KC_LOCKING_CAPS_LOCK": 0x0082,
    "KC_LOCKING_NUM_LOCK": 0x0083,
    "KC_LOCKING_SCROLL_LOCK": 0x0084,
    "KC_KP_COMMA": 0x0085,
    "KC_KP_EQUAL_AS400": 0x0086,
    "KC_INTERNATIONAL_1": 0x0087,
    "KC_INTERNATIONAL_2": 0x0088,
    "KC_INTERNATIONAL_3": 0x0089,
    "KC_INTERNATIONAL_4": 0x008A,
    "KC_INTERNATIONAL_5": 0x008B,
    "KC_INTERNATIONAL_6": 0x008C,
    "KC_INTERNATIONAL_7": 0x008D,
    "KC_INTERNATIONAL_8": 0x008E,
    "KC_INTERNATIONAL_9": 0x008F,
    "KC_LANGUAGE_1": 0x0090,
    "KC_LANGUAGE_2": 0x0091,
    "KC_LANGUAGE_3": 0x0092,
    "KC_LANGUAGE_4": 0x0093,
    "KC_LANGUAGE_5": 0x0094,
    "KC_LANGUAGE_6": 0x0095,
    "KC_LANGUAGE_7": 0x0096,
    "KC_LANGUAGE_8": 0x0097,
    "KC_LANGUAGE_9": 0x0098,
    "KC_ALTERNATE_ERASE": 0x0099,
    "KC_SYSTEM_REQUEST": 0x009A,
    "KC_CANCEL": 0x009B,
    "KC_CLEAR": 0x009C,
    "KC_PRIOR": 0x009D,
    "KC_RETURN": 0x009E,
    "KC_SEPARATOR": 0x009F,
    "KC_OUT": 0x00A0,
    "KC_OPER": 0x00A1,
    "KC_CLEAR_AGAIN": 0x00A2,
    "KC_CRSEL": 0x00A3,
    "KC_EXSEL": 0x00A4,
    "KC_SYSTEM_POWER": 0x00A5,
    "KC_SYSTEM_SLEEP": 0x00A6,
    "KC_SYSTEM_WAKE": 0x00A7,
    "KC_AUDIO_MUTE": 0x00A8,
    "KC_AUDIO_VOL_UP": 0x00A9,
    "KC_AUDIO_VOL_DOWN": 0x00AA,
    "KC_MEDIA_NEXT_TRACK": 0x00AB,
    "KC_MEDIA_PREV_TRACK": 0x00AC,
    "KC_MEDIA_STOP": 0x00AD,
    "KC_MEDIA_PLAY_PAUSE": 0x00AE,
    "KC_MEDIA_SELECT": 0x00AF,
    "KC_MEDIA_EJECT": 0x00B0,
    "KC_MAIL": 0x00B1,
    "KC_CALCULATOR": 0x00B2,
    "KC_MY_COMPUTER": 0x00B3,
    "KC_WWW_SEARCH": 0x00B4,
    "KC_WWW_HOME": 0x00B5,
    "KC_WWW_BACK": 0x00B6,
    "KC_WWW_FORWARD": 0x00B7,
    "KC_WWW_STOP": 0x00B8,
    "KC_WWW_REFRESH": 0x00B9,
    "KC_WWW_FAVORITES": 0x00BA,
    "KC_MEDIA_FAST_FORWARD": 0x00BB,
    "KC_MEDIA_REWIND": 0x00BC,
    "KC_BRIGHTNESS_UP": 0x00BD,
    "KC_BRIGHTNESS_DOWN": 0x00BE,
    "KC_CONTROL_PANEL": 0x00BF,
    "KC_ASSISTANT": 0x00C0,
    "KC_MISSION_CONTROL": 0x00C1,
    "KC_LAUNCHPAD": 0x00C2,
    "QK_MOUSE_CURSOR_UP": 0x00CD,
    "QK_MOUSE_CURSOR_DOWN": 0x00CE,
    "QK_MOUSE_CURSOR_LEFT": 0x00CF,
    "QK_MOUSE_CURSOR_RIGHT": 0x00D0,
    "QK_MOUSE_BUTTON_1": 0x00D1,
    "QK_MOUSE_BUTTON_2": 0x00D2,
    "QK_MOUSE_BUTTON_3": 0x00D3,
    "QK_MOUSE_BUTTON_4": 0x00D4,
    "QK_MOUSE_BUTTON_5": 0x00D5,
    "QK_MOUSE_BUTTON_6": 0x00D6,
    "QK_MOUSE_BUTTON_7": 0x00D7,
    "QK_MOUSE_BUTTON_8": 0x00D8,
    "QK_MOUSE_WHEEL_UP": 0x00D9,
    "QK_MOUSE_WHEEL_DOWN": 0x00DA,
    "QK_MOUSE_WHEEL_LEFT": 0x00DB,
    "QK_MOUSE_WHEEL_RIGHT": 0x00DC,
    "QK_MOUSE_ACCELERATION_0": 0x00DD,
    "QK_MOUSE_ACCELERATION_1": 0x00DE,
    "QK_MOUSE_ACCELERATION_2": 0x00DF,
    "KC_LEFT_CTRL": 0x00E0,
    "KC_LEFT_SHIFT": 0x00E1,
    "KC_LEFT_ALT": 0x00E2,
    "KC_LEFT_GUI": 0x00E3,
    "KC_RIGHT_CTRL": 0x00E4,
    "KC_RIGHT_SHIFT": 0x00E5,
    "KC_RIGHT_ALT": 0x00E6,
    "KC_RIGHT_GUI": 0x00E7,
    "QK_SWAP_HANDS_TOGGLE": 0x56F0,
    "QK_SWAP_HANDS_TAP_TOGGLE": 0x56F1,
    "QK_SWAP_HANDS_MOMENTARY_ON": 0x56F2,
    "QK_SWAP_HANDS_MOMENTARY_OFF": 0x56F3,
    "QK_SWAP_HANDS_OFF": 0x56F4,
    "QK_SWAP_HANDS_ON": 0x56F5,
    "QK_SWAP_HANDS_ONE_SHOT": 0x56F6,
    "QK_MAGIC_SWAP_CONTROL_CAPS_LOCK": 0x7000,
    "QK_MAGIC_UNSWAP_CONTROL_CAPS_LOCK": 0x7001,
    "QK_MAGIC_TOGGLE_CONTROL_CAPS_LOCK": 0x7002,
    "QK_MAGIC_CAPS_LOCK_AS_CONTROL_OFF": 0x7003,
    "QK_MAGIC_CAPS_LOCK_AS_CONTROL_ON": 0x7004,
    "QK_MAGIC_SWAP_LALT_LGUI": 0x7005,
    "QK_MAGIC_UNSWAP_LALT_LGUI": 0x7006,
    "QK_MAGIC_SWAP_RALT_RGUI": 0x7007,
    "QK_MAGIC_UNSWAP_RALT_RGUI": 0x7008,
    "QK_MAGIC_GUI_ON": 0x7009,
    "QK_MAGIC_GUI_OFF": 0x700A,
    "QK_MAGIC_TOGGLE_GUI": 0x700B,
    "QK_MAGIC_SWAP_GRAVE_ESC": 0x700C,
    "QK_MAGIC_UNSWAP_GRAVE_ESC": 0x700D,
    "QK_MAGIC_SWAP_BACKSLASH_BACKSPACE": 0x700E,
    "QK_MAGIC_UNSWAP_BACKSLASH_BACKSPACE": 0x700F,
    "QK_MAGIC_TOGGLE_BACKSLASH_BACKSPACE": 0x7010,
    "QK_MAGIC_NKRO_ON": 0x7011,
    "QK_MAGIC_NKRO_OFF": 0x7012,
    "QK_MAGIC_TOGGLE_NKRO": 0x7013,
    "QK_MAGIC_SWAP_ALT_GUI": 0x7014,
    "QK_MAGIC_UNSWAP_ALT_GUI": 0x7015,
    "QK_MAGIC_TOGGLE_ALT_GUI": 0x7016,
    "QK_MAGIC_SWAP_LCTL_LGUI": 0x7017,
    "QK_MAGIC_UNSWAP_LCTL_LGUI": 0x7018,
    "QK_MAGIC_SWAP_RCTL_RGUI": 0x7019,
    "QK_MAGIC_UNSWAP_RCTL_RGUI": 0x701A,
    "QK_MAGIC_SWAP_CTL_GUI": 0x701B,
    "QK_MAGIC_UNSWAP_CTL_GUI": 0x701C,
    "QK_MAGIC_TOGGLE_CTL_GUI": 0x701D,
    "QK_MAGIC_EE_HANDS_LEFT": 0x701E,
    "QK_MAGIC_EE_HANDS_RIGHT": 0x701F,
    "QK_MAGIC_SWAP_ESCAPE_CAPS_LOCK": 0x7020,
    "QK_MAGIC_UNSWAP_ESCAPE_CAPS_LOCK": 0x7021,
    "QK_MAGIC_TOGGLE_ESCAPE_CAPS_LOCK": 0x7022,
    "QK_JOYSTICK_BUTTON_0": 0x7400,
    "QK_JOYSTICK_BUTTON_1": 0x7401,
    "QK_JOYSTICK_BUTTON_2": 0x7402,
    "QK_JOYSTICK_BUTTON_3": 0x7403,
    "QK_JOYSTICK_BUTTON_4": 0x7404,
    "QK_JOYSTICK_BUTTON_5": 0x7405,
    "QK_JOYSTICK_BUTTON_6": 0x7406,
    "QK_JOYSTICK_BUTTON_7": 0x7407,
    "QK_JOYSTICK_BUTTON_8": 0x7408,
    "QK_JOYSTICK_BUTTON_9": 0x7409,
    "QK_JOYSTICK_BUTTON_10": 0x740A,
    "QK_JOYSTICK_BUTTON_11": 0x740B,
    "QK_JOYSTICK_BUTTON_12": 0x740C,
    "QK_JOYSTICK_BUTTON_13": 0x740D,
    "QK_JOYSTICK_BUTTON_14": 0x740E,
    "QK_JOYSTICK_BUTTON_15": 0x740F,
    "QK_JOYSTICK_BUTTON_16": 0x7410,
    "QK_JOYSTICK_BUTTON_17": 0x7411,
    "QK_JOYSTICK_BUTTON_18": 0x7412,
    "QK_JOYSTICK_BUTTON_19": 0x7413,
    "QK_JOYSTICK_BUTTON_20": 0x7414,
    "QK_JOYSTICK_BUTTON_21": 0x7415,
    "QK_JOYSTICK_BUTTON_22": 0x7416,
    "QK_JOYSTICK_BUTTON_23": 0x7417,
    "QK_JOYSTICK_BUTTON_24": 0x7418,
    "QK_JOYSTICK_BUTTON_25": 0x7419,
    "QK_JOYSTICK_BUTTON_26": 0x741A,
    "QK_JOYSTICK_BUTTON_27": 0x741B,
    "QK_JOYSTICK_BUTTON_28": 0x741C,
    "QK_JOYSTICK_BUTTON_29": 0x741D,
    "QK_JOYSTICK_BUTTON_30": 0x741E,
    "QK_JOYSTICK_BUTTON_31": 0x741F,
    "QK_PROGRAMMABLE_BUTTON_1": 0x7440,
    "QK_PROGRAMMABLE_BUTTON_2": 0x7441,
    "QK_PROGRAMMABLE_BUTTON_3": 0x7442,
    "QK_PROGRAMMABLE_BUTTON_4": 0x7443,
    "QK_PROGRAMMABLE_BUTTON_5": 0x7444,
    "QK_PROGRAMMABLE_BUTTON_6": 0x7445,
    "QK_PROGRAMMABLE_BUTTON_7": 0x7446,
    "QK_PROGRAMMABLE_BUTTON_8": 0x7447,
    "QK_PROGRAMMABLE_BUTTON_9": 0x7448,
    "QK_PROGRAMMABLE_BUTTON_10": 0x7449,
    "QK_PROGRAMMABLE_BUTTON_11": 0x744A,
    "QK_PROGRAMMABLE_BUTTON_12": 0x744B,
    "QK_PROGRAMMABLE_BUTTON_13": 0x744C,
    "QK_PROGRAMMABLE_BUTTON_14": 0x744D,
    "QK_PROGRAMMABLE_BUTTON_15": 0x744E,
    "QK_PROGRAMMABLE_BUTTON_16": 0x744F,
    "QK_PROGRAMMABLE_BUTTON_17": 0x7450,
    "QK_PROGRAMMABLE_BUTTON_18": 0x7451,
    "QK_PROGRAMMABLE_BUTTON_19": 0x7452,
    "QK_PROGRAMMABLE_BUTTON_20": 0x7453,
    "QK_PROGRAMMABLE_BUTTON_21": 0x7454,
    "QK_PROGRAMMABLE_BUTTON_22": 0x7455,
    "QK_PROGRAMMABLE_BUTTON_23": 0x7456,
    "QK_PROGRAMMABLE_BUTTON_24": 0x7457,
    "QK_PROGRAMMABLE_BUTTON_25": 0x7458,
    "QK_PROGRAMMABLE_BUTTON_26": 0x7459,
    "QK_PROGRAMMABLE_BUTTON_27": 0x745A,
    "QK_PROGRAMMABLE_BUTTON_28": 0x745B,
    "QK_PROGRAMMABLE_BUTTON_29": 0x745C,
    "QK_PROGRAMMABLE_BUTTON_30": 0x745D,
    "QK_PROGRAMMABLE_BUTTON_31": 0x745E,
    "QK_PROGRAMMABLE_BUTTON_32": 0x745F,
    "QK_AUDIO_ON": 0x7480,
    "QK_AUDIO_OFF": 0x7481,
    "QK_AUDIO_TOGGLE": 0x7482,
    "QK_AUDIO_CLICKY_TOGGLE": 0x748A,
    "QK_AUDIO_CLICKY_ON": 0x748B,
    "QK_AUDIO_CLICKY_OFF": 0x748C,
    "QK_AUDIO_CLICKY_UP": 0x748D,
    "QK_AUDIO_CLICKY_DOWN": 0x748E,
    "QK_AUDIO_CLICKY_RESET": 0x748F,
    "QK_MUSIC_ON": 0x7490,
    "QK_MUSIC_OFF": 0x7491,
    "QK_MUSIC_TOGGLE": 0x7492,
    "QK_MUSIC_MODE_NEXT": 0x7493,
    "QK_AUDIO_VOICE_NEXT": 0x7494,
    "QK_AUDIO_VOICE_PREVIOUS": 0x7495,
    "QK_STENO_BOLT": 0x74F0,
    "QK_STENO_GEMINI": 0x74F1,
    "QK_STENO_COMB": 0x74F2,
    "QK_STENO_COMB_MAX": 0x74FC,
    "QK_MACRO_0": 0x7700,
    "QK_MACRO_1": 0x7701,
    "QK_MACRO_2": 0x7702,
    "QK_MACRO_3": 0x7703,
    "QK_MACRO_4": 0x7704,
    "QK_MACRO_5": 0x7705,
    "QK_MACRO_6": 0x7706,
    "QK_MACRO_7": 0x7707,
    "QK_MACRO_8": 0x7708,
    "QK_MACRO_9": 0x7709,
    "QK_MACRO_10": 0x770A,
    "QK_MACRO_11": 0x770B,
    "QK_MACRO_12": 0x770C,
    "QK_MACRO_13": 0x770D,
    "QK_MACRO_14": 0x770E,
    "QK_MACRO_15": 0x770F,
    "QK_MACRO_16": 0x7710,
    "QK_MACRO_17": 0x7711,
    "QK_MACRO_18": 0x7712,
    "QK_MACRO_19": 0x7713,
    "QK_MACRO_20": 0x7714,
    "QK_MACRO_21": 0x7715,
    "QK_MACRO_22": 0x7716,
    "QK_MACRO_23": 0x7717,
    "QK_MACRO_24": 0x7718,
    "QK_MACRO_25": 0x7719,
    "QK_MACRO_26": 0x771A,
    "QK_MACRO_27": 0x771B,
    "QK_MACRO_28": 0x771C,
    "QK_MACRO_29": 0x771D,
    "QK_MACRO_30": 0x771E,
    "QK_MACRO_31": 0x771F,
    "QK_BACKLIGHT_ON": 0x7800,
    "QK_BACKLIGHT_OFF": 0x7801,
    "QK_BACKLIGHT_TOGGLE": 0x7802,
    "QK_BACKLIGHT_DOWN": 0x7803,
    "QK_BACKLIGHT_UP": 0x7804,
    "QK_BACKLIGHT_STEP": 0x7805,
    "QK_BACKLIGHT_TOGGLE_BREATHING": 0x7806,
    "QK_LED_MATRIX_ON": 0x7810,
    "QK_LED_MATRIX_OFF": 0x7811,
    "QK_LED_MATRIX_TOGGLE": 0x7812,
    "QK_LED_MATRIX_MODE_NEXT": 0x7813,
    "QK_LED_MATRIX_MODE_PREVIOUS": 0x7814,
    "QK_LED_MATRIX_BRIGHTNESS_UP": 0x7815,
    "QK_LED_MATRIX_BRIGHTNESS_DOWN": 0x7816,
    "QK_LED_MATRIX_SPEED_UP": 0x7817,
    "QK_LED_MATRIX_SPEED_DOWN": 0x7818,
    "RGB_MODE_PLAIN": 0x782B,
    "RGB_MODE_BREATHE": 0x782C,
    "RGB_MODE_RAINBOW": 0x782D,
    "RGB_MODE_SWIRL": 0x782E,
    "RGB_MODE_SNAKE": 0x782F,
    "RGB_MODE_KNIGHT": 0x7830,
    "RGB_MODE_XMAS": 0x7831,
    "RGB_MODE_GRADIENT": 0x7832,
    "RGB_MODE_RGBTEST": 0x7833,
    "RGB_MODE_TWINKLE": 0x7834,
    "QK_RGB_MATRIX_ON": 0x7840,
    "QK_RGB_MATRIX_OFF": 0x7841,
    "QK_RGB_MATRIX_TOGGLE": 0x7842,
    "QK_RGB_MATRIX_MODE_NEXT": 0x7843,
    "QK_RGB_MATRIX_MODE_PREVIOUS": 0x7844,
    "QK_RGB_MATRIX_HUE_UP": 0x7845,
    "QK_RGB_MATRIX_HUE_DOWN": 0x7846,
    "QK_RGB_MATRIX_SATURATION_UP": 0x7847,
    "QK_RGB_MATRIX_SATURATION_DOWN": 0x7848,
    "QK_RGB_MATRIX_VALUE_UP": 0x7849,
    "QK_RGB_MATRIX_VALUE_DOWN": 0x784A,
    "QK_RGB_MATRIX_SPEED_UP": 0x784B,
    "QK_RGB_MATRIX_SPEED_DOWN": 0x784C,
    "QK_BOOTLOADER": 0x7C00,
    "QK_REBOOT": 0x7C01,
    "QK_DEBUG_TOGGLE": 0x7C02,
    "QK_CLEAR_EEPROM": 0x7C03,
    "QK_MAKE": 0x7C04,
    "QK_AUTO_SHIFT_DOWN": 0x7C10,
    "QK_AUTO_SHIFT_UP": 0x7C11,
    "QK_AUTO_SHIFT_REPORT": 0x7C12,
    "QK_AUTO_SHIFT_ON": 0x7C13,
    "QK_AUTO_SHIFT_OFF": 0x7C14,
    "QK_AUTO_SHIFT_TOGGLE": 0x7C15,
    "QK_GRAVE_ESCAPE": 0x7C16,
    "QK_VELOCIKEY_TOGGLE": 0x7C17,
    "QK_SPACE_CADET_LEFT_CTRL_PARENTHESIS_OPEN": 0x7C18,
    "QK_SPACE_CADET_RIGHT_CTRL_PARENTHESIS_CLOSE": 0x7C19,
    "QK_SPACE_CADET_LEFT_SHIFT_PARENTHESIS_OPEN": 0x7C1A,
    "QK_SPACE_CADET_RIGHT_SHIFT_PARENTHESIS_CLOSE": 0x7C1B,
    "QK_SPACE_CADET_LEFT_ALT_PARENTHESIS_OPEN": 0x7C1C,
    "QK_SPACE_CADET_RIGHT_ALT_PARENTHESIS_CLOSE": 0x7C1D,
    "QK_SPACE_CADET_RIGHT_SHIFT_ENTER": 0x7C1E,
    "QK_UNICODE_MODE_NEXT": 0x7C30,
    "QK_UNICODE_MODE_PREVIOUS": 0x7C31,
    "QK_UNICODE_MODE_MACOS": 0x7C32,
    "QK_UNICODE_MODE_LINUX": 0x7C33,
    "QK_UNICODE_MODE_WINDOWS": 0x7C34,
    "QK_UNICODE_MODE_BSD": 0x7C35,
    "QK_UNICODE_MODE_WINCOMPOSE": 0x7C36,
    "QK_UNICODE_MODE_EMACS": 0x7C37,
    "QK_COMBO_ON": 0x7C50,
    "QK_COMBO_OFF": 0x7C51,
    "QK_COMBO_TOGGLE": 0x7C52,
    "QK_DYNAMIC_MACRO_RECORD_START_1": 0x7C53,
    "QK_DYNAMIC_MACRO_RECORD_START_2": 0x7C54,
    "QK_DYNAMIC_MACRO_RECORD_STOP": 0x7C55,
    "QK_DYNAMIC_MACRO_PLAY_1": 0x7C56,
    "QK_DYNAMIC_MACRO_PLAY_2": 0x7C57,
    "QK_LEADER": 0x7C58,
    "QK_LOCK": 0x7C59,
    "QK_ONE_SHOT_ON": 0x7C5A,
    "QK_ONE_SHOT_OFF": 0x7C5B,
    "QK_ONE_SHOT_TOGGLE": 0x7C5C,
    "QK_KEY_OVERRIDE_TOGGLE": 0x7C5D,
    "QK_KEY_OVERRIDE_ON": 0x7C5E,
    "QK_KEY_OVERRIDE_OFF": 0x7C5F,
    "QK_SECURE_LOCK": 0x7C60,
    "QK_SECURE_UNLOCK": 0x7C61,
    "QK_SECURE_TOGGLE": 0x7C62,
    "QK_SECURE_REQUEST": 0x7C63,
    "QK_DYNAMIC_TAPPING_TERM_PRINT": 0x7C70,
    "QK_DYNAMIC_TAPPING_TERM_UP": 0x7C71,
    "QK_DYNAMIC_TAPPING_TERM_DOWN": 0x7C72,
    "QK_CAPS_WORD_TOGGLE": 0x7C73,
    "QK_AUTOCORRECT_ON": 0x7C74,
    "QK_AUTOCORRECT_OFF": 0x7C75,
    "QK_AUTOCORRECT_TOGGLE": 0x7C76,
    "QK_TRI_LAYER_LOWER": 0x7C77,
    "QK_TRI_LAYER_UPPER": 0x7C78,
    "QK_REPEAT_KEY": 0x7C79,
    "QK_ALT_REPEAT_KEY": 0x7C7A,
    "QK_LAYER_LOCK": 0x7C7B,
    "RPI_RGB_MODE_NEXT": 0x7E00,
    "RPI_RGB_MODE_PREVIOUS": 0x7E01,
    "RPI_RGB_HUE_UP": 0x7E02,
    "RPI_RGB_HUE_DOWN": 0x7E03,
    "RPI_PWR": 0x7E04,
    "QK_KB_5": 0x7E05,
    "QK_KB_6": 0x7E06,
    "QK_KB_7": 0x7E07,
    "QK_KB_8": 0x7E08,
    "QK_KB_9": 0x7E09,
    "QK_KB_10": 0x7E0A,
    "QK_KB_11": 0x7E0B,
    "QK_KB_12": 0x7E0C,
    "QK_KB_13": 0x7E0D,
    "QK_KB_14": 0x7E0E,
    "QK_KB_15": 0x7E0F,
    "QK_KB_16": 0x7E10,
    "QK_KB_17": 0x7E11,
    "QK_KB_18": 0x7E12,
    "QK_KB_19": 0x7E13,
    "QK_KB_20": 0x7E14,
    "QK_KB_21": 0x7E15,
    "QK_KB_22": 0x7E16,
    "QK_KB_23": 0x7E17,
    "QK_KB_24": 0x7E18,
    "QK_KB_25": 0x7E19,
    "QK_KB_26": 0x7E1A,
    "QK_KB_27": 0x7E1B,
    "QK_KB_28": 0x7E1C,
    "QK_KB_29": 0x7E1D,
    "QK_KB_30": 0x7E1E,
    "QK_KB_31": 0x7E1F,
    "QK_USER_0": 0x7E40,
    "QK_USER_1": 0x7E41,
    "QK_USER_2": 0x7E42,
    "QK_USER_3": 0x7E43,
    "QK_USER_4": 0x7E44,
    "QK_USER_5": 0x7E45,
    "QK_USER_6": 0x7E46,
    "QK_USER_7": 0x7E47,
    "QK_USER_8": 0x7E48,
    "QK_USER_9": 0x7E49,
    "QK_USER_10": 0x7E4A,
    "QK_USER_11": 0x7E4B,
    "QK_USER_12": 0x7E4C,
    "QK_USER_13": 0x7E4D,
    "QK_USER_14": 0x7E4E,
    "QK_USER_15": 0x7E4F,
    "QK_USER_16": 0x7E50,
    "QK_USER_17": 0x7E51,
    "QK_USER_18": 0x7E52,
    "QK_USER_19": 0x7E53,
    "QK_USER_20": 0x7E54,
    "QK_USER_21": 0x7E55,
    "QK_USER_22": 0x7E56,
    "QK_USER_23": 0x7E57,
    "QK_USER_24": 0x7E58,
    "QK_USER_25": 0x7E59,
    "QK_USER_26": 0x7E5A,
    "QK_USER_27": 0x7E5B,
    "QK_USER_28": 0x7E5C,
    "QK_USER_29": 0x7E5D,
    "QK_USER_30": 0x7E5E,
    "QK_USER_31": 0x7E5F,
    "QK_TO": 0x5200,
    "QK_MOMENTARY": 0x5220,
    "QK_DEF_LAYER": 0x5240,
    "QK_PERSISTENT_DEF_LAYER": 0x52E0,
    "QK_TOGGLE_LAYER": 0x5260,
    "QK_ONE_SHOT_LAYER": 0x5280,
    "QK_LAYER_TAP_TOGGLE": 0x52C0
}

for x in range(4):
    qmk_key_to_keycode["MO({})".format(x)] = qmk_key_to_keycode["QK_MOMENTARY"] + x
    qmk_key_to_keycode["DF({})".format(x)] = qmk_key_to_keycode["QK_DEF_LAYER"] + x
    qmk_key_to_keycode["TG({})".format(x)] = qmk_key_to_keycode["QK_TOGGLE_LAYER"] + x
    qmk_key_to_keycode["TT({})".format(x)] = qmk_key_to_keycode["QK_LAYER_TAP_TOGGLE"] + x
    qmk_key_to_keycode["OSL({})".format(x)] = qmk_key_to_keycode["QK_ONE_SHOT_LAYER"] + x
    qmk_key_to_keycode["TO({})".format(x)] = qmk_key_to_keycode["QK_TO"] + x
    qmk_key_to_keycode["PDF({})".format(x)] = qmk_key_to_keycode["QK_PERSISTENT_DEF_LAYER"] + x

qmk_keycode_to_key: Dict[int, str] = {v: k for k, v in qmk_key_to_keycode.items()}

def keyboard_ascii_art(model: str, layout: str, keynames: List[str], width: int = 80) -> str:
    """Generate ASCII art representation of keyboard layout.

    Args:
        model: Keyboard model (PI500 or PI500PLUS)
        layout: Keyboard layout (ISO, ANSI, JIS)
        keynames: List of key names for each position

    Returns:
        ASCII art string representation of the keyboard
    """
    k = [name.replace("KC_", "").replace("QK_", "").replace("LEFT_", "")
         .replace("RIGHT_", "").replace("TRANSPARENT", "")
         .replace("AUDIO_", "").replace("NONUS_", "").replace("RPI_RGB_", "")
         .replace("RGB_MATRIX_", "") for name in keynames]
    
    art = "Unsupported model or layout"
    
    if model == "PI500":
        art =  f"""
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬─────────┐
│0,0 │0,1 │0,2 │0,3 │0,4 │0,5 │0,6 │0,7 │0,8 │0,9 │0,10│0,11│0,12│0,14     |
|{k[0]:^4.4}|{k[1]:^4.4}|{k[2]:^4.4}|{k[3]:^4.4}|{k[4]:^4.4}|{k[5]:^4.4}|{k[6]:^4.4}|{k[7]:^4.4}""" + \
f"""|{k[8]:^4.4}|{k[9]:^4.4}|{k[10]:^4.4}|{k[11]:^4.4}|{k[12]:^4.4}|{k[13]:^9.9}|
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼─────────┤
│1,0 │1,1 │1,2 │1,3 │1,4 │1,5 │1,6 │1,7 │1,8 │1,9 │1,10│1,11│1,12│1,14     |
|{k[14]:^4.4}|{k[15]:^4.4}|{k[16]:^4.4}|{k[17]:^4.4}|{k[18]:^4.4}|{k[19]:^4.4}|{k[20]:^4.4}""" + \
f"""|{k[21]:^4.4}|{k[22]:^4.4}|{k[23]:^4.4}|{k[24]:^4.4}|{k[25]:^4.4}|{k[26]:^4.4}|{k[27]:^9.9}|
├────┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬───────┤
│2,0   │2,2 │2,3 │2,4 │2,5 │2,6 │2,7 │2,8 │2,9 │2,10│2,11│2,12│2,13│2,14   │
|{k[28]:^6.6}|{k[29]:^4.4}|{k[30]:^4.4}|{k[31]:^4.4}|{k[32]:^4.4}|{k[33]:^4.4}|{k[34]:^4.4}""" + \
f"""|{k[35]:^4.4}|{k[36]:^4.4}|{k[37]:^4.4}|{k[38]:^4.4}|{k[39]:^4.4}|{k[40]:^4.4}|{k[54]:^7.7}|
├──────┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┐      |
│3,0    │3,2 │3,3 │3,4 │3,5 │3,6 │3,7 │3,8 │3,9 │3,10│3,11│3,12│3,13│      │
|{k[42]:^7.7}|{k[43]:^4.4}|{k[44]:^4.4}|{k[45]:^4.4}|{k[46]:^4.4}|{k[47]:^4.4}|{k[48]:^4.4}""" + \
f"""|{k[49]:^4.4}|{k[50]:^4.4}|{k[51]:^4.4}|{k[52]:^4.4}|{k[53]:^4.4}|{k[79]:^4.4}|      |
├─────┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴────┴──────┤
│4,0  │4,1 │4,2 │4,3 │4,4 │4,5 │4,6 │4,7 │4,8 │4,9 │4,10│4,11│4,14         │
|{k[55]:^5.5}|{k[78]:^4.4}|{k[56]:^4.4}|{k[57]:^4.4}|{k[58]:^4.4}|{k[59]:^4.4}|{k[60]:^4.4}""" + \
f"""|{k[61]:^4.4}|{k[62]:^4.4}|{k[63]:^4.4}|{k[64]:^4.4}|{k[65]:^4.4}|{k[66]:^13.13}|
├────┬┴───┬┴───┬┴───┬┴────┴────┴────┴────┴────┼────┴┬───┴─┬──┴──┬────┬─────┘
│5,0 │5,1 │5,2 │5,3 |5,6                      │5,9  │5,10 │     |5,13|
|{k[67]:^4.4}|{k[68]:^4.4}|{k[69]:^4.4}|{k[70]:^4.4}|{k[71]:^25.25}|{k[72]:^5.5}|""" + \
f"""{k[73]:^5.5}|     |{k[74]:^4.4}|
└────┴────┴────┴────┴─────────────────────────┴─────┴─────┘┌────┼────┼────┐
                                                           |6,12|6,13|6,14|
                                                           |{k[75]:^4.4}|{k[76]:^4.4}|{k[77]:^4.4}|
                                                           └────┴────┴────┘
"""
    if model == "PI500PLUS":
        if layout == "ISO":
            art =  f"""
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│0,0 │0,1 │0,2 │0,3 │0,4 │0,5 │0,6 │0,7 │0,8 │0,9 │0,10│0,11│0,12│0,13│0,14│PWR │
|{k[0]:^4.4}|{k[1]:^4.4}|{k[2]:^4.4}|{k[3]:^4.4}|{k[4]:^4.4}|{k[5]:^4.4}|{k[6]:^4.4}|{k[7]:^4.4}""" + \
f"""|{k[8]:^4.4}|{k[9]:^4.4}|{k[10]:^4.4}|{k[11]:^4.4}|{k[12]:^4.4}|{k[13]:^4.4}|{k[14]:^4.4}|    |
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┴────┼────┤
│1,0 │1,1 │1,2 │1,3 │1,4 │1,5 │1,6 │1,7 │1,8 │1,9 │1,10│1,11│1,12│1,14     │1,15│
|{k[15]:^4.4}|{k[16]:^4.4}|{k[17]:^4.4}|{k[18]:^4.4}|{k[19]:^4.4}|{k[20]:^4.4}|{k[21]:^4.4}""" + \
f"""|{k[22]:^4.4}|{k[23]:^4.4}|{k[24]:^4.4}|{k[25]:^4.4}|{k[26]:^4.4}|{k[27]:^4.4}|{k[28]:^9.9}|{k[29]:^4.4}|
├────┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬───────┼────┤
│2,0   │2,2 │2,3 │2,4 │2,5 │2,6 │2,7 │2,8 │2,9 │2,10│2,11│2,12│2,13│2,14   │2,15│
|{k[30]:^6.6}|{k[31]:^4.4}|{k[32]:^4.4}|{k[33]:^4.4}|{k[34]:^4.4}|{k[35]:^4.4}|{k[36]:^4.4}""" + \
f"""|{k[37]:^4.4}|{k[38]:^4.4}|{k[39]:^4.4}|{k[40]:^4.4}|{k[41]:^4.4}|{k[42]:^4.4}|{k[43]:^7.7}|{k[44]:^4.4}|
├──────┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┐      ├────┤
│3,0    │3,2 │3,3 │3,4 │3,5 │3,6 │3,7 │3,8 │3,9 │3,10│3,11│3,12│3,13│      │3,15│
|{k[45]:^7.7}|{k[46]:^4.4}|{k[47]:^4.4}|{k[48]:^4.4}|{k[49]:^4.4}|{k[50]:^4.4}|{k[51]:^4.4}""" + \
f"""|{k[52]:^4.4}|{k[53]:^4.4}|{k[54]:^4.4}|{k[55]:^4.4}|{k[56]:^4.4}|{k[57]:^4.4}|      |{k[58]:^4.4}|
├─────┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴────┴─┬────┼────┤
│4,0  │4,1 │4,2 │4,3 │4,4 │4,5 │4,6 │4,7 │4,8 │4,9 │4,10│4,11│4,13    │4,14│4,15│
|{k[59]:^5.5}|{k[60]:^4.4}|{k[61]:^4.4}|{k[62]:^4.4}|{k[63]:^4.4}|{k[64]:^4.4}|{k[65]:^4.4}""" + \
f"""|{k[66]:^4.4}|{k[67]:^4.4}|{k[68]:^4.4}|{k[69]:^4.4}|{k[70]:^4.4}|{k[71]:^8.8}|{k[72]:^4.4}|{k[73]:^4.4}|
├─────┼────┴┬───┴─┬──┴────┴────┴────┴────┴────┴───┬┴───┬┴───┬┴───┬────┼────┼────┤
│5,0  │5,1  │5,2  │5,6                            │5,10│5,11│5,12│5,13│5,14│5,15│
|{k[74]:^5.5}|{k[75]:^5.5}|{k[76]:^5.5}|{k[77]:^31.31}|{k[78]:^4.4}|{k[79]:^4.4}|{k[80]:^4.4}""" + \
f"""|{k[81]:^4.4}|{k[82]:^4.4}|{k[83]:^4.4}|
└─────┴─────┴─────┴───────────────────────────────┴────┴────┴────┴────┴────┴────┘
"""
        if layout == "ANSI":
            art =  f"""
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│0,0 │0,1 │0,2 │0,3 │0,4 │0,5 │0,6 │0,7 │0,8 │0,9 │0,10│0,11│0,12│0,13│0,14│PWR │
|{k[0]:^4.4}|{k[1]:^4.4}|{k[2]:^4.4}|{k[3]:^4.4}|{k[4]:^4.4}|{k[5]:^4.4}|{k[6]:^4.4}|{k[7]:^4.4}""" + \
f"""|{k[8]:^4.4}|{k[9]:^4.4}|{k[10]:^4.4}|{k[11]:^4.4}|{k[12]:^4.4}|{k[13]:^4.4}|{k[14]:^4.4}|    |
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┴────┼────┤
│1,0 │1,1 │1,2 │1,3 │1,4 │1,5 │1,6 │1,7 │1,8 │1,9 │1,10│1,11│1,12│1,14     │1,15│
|{k[15]:^4.4}|{k[16]:^4.4}|{k[17]:^4.4}|{k[18]:^4.4}|{k[19]:^4.4}|{k[20]:^4.4}|{k[21]:^4.4}""" + \
f"""|{k[22]:^4.4}|{k[23]:^4.4}|{k[24]:^4.4}|{k[25]:^4.4}|{k[26]:^4.4}|{k[27]:^4.4}|{k[28]:^9.9}|{k[29]:^4.4}|
├────┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬───────┼────┤
│2,0   │2,2 │2,3 │2,4 │2,5 │2,6 │2,7 │2,8 │2,9 │2,10│2,11│2,12│2,13│2,14   │2,15│
|{k[30]:^6.6}|{k[31]:^4.4}|{k[32]:^4.4}|{k[33]:^4.4}|{k[34]:^4.4}|{k[35]:^4.4}|{k[36]:^4.4}""" + \
f"""|{k[37]:^4.4}|{k[38]:^4.4}|{k[39]:^4.4}|{k[40]:^4.4}|{k[41]:^4.4}|{k[42]:^4.4}|{k[43]:^7.7}|{k[44]:^4.4}|
├──────┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴───────┼────┤
│3,0    │3,2 │3,3 │3,4 │3,5 │3,6 │3,7 │3,8 │3,9 │3,10│3,11│3,12│3,13       │3,15│
|{k[45]:^7.7}|{k[46]:^4.4}|{k[47]:^4.4}|{k[48]:^4.4}|{k[49]:^4.4}|{k[50]:^4.4}|{k[51]:^4.4}""" + \
f"""|{k[52]:^4.4}|{k[53]:^4.4}|{k[54]:^4.4}|{k[55]:^4.4}|{k[56]:^4.4}|{k[57]:^11.11}|{k[58]:^4.4}|
├───────┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──────┬────┼────┤
│4,0       │4,2 │4,3 │4,4 │4,5 │4,6 │4,7 │4,8 │4,9 │4,10│4,11│4,13    │4,14│4,15│
|{k[59]:^10.10}|{k[60]:^4.4}|{k[61]:^4.4}|{k[62]:^4.4}|{k[63]:^4.4}|{k[64]:^4.4}|{k[65]:^4.4}""" + \
f"""|{k[66]:^4.4}|{k[67]:^4.4}|{k[68]:^4.4}|{k[69]:^4.4}|{k[70]:^8.8}|{k[71]:^4.4}|{k[72]:^4.4}|
├─────┬────┴┬───┴─┬──┴────┴────┴────┴────┴────┴───┬┴───┬┴───┬┴───┬────┼────┼────┤
│5,0  │5,1  │5,2  │5,6                            │5,10│5,11│5,12│5,13│5,14│5,15│
|{k[73]:^5.5}|{k[74]:^5.5}|{k[75]:^5.5}|{k[76]:^31.31}|{k[77]:^4.4}|{k[78]:^4.4}|{k[79]:^4.4}""" + \
f"""|{k[80]:^4.4}|{k[81]:^4.4}|{k[82]:^4.4}|
└─────┴─────┴─────┴───────────────────────────────┴────┴────┴────┴────┴────┴────┘
"""
        if layout == "JIS":
            art = f"""
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│0,0 │0,1 │0,2 │0,3 │0,4 │0,5 │0,6 │0,7 │0,8 │0,9 │0,10│0,11│0,12│0,13│0,14│PWR │
|{k[0]:^4.4}|{k[1]:^4.4}|{k[2]:^4.4}|{k[3]:^4.4}|{k[4]:^4.4}|{k[5]:^4.4}|{k[6]:^4.4}|{k[7]:^4.4}""" + \
f"""|{k[8]:^4.4}|{k[9]:^4.4}|{k[10]:^4.4}|{k[11]:^4.4}|{k[12]:^4.4}|{k[13]:^4.4}|{k[14]:^4.4}|    |
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
│1,0 │1,1 │1,2 │1,3 │1,4 │1,5 │1,6 │1,7 │1,8 │1,9 │1,10│1,11│1,12│1,13|1,14│1,15│
|{k[15]:^4.4}|{k[16]:^4.4}|{k[17]:^4.4}|{k[18]:^4.4}|{k[19]:^4.4}|{k[20]:^4.4}|{k[21]:^4.4}""" + \
f"""|{k[22]:^4.4}|{k[23]:^4.4}|{k[24]:^4.4}|{k[25]:^4.4}|{k[26]:^4.4}|{k[27]:^4.4}""" + \
f"""|{k[28]:^4.4}|{k[29]:^4.4}|{k[30]:^4.4}|
├────┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴────┼────┤
│2,0   │2,2 │2,3 │2,4 │2,5 │2,6 │2,7 │2,8 │2,9 │2,10│2,11│2,12│2,13│2,14   │2,15│
|{k[31]:^6.6}|{k[32]:^4.4}|{k[33]:^4.4}|{k[34]:^4.4}|{k[35]:^4.4}|{k[36]:^4.4}|{k[37]:^4.4}""" + \
f"""|{k[38]:^4.4}|{k[39]:^4.4}|{k[40]:^4.4}|{k[41]:^4.4}|{k[42]:^4.4}|{k[43]:^4.4}|{k[44]:^7.7}|{k[45]:^4.4}|
├──────┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┐      ├────┤
│3,0    │3,2 │3,3 │3,4 │3,5 │3,6 │3,7 │3,8 │3,9 │3,10│3,11│3,12│3,13│      │3,15│
|{k[46]:^7.7}|{k[47]:^4.4}|{k[48]:^4.4}|{k[49]:^4.4}|{k[50]:^4.4}|{k[51]:^4.4}|{k[52]:^4.4}""" + \
f"""|{k[53]:^4.4}|{k[54]:^4.4}|{k[55]:^4.4}|{k[56]:^4.4}|{k[57]:^4.4}|{k[58]:^4.4}|      |{k[59]:^4.4}|
├───────┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬──┴─┬────┼────┤
│4,0      │4,2 │4,3 │4,4 │4,5 │4,6 │4,7 │4,8 │4,9 │4,10│4,11│4,12|4,13|4,14│4,15│
|{k[60]:^9.9}|{k[61]:^4.4}|{k[62]:^4.4}|{k[63]:^4.4}|{k[64]:^4.4}|{k[65]:^4.4}|{k[66]:^4.4}""" + \
f"""|{k[67]:^4.4}|{k[68]:^4.4}|{k[69]:^4.4}|{k[70]:^4.4}|{k[71]:^4.4}|{k[72]:^4.4}|{k[73]:^4.4}|{k[74]:^4.4}|
├─────┬───┴─┬──┴──┬─┴──┬─┴────┴────┴────┴────┼────┼────┼────┼────┼────┼────┼────┤
│5,0  │5,1  │5,2  │5,3 |5,6                  |5,9 │5,10│5,11│5,12│5,13│5,14│5,15│
|{k[75]:^5.5}|{k[76]:^5.5}|{k[77]:^5.5}|{k[78]:^4.4}|{k[79]:^21.21}|{k[80]:^4.4}|{k[81]:^4.4}""" + \
f"""|{k[82]:^4.4}|{k[83]:^4.4}|{k[84]:^4.4}|{k[85]:^4.4}|{k[86]:^4.4}|
└─────┴─────┴─────┴────┴─────────────────────┴────┴────┴────┴────┴────┴────┴────┘
"""
    # Trim each line of art
    art = "\n".join(line[:width] for line in art.splitlines())
    return art