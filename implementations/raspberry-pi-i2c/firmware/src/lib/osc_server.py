"""
OctoPulse OSC Server

OSC server for receiving haptic feedback commands and routing them to I2C controllers.
"""

import re
from pythonosc import dispatcher
from pythonosc import osc_server
from typing import Optional, Callable
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from .i2c_controller import I2CHapticController


class OctoPulseServer:
    """
    OSC server for OctoPulse haptic feedback system.

    Receives OSC messages in the format:
        /belt_{belt_id}/buzz_{motor_id}
    With optional arguments:
        [duration, pattern]
    """

    def __init__(self, i2c_controller: I2CHapticController,
                 osc_ip: Optional[str] = None,
                 osc_port: Optional[int] = None):
        """
        Initialize OSC server.

        Args:
            i2c_controller: I2C haptic controller instance
            osc_ip: IP address to bind to (default: from config)
            osc_port: Port to listen on (default: from config)
        """
        self.i2c_controller = i2c_controller

        # Use config values if not provided
        self.osc_ip = osc_ip or config.OSC_RECEIVE_IP
        self.osc_port = osc_port or config.OSC_RECEIVE_PORT

        # OSC message pattern for belt/buzzer addressing
        # Matches: /belt_1/buzz_3 or /belt_2/buzz_5 etc.
        self.buzz_pattern = re.compile(r'/belt_(\d+)/buzz_(\d+)')

        # Create OSC dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/belt_*/*", self._buzz_handler)
        self.dispatcher.set_default_handler(self._default_handler)

        # Create OSC server (will be set in start())
        self.server: Optional[osc_server.ThreadingOSCUDPServer] = None

        print(f"OctoPulse OSC Server initialized")
        print(f"  Listen address: {self.osc_ip}:{self.osc_port}")

    def _default_handler(self, address: str, *args):
        """
        Default handler for unmatched OSC messages.

        Args:
            address: OSC address
            *args: OSC arguments
        """
        if config.VERBOSE_OSC:
            print(f"OSC: {address} {args}")

    def _buzz_handler(self, address: str, *args):
        """
        Handle haptic buzzer OSC messages.

        Args:
            address: OSC address (e.g., /belt_1/buzz_3)
            *args: Optional arguments [duration, pattern]
        """
        print(f"OSC Buzz: {address} {args}")

        # Parse belt and buzzer IDs from address
        match = self.buzz_pattern.match(address)
        if not match:
            print(f"Warning: Invalid OSC address format: {address}")
            return

        belt_id = int(match.group(1))
        buzz_id = int(match.group(2))

        # Parse optional arguments
        if len(args) == 0:
            duration = 0.5
            pattern = 118  # Default strong click
        elif len(args) == 1:
            duration = float(args[0])
            pattern = 118
        else:
            duration = float(args[0])
            pattern = int(args[1])

        # Clamp duration to DRV2605L max
        if duration > 1.27:
            print(f"Warning: Duration {duration}s exceeds max 1.27s, clamping")
            duration = 1.27

        # Validate pattern ID (DRV2605L has effects 1-123)
        if pattern < 1 or pattern > 123:
            print(f"Warning: Invalid pattern {pattern}, using default 118")
            pattern = 118

        print(f"  Belt: {belt_id}, Buzz: {buzz_id}, "
              f"Duration: {duration}s, Pattern: {pattern}")

        # Send command to I2C controller
        command = {
            "start": 1,
            "belt": belt_id,
            "buzz": buzz_id,
            "pattern": pattern,
            "duration": duration
        }

        success = self.i2c_controller.send_command(command)
        if not success:
            print(f"Error: Failed to queue command (queue full)")

    def start(self):
        """
        Start the OSC server (blocking).

        This method blocks until the server is stopped with Ctrl+C.
        """
        print(f"\nStarting OctoPulse OSC Server...")
        print(f"Listening on {self.osc_ip}:{self.osc_port}")
        print(f"Press Ctrl+C to stop\n")

        try:
            self.server = osc_server.ThreadingOSCUDPServer(
                (self.osc_ip, self.osc_port),
                self.dispatcher
            )
            print("Server ready")
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\nShutdown requested...")
            self.stop()

        except Exception as e:
            print(f"Server error: {e}")
            self.stop()
            raise

    def stop(self):
        """
        Stop the OSC server.
        """
        print("Stopping OSC server...")
        if self.server:
            self.server.shutdown()
            self.server = None
        print("Server stopped")
