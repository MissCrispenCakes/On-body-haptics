"""
OLED Display Manager

Manages SSD1306 OLED display for showing IP address and system status.
Displays information when button is pressed.
"""

import threading
import netifaces
from typing import Optional

try:
    import board
    import digitalio
    import busio
    import adafruit_ssd1306
except ImportError:
    # Hardware modules not available (e.g., in CI environment)
    board = None
    digitalio = None
    busio = None
    adafruit_ssd1306 = None


class OLEDDisplay(threading.Thread):
    """
    Thread-safe OLED display manager.

    Monitors a button and displays IP/MAC information when pressed.
    """

    STATE_IDLE = 0
    STATE_SHOWING = 1

    def __init__(self, button_pin=board.D26, display_time: float = 10.0,
                 width: int = 128, height: int = 32, name: str = "OLED-Display"):
        """
        Initialize OLED display manager.

        Args:
            button_pin: GPIO pin for button (default: D26/GPIO26)
            display_time: How long to show info after button press (seconds)
            width: Display width in pixels
            height: Display height in pixels
            name: Thread name for debugging
        """
        super(OLEDDisplay, self).__init__(name=name)
        self.setDaemon(True)

        self.display_time = display_time
        self._running = True
        self.state = self.STATE_IDLE

        # Initialize button
        self.button = digitalio.DigitalInOut(button_pin)
        self.button.direction = digitalio.Direction.INPUT

        # Initialize I2C and display
        print(f"{name}: Initializing I2C and display")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.display = adafruit_ssd1306.SSD1306_I2C(width, height, self.i2c)

        # Event for clearing display after timeout
        self.clear_event = threading.Event()  # FIXED: was threading.event() - lowercase

        print(f"{name}: Initialization complete")

    def show_ip(self):
        """
        Display IP address and MAC address on OLED.
        """
        self.display.fill(0)
        self.display.text("OctoPulse", 0, 2, 1)

        # Find wireless interface IP and MAC
        wl_ip = "Not connected"
        wl_mac = ""

        for ifacename in netifaces.interfaces():
            # Check wireless interfaces (wlan0, wlp*, etc.)
            if not (ifacename.startswith('wl') or ifacename.startswith('wlan')):
                continue

            addrs = netifaces.ifaddresses(ifacename)

            if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
                ips = [addr['addr'] for addr in addrs[netifaces.AF_INET]]

                for ip in ips:
                    if not ip.startswith('127.'):
                        wl_ip = ip
                        wl_mac = addrs[netifaces.AF_LINK][0]['addr']
                        break

        print(f"{self.name}: IP={wl_ip}, MAC={wl_mac}")

        # Display on OLED
        self.display.text(f"IP: {wl_ip}", 0, 12, 1)
        if wl_mac:
            self.display.text(f"MAC: {wl_mac}", 0, 22, 1)

        self.display.show()

    def clear_display(self):
        """
        Clear the OLED display.
        """
        self.display.fill(0)
        self.display.show()

    def schedule_clear(self):
        """
        Set the clear event (called by timer).
        """
        self.clear_event.set()

    def run(self):
        """
        Main thread loop - monitors button and manages display.
        """
        print(f"{self.name}: Thread started")

        while self._running:
            try:
                # Check if we're idle and button is pressed
                if self.state == self.STATE_IDLE:
                    if not self.button.value:  # Button pressed (active low)
                        # Show IP and schedule clear
                        self.state = self.STATE_SHOWING
                        self.show_ip()

                        # Start timer to clear display
                        timer = threading.Timer(self.display_time, self.schedule_clear)
                        timer.start()

                # Check if it's time to clear the display
                if self.clear_event.is_set():
                    self.clear_display()
                    self.clear_event.clear()
                    self.state = self.STATE_IDLE

            except Exception as e:
                print(f"{self.name}: Error: {e}")

        print(f"{self.name}: Thread stopping")

    def stop(self):
        """
        Stop the display thread and clear the display.
        """
        print(f"{self.name}: Stopping")
        self._running = False
        self.clear_display()
