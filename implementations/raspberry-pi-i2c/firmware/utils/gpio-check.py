#!/usr/bin/env python3
"""
GPIO Button Test Utility

Tests GPIO button input by continuously polling a button pin.
Useful for verifying button wiring and GPIO functionality.

Usage:
    python gpio-check.py

Press Ctrl+C to stop the test.
"""

import board
import digitalio
import time


def main():
    """Main test loop."""
    # Initialize button on GPIO4 (D4)
    button = digitalio.DigitalInOut(board.D4)
    button.direction = digitalio.Direction.INPUT

    print("GPIO Button Test")
    print("Button pin: D4 (GPIO4)")
    print("Press button to see state changes")
    print("Press Ctrl+C to exit\n")

    try:
        last_state = None

        while True:
            current_state = button.value

            # Only print when state changes
            if current_state != last_state:
                if not current_state:
                    print("Button: PRESSED (Low)")
                else:
                    print("Button: RELEASED (High)")
                last_state = current_state

            time.sleep(0.1)  # Poll at 10Hz

    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
