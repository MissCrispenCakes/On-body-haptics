"""
On-Body Haptics - Raspberry Pi Configuration

Configuration settings for the Octopulse haptic server.
Copy this file to config_local.py and customize for your setup.
"""

# ============================================
# OSC CONFIGURATION
# ============================================
OSC_RECEIVE_IP = "0.0.0.0"  # Bind to all interfaces
OSC_RECEIVE_PORT = 9999      # Port to receive OSC messages
OSC_SEND_PORT = 3333         # Port to send OSC responses (if needed)

# ============================================
# I2C CONFIGURATION
# ============================================
# I2C bus number (usually 1 on Raspberry Pi)
I2C_BUS = 1

# TCA9548A I2C Multiplexer address
I2C_MULTIPLEXER_ADDRESS = 0x70

# DRV2605L Haptic Driver address (same on all channels)
DRV2605_ADDRESS = 0x5A

# Number of haptic channels
NUM_CHANNELS = 8

# I2C speed (Hz) - default is 100000 (100kHz)
# Can be increased to 400000 (400kHz) for faster communication
I2C_SPEED = 100000

# ============================================
# DRV2605L CONFIGURATION
# ============================================
# Library selection (1-6)
# 1: ERM (Eccentric Rotating Mass)
# 2: LRA (Linear Resonant Actuator)
DRV2605_LIBRARY = 2  # LRA by default

# Rated voltage (0-255, typically 100-120 for LRAs)
DRV2605_RATED_VOLTAGE = 100

# Overdrive voltage (0-255, typically 150-200 for LRAs)
DRV2605_OVERDRIVE_VOLTAGE = 150

# ============================================
# OLED DISPLAY CONFIGURATION
# ============================================
OLED_ENABLED = True
OLED_I2C_ADDRESS = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 32

# Button GPIO pin (BCM numbering) for display control
BUTTON_PIN = 17
BUTTON_BOUNCE_TIME = 200  # milliseconds

# ============================================
# GPIO CONFIGURATION
# ============================================
# Use BCM pin numbering
GPIO_MODE = "BCM"  # or "BOARD"

# Optional: Additional GPIO pins for status LEDs, etc.
# STATUS_LED_PIN = 18
# ERROR_LED_PIN = 23

# ============================================
# THREADING & PERFORMANCE
# ============================================
# Command queue size
COMMAND_QUEUE_SIZE = 100

# I2C thread sleep time (seconds)
I2C_THREAD_SLEEP = 0.01  # 10ms

# Enable thread debugging
THREAD_DEBUG = False

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = False
LOG_FILE_PATH = "/var/log/octopulse/server.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================
# NETWORK CONFIGURATION
# ============================================
# Preferred network interface for IP display
# Leave empty to auto-detect, or specify: "wlan0", "eth0", etc.
PREFERRED_NETWORK_INTERFACE = ""

# Hostname (for mDNS/Avahi)
HOSTNAME = "octopulse"

# ============================================
# SYSTEMD SERVICE CONFIGURATION
# ============================================
# Auto-start on boot (configured in systemd service file)
SERVICE_NAME = "octopulse-server"
SERVICE_USER = "pi"
SERVICE_WORKING_DIR = "/home/pi/On-body-haptics/implementations/raspberry-pi-i2c/firmware"

# ============================================
# DEVELOPMENT & DEBUGGING
# ============================================
DEBUG_MODE = False
VERBOSE_OSC = False  # Print all incoming OSC messages
SIMULATE_HARDWARE = False  # For testing without actual hardware

# ============================================
# SAFETY & LIMITS
# ============================================
# Maximum effect duration (milliseconds)
MAX_EFFECT_DURATION = 5000

# Minimum time between effects (milliseconds) to prevent overheating
MIN_EFFECT_INTERVAL = 10

# Enable thermal protection (reduce intensity if too frequent)
THERMAL_PROTECTION = True

# ============================================
# EFFECT LIBRARY
# ============================================
# DRV2605L has 120+ effects (1-123)
# Common effects:
EFFECT_STRONG_CLICK = 14
EFFECT_SHARP_CLICK = 15
EFFECT_SOFT_BUMP = 18
EFFECT_DOUBLE_CLICK = 20
EFFECT_TRIPLE_CLICK = 30
EFFECT_PULSING = 33

# Custom effect mappings (optional)
CUSTOM_EFFECTS = {
    "click": 14,
    "sharp": 15,
    "soft": 18,
    "double": 20,
    "triple": 30,
    "pulse": 33,
}

# ============================================
# LOAD LOCAL OVERRIDES
# ============================================
# Import local configuration if it exists
try:
    from config_local import *
except ImportError:
    pass  # No local config, use defaults
