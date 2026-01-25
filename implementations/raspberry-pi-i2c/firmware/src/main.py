#!/usr/bin/env python3
"""
OctoPulse Haptic Server - Main Entry Point

Raspberry Pi I2C haptic feedback server with OSC control.
"""

import sys
import signal
from lib import I2CHapticController, OctoPulseServer
import config


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print('\nShutdown signal received')
    sys.exit(0)


def main():
    """
    Main entry point for OctoPulse haptic server.
    """
    print("=" * 60)
    print("OctoPulse Haptic Server v2.0")
    print("Raspberry Pi I2C Implementation")
    print("=" * 60)
    print()

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize I2C haptic controller
    print("Initializing I2C haptic controller...")
    try:
        i2c_controller = I2CHapticController(
            num_channels=config.NUM_CHANNELS,
            use_lra=(config.DRV2605_LIBRARY == 2),
            queue_size=config.COMMAND_QUEUE_SIZE
        )
        i2c_controller.start()
        print("I2C controller started")
        print()

    except Exception as e:
        print(f"FATAL: Failed to initialize I2C controller: {e}")
        print("Check hardware connections and permissions")
        sys.exit(1)

    # Initialize OSC server
    print("Initializing OSC server...")
    try:
        osc_server = OctoPulseServer(
            i2c_controller=i2c_controller,
            osc_ip=config.OSC_RECEIVE_IP,
            osc_port=config.OSC_RECEIVE_PORT
        )
        print("OSC server initialized")
        print()

    except Exception as e:
        print(f"FATAL: Failed to initialize OSC server: {e}")
        i2c_controller.stop()
        sys.exit(1)

    # Start OSC server (blocking)
    try:
        osc_server.start()

    except KeyboardInterrupt:
        print("\nShutdown requested")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

    finally:
        # Clean shutdown
        print("\nCleaning up...")
        i2c_controller.stop()
        print("Goodbye!")


if __name__ == "__main__":
    main()
