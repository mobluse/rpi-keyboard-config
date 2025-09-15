"""Flappy Bird game using RGB lights on the keyboard."""

import random
import time
from typing import List, NoReturn, Tuple

from .keyboard import RPiKeyboardConfig


class FlappyBirdGame:
    """Flappy Bird game that runs on the RGB keyboard."""

    def __init__(self) -> None:
        """Initialise the Flappy Bird game."""
        self.keyboard = RPiKeyboardConfig()

        self.NUM_LEDS = self.keyboard.get_number_leds()
        self.ROWS = 6
        self.MAX_COLS = 16

        self.bird_row = 3  # Start in middle row
        self.bird_col = 2  # Fixed column position for bird
        self.gravity = 0.5
        self.jump_strength = -1

        self.pipe_width = 2
        self.pipe_gap = 2
        self.pipe_speed = 1
        self.pipes = []
        self.pipe_spawn_timer = 0
        self.pipe_spawn_interval = 15

        self.score = 0
        self.game_over = False
        self.frame_count = 0

        self.fps = 8

        self.BIRD_COLOUR = (60, 255, 255)
        self.PIPE_COLOUR = (120, 255, 200)
        self.BG_COLOUR = (0, 0, 0)
        self.SCORE_COLOUR = (190, 255, 255)

        unlocked, _unlock_in_progress, _keys = self.keyboard.get_unlock_status()
        if not unlocked:
            print("Keyboard is locked, unlocking...")
            self.keyboard.unlock()

        self.keyboard.set_led_direct_effect()

        print("Flappy Bird initialised! Press SPACE to jump, Q to quit.")

    def draw_bird(self) -> None:
        """Draw the bird at its current position."""
        bird_row = int(self.bird_row)
        try:
            self.keyboard.set_led_by_matrix(
                matrix=[bird_row, self.bird_col], colour=self.BIRD_COLOUR
            )
        except ValueError:
            pass

    def draw_pipe(self, pipe_col: int, gap_center: int) -> None:
        """Draw a pipe with a gap at the specified column.
        
        Args:
            pipe_col: Column position to draw the pipe
            gap_center: Row position of the gap center
        """
        gap_top = gap_center - self.pipe_gap // 2
        gap_bottom = gap_center + self.pipe_gap // 2

        for col_offset in range(self.pipe_width):
            current_col = pipe_col + col_offset
            if current_col >= self.MAX_COLS:
                continue

            for row in range(self.ROWS):
                try:
                    if row < gap_top:
                        self.keyboard.set_led_by_matrix(
                            matrix=[row, current_col], colour=self.PIPE_COLOUR
                        )
                    elif row > gap_bottom:
                        self.keyboard.set_led_by_matrix(
                            matrix=[row, current_col], colour=self.PIPE_COLOUR
                        )
                except ValueError:
                    pass

    def update_bird(self, jump_pressed: bool) -> None:
        """Update bird physics.
        
        Args:
            jump_pressed: True if jump key was pressed
        """
        if jump_pressed and not self.game_over:
            self.bird_row += self.jump_strength

        if not self.game_over:
            self.bird_row += self.gravity

            if self.bird_row < 0 or self.bird_row > self.ROWS - 1:
                self.game_over = True

    def update_pipes(self) -> None:
        """Update pipe positions and spawn new ones.
        
        Moves existing pipes left and spawns new pipes when needed.
        Increments score when pipes are passed.
        """
        if not self.game_over:
            for pipe in self.pipes[:]:
                pipe['col'] -= self.pipe_speed
                if pipe['col'] < -self.pipe_width:
                    self.pipes.remove(pipe)
                    self.score += 1
                    print(f"Score: {self.score}")

            self.pipe_spawn_timer += 1
            if self.pipe_spawn_timer >= self.pipe_spawn_interval:
                self.pipe_spawn_timer = 0
                gap_center = random.randint(1, self.ROWS - 2)
                self.pipes.append({
                    'col': self.MAX_COLS,
                    'gap_center': gap_center
                })

    def check_collisions(self) -> bool:
        """Check if bird collides with pipes.
        
        Returns:
            True if collision detected, False otherwise
        """
        if self.game_over:
            return

        bird_row = int(self.bird_row)

        for pipe in self.pipes:
            pipe_left = pipe['col']
            pipe_right = pipe['col'] + self.pipe_width - 1

            if self.bird_col >= pipe_left and self.bird_col <= pipe_right:
                gap_top = pipe['gap_center'] - self.pipe_gap // 2
                gap_bottom = pipe['gap_center'] + self.pipe_gap // 2

                if bird_row < gap_top or bird_row > gap_bottom:
                    self.game_over = True
                    print(f"Game Over! Final Score: {self.score}")

    def draw_score(self) -> None:
        """Draw score on the top row.
        
        Displays current score as lit LEDs on the top row of the keyboard.
        """
        score_leds = min(self.score, 16)
        for col in range(score_leds):
            try:
                self.keyboard.set_led_by_matrix(matrix=[0, col], colour=self.SCORE_COLOUR)
            except ValueError:
                pass

    def game_over_animation(self) -> None:
        """Flash red when game over. 
        
        Returns (jump_pressed, quit_pressed) if detected during animation.
        """
        jump_detected = False
        quit_detected = False

        for _ in range(3):
            for i in range(self.NUM_LEDS):
                self.keyboard.set_led_by_idx(idx=i, colour=(0, 255, 255))  # Red
            self.keyboard.send_leds()

            # Check for keypresses during the red flash
            j, e = self.responsive_sleep(0.3)
            if j:
                jump_detected = True
            if e:
                quit_detected = True

            self.keyboard.rgb_clear()

            # Check for keypresses during the clear period
            j, e = self.responsive_sleep(0.3)
            if j:
                jump_detected = True
            if e:
                quit_detected = True

        return jump_detected, quit_detected

    def get_input(self) -> Tuple[bool, bool]:
        """Check for key presses.
        
        Returns:
            Tuple of (jump_pressed, quit_pressed) booleans
        """
        active_keys = self.keyboard.get_switch_matrix_state()

        # Check for spacebar at position [5,6]
        spacebar_pressed = [5, 6] in active_keys

        # Check for Q key at position [2,2]
        quit_pressed = [2, 2] in active_keys

        # Also accept any key in bottom row as jump
        jump_pressed = spacebar_pressed or any(key[0] == 5 for key in active_keys)

        return jump_pressed, quit_pressed

    def responsive_sleep(self, duration: float, check_interval: float = 0.01) -> bool:
        """Sleep for the specified duration while checking for keypresses.

        Returns (jump_pressed, quit_pressed) for any keypresses detected during sleep.

        Args:
            duration: Total time to sleep in seconds
            check_interval: How often to check for keypresses in seconds
        """
        start_time = time.time()
        elapsed = 0
        jump_detected = False
        quit_detected = False

        while elapsed < duration:
            # Check for keypresses
            jump_pressed, quit_pressed = self.get_input()

            if jump_pressed:
                jump_detected = True

            if quit_pressed:
                quit_detected = True

            # Sleep for the check interval or remaining time, whichever is shorter
            remaining_time = duration - elapsed
            sleep_time = min(check_interval, remaining_time)
            time.sleep(sleep_time)

            elapsed = time.time() - start_time

        return jump_detected, quit_detected

    def render(self) -> None:
        """Render the game state to the keyboard."""
        for led in range(self.NUM_LEDS):
            self.keyboard.set_led_by_idx(idx=led, colour=(0, 0, 0))

        if not self.game_over:
            self.draw_bird()

            for pipe in self.pipes:
                self.draw_pipe(pipe['col'], pipe['gap_center'])

            self.draw_score()

        self.keyboard.send_leds()

    def reset_game(self) -> None:
        """Reset game state."""
        self.bird_row = 3
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        self.pipe_spawn_timer = 0
        print("Game reset! Press SPACE to jump, Q to quit.")

    def run(self) -> None:
        """Run the main game loop."""
        try:
            jump_pressed = False
            quit_pressed = False
            while True:
                start_time = time.time()

                if jump_pressed:
                    print("Jump pressed")

                if quit_pressed:
                    print("Goodbye!")
                    break

                if self.game_over:
                    # Wait for key to restart - using responsive sleep to catch keypresses
                    jump_pressed, quit_pressed = self.responsive_sleep(0.1)
                    if jump_pressed:
                        self.reset_game()
                    if quit_pressed:
                        print("Goodbye!")
                        break
                    continue

                # Update game state
                self.update_bird(jump_pressed)
                self.update_pipes()
                self.check_collisions()

                # Render
                self.render()

                if self.game_over:
                    # Check for keypresses during game over animation
                    _, animation_quit = self.game_over_animation()
                    if animation_quit:
                        quit_pressed = True  # Will be handled in next iteration
                    self.draw_score()
                    self.keyboard.send_leds()
                    continue

                self.frame_count += 1

                elapsed = time.time() - start_time
                target_frame_time = 1.0 / self.fps

                # Use responsive sleep for the remaining frame time to catch keypresses
                remaining_time = target_frame_time - elapsed
                if remaining_time > 0:
                    jump_pressed, quit_pressed = self.responsive_sleep(remaining_time)
                else:
                    jump_pressed = False
                    quit_pressed = False

        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        finally:
            self.keyboard.rgb_clear()
            self.keyboard.send_leds()
            self.keyboard.revert_to_saved_preset()
            self.keyboard.close()


def main() -> NoReturn:
    """Start the Flappy Bird game."""
    print("Starting Flappy Bird on Keyboard!")
    print("Instructions:")
    print("- Press SPACEBAR (or any bottom row key) to make the bird jump")
    print("- Press Q to quit")
    print("- Avoid the blue pipes!")
    print("- Your score is shown on the top row (purple LEDs)")
    print()

    game = FlappyBirdGame()
    game.run()


if __name__ == "__main__":
    main()
