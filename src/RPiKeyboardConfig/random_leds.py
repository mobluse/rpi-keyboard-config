"""Randomly turn on and off LEDs on a 500+ keyboard."""

import random
import time
from typing import NoReturn

from .keyboard import RPiKeyboardConfig


def main() -> NoReturn:
    """Run the random LEDs test.
    
    Continuously sets random LEDs to random colors on the keyboard.
    Runs indefinitely until interrupted with Ctrl+C.
    
    Raises:
        KeyboardInterrupt: When user presses Ctrl+C to stop
    """
    print("Starting Random LEDs Test!")
    print("Press Ctrl+C to stop...")
    print()

    keyboard = RPiKeyboardConfig()
    try:
        keyboard.set_led_direct_effect()
        number_of_leds = keyboard.get_number_leds()

        def rand_led_on():
            led_idx = random.randint(0, number_of_leds - 1)
            hue = random.randint(0, 255)
            saturation = 255
            value = 255
            keyboard.set_led_by_idx(idx=led_idx, colour=(hue, saturation, value))

        def rand_led_off():
            led_idx = random.randint(0, number_of_leds - 1)
            keyboard.set_led_by_idx(idx=led_idx, colour=(0, 0, 0))

        # Until 75% the LEDS are on
        print(f"Lighting up {int(number_of_leds * 0.75)} LEDs initially...")
        for _ in range(int(number_of_leds * 0.75)):
            rand_led_on()
            keyboard.send_leds()
            time_delay = random.uniform(0.05, 0.3)
            time.sleep(time_delay)

        print("Running random LED pattern...")
        while True:
            if random.random() < 0.5:
                rand_led_on()
            else:
                rand_led_off()

            keyboard.send_leds()
            time_delay = random.uniform(0.05, 0.3)
            time.sleep(time_delay)

    except KeyboardInterrupt:
        print("\nRandom LEDs test interrupted by user")
    finally:
        keyboard.rgb_clear()
        keyboard.send_leds()
        keyboard.revert_to_saved_preset()
        keyboard.close()
        print("Random LEDs test stopped")


if __name__ == "__main__":
    main()
