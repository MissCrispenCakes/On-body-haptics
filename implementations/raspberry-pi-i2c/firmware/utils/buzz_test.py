#!/usr/bin/env python3
"""
Haptic Motor Test Utility

Tests all haptic motors by playing a single effect on each channel sequentially.
Useful for verifying I2C connections and motor functionality.

Usage:
    python buzz_test.py

Press Ctrl+C to stop the test.
"""

import time
import board
import busio
import adafruit_drv2605
import adafruit_tca9548a
from signal import signal, SIGINT
from sys import exit


drv = []


def handler(signal_received, frame):
    """Cleanup handler for graceful shutdown."""
    print("\nStopping all motors...")
    for i in range(8):
        drv[i].stop()
    print("Exiting")
    exit(0)


def main():
    """Main test loop."""
    global drv

    # Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize I2C multiplexer
    print("Initializing I2C multiplexer (TCA9548A)")
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # Initialize all DRV2605L drivers
    for i in range(8):
        print(f"Initializing driver {i}")
        drv.append(adafruit_drv2605.DRV2605(tca[i]))
        drv[i].use_LRM()  # Use Linear Resonant Actuator mode

    # Register signal handler for Ctrl+C
    signal(SIGINT, handler)

    # Test configuration
    # See DRV2605L datasheet table 11.2 for effect IDs (1-123):
    # http://www.ti.com/lit/ds/symlink/drv2605.pdf
    effect_id = 118  # Strong click (1kHz)

    print(f"\nTesting effect #{effect_id} on all channels")
    print("Press Ctrl+C to stop\n")

    # Test loop - cycle through all channels
    while True:
        for i in range(8):
            print(f"Channel {i}: Playing effect {effect_id}")
            drv[i].sequence[0] = adafruit_drv2605.Effect(effect_id)
            drv[i].sequence[1] = adafruit_drv2605.Pause(1)
            drv[i].play()
            time.sleep(1)
            drv[i].stop()


if __name__ == "__main__":
    main()
