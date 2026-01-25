"""
I2C Haptic Controller

Manages I2C communication with TCA9548A multiplexer and DRV2605L haptic drivers.
Runs in a separate thread to handle haptic effects asynchronously.
"""

import time
import board
import busio
import threading
import queue
import adafruit_drv2605
import adafruit_tca9548a
from typing import Dict, Optional


class I2CHapticController(threading.Thread):
    """
    Thread-safe controller for I2C haptic motor drivers.

    Manages communication with multiple DRV2605L haptic drivers via
    TCA9548A I2C multiplexer. Processes haptic commands from a queue.
    """

    def __init__(self, num_channels: int = 8, use_lra: bool = True,
                 queue_size: int = 100, name: str = "I2C-Haptic"):
        """
        Initialize I2C haptic controller.

        Args:
            num_channels: Number of haptic channels (default: 8)
            use_lra: Use LRA motors instead of ERM (default: True)
            queue_size: Command queue size (default: 100)
            name: Thread name for debugging
        """
        super(I2CHapticController, self).__init__(name=name)
        self.setDaemon(True)

        self.num_channels = num_channels
        self.use_lra = use_lra
        self._running = True
        self.command_queue = queue.Queue(queue_size)

        print(f"{name}: Initializing I2C bus")
        self.i2c = busio.I2C(board.SCL, board.SDA)

        print(f"{name}: Initializing I2C multiplexer (TCA9548A)")
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)

        print(f"{name}: Initializing {num_channels} DRV2605L drivers")
        self.drivers = []
        for i in range(num_channels):
            print(f"{name}: Channel {i}")
            driver = adafruit_drv2605.DRV2605(self.tca[i])
            if use_lra:
                driver.use_LRM()  # Linear Resonant Actuator
            else:
                driver.use_ERM()  # Eccentric Rotating Mass
            self.drivers.append(driver)

        print(f"{name}: Initialization complete")

    def send_command(self, command: Dict) -> bool:
        """
        Send haptic command to queue.

        Args:
            command: Dictionary with keys:
                - start: 1 to start effect, 0 to stop
                - belt: Belt ID (currently unused, reserved for multi-belt)
                - buzz: Buzzer/motor index (0-7)
                - pattern: DRV2605L effect ID (1-123)
                - duration: Effect duration in seconds

        Returns:
            True if command queued successfully, False if queue full
        """
        try:
            self.command_queue.put_nowait(command)
            return True
        except queue.Full:
            print(f"Warning: Command queue full, dropping command: {command}")
            return False

    def _stop_buzzer(self, buzz_index: int):
        """
        Stop a specific buzzer after timer expires.

        Args:
            buzz_index: Motor index (0-7)
        """
        stop_cmd = {
            "start": 0,
            "belt": 1,
            "buzz": buzz_index,
            "pattern": 0,
            "duration": 0
        }
        self.send_command(stop_cmd)

    def run(self):
        """
        Main thread loop - processes commands from queue.
        """
        print(f"{self.name}: Thread started")

        while self._running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    self._process_command(command)
                else:
                    time.sleep(0.01)  # Small sleep to prevent busy-waiting

            except Exception as e:
                print(f"{self.name}: Error processing command: {e}")

        print(f"{self.name}: Thread stopping")

    def _process_command(self, command: Dict):
        """
        Process a single haptic command.

        Args:
            command: Command dictionary from queue
        """
        buzz_index = command.get('buzz', 0)

        if buzz_index >= self.num_channels:
            print(f"Warning: Invalid buzzer index {buzz_index}, max is {self.num_channels - 1}")
            return

        driver = self.drivers[buzz_index]

        if command.get('start') == 1:
            # Start haptic effect
            pattern = command.get('pattern', 118)
            duration = command.get('duration', 0.5)

            # DRV2605L duration in pause slots (max ~1.27s)
            if duration > 1.27:
                duration = 1.27

            # Set effect sequence
            driver.sequence[0] = adafruit_drv2605.Effect(pattern)
            driver.sequence[1] = adafruit_drv2605.Pause(duration)
            driver.play()

            print(f"Buzz {buzz_index}: Effect {pattern}, Duration {duration}s")

            # Schedule stop after duration
            time.sleep(0.2)  # Small delay for effect to start
            timer = threading.Timer(duration, self._stop_buzzer, [buzz_index])
            timer.start()

        else:
            # Stop haptic effect
            driver.stop()
            print(f"Buzz {buzz_index}: Stopped")

    def stop(self):
        """
        Stop the controller thread and turn off all motors.
        """
        print(f"{self.name}: Stopping all motors")
        self._running = False

        # Turn off all drivers
        for i, driver in enumerate(self.drivers):
            try:
                driver.stop()
            except Exception as e:
                print(f"Error stopping driver {i}: {e}")

    def test_motor(self, motor_index: int, effect_id: int = 118, duration: float = 0.5):
        """
        Test a single motor with specified effect.

        Args:
            motor_index: Motor index (0-7)
            effect_id: DRV2605L effect ID (1-123)
            duration: Duration in seconds
        """
        command = {
            "start": 1,
            "belt": 1,
            "buzz": motor_index,
            "pattern": effect_id,
            "duration": duration
        }
        self.send_command(command)
