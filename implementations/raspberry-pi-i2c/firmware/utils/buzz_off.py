#!/usr/bin/env python3
"""
Stop All Motors Utility

Stops all haptic motors immediately by sending stop commands to all DRV2605L drivers.
Useful for emergency stop or cleanup after testing.

Usage:
    python buzz_off.py
"""

import time
import board
import busio
import adafruit_drv2605
import adafruit_tca9548a


def main():
    """Stop all haptic motors."""
    print("Stopping all haptic motors...")

    # Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize I2C multiplexer
    print("Initializing I2C multiplexer (TCA9548A)")
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # Initialize drivers
    drv = []
    for i in range(8):
        print(f"Initializing driver {i}")
        drv.append(adafruit_drv2605.DRV2605(tca[i]))
        drv[i].use_LRM()

    # Stop all motors
    print("\nStopping all channels...")
    for i in range(8):
        print(f"Stopping channel {i}")
        drv[i].stop()

    print("\nAll motors stopped")


if __name__ == "__main__":
    main()
