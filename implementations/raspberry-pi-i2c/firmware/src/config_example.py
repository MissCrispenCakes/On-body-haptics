"""
On-Body Haptics - Example Local Configuration

Copy this file to config_local.py and customize for your setup.
config_local.py is in .gitignore and won't be committed.
"""

# Override OSC port if needed
# OSC_RECEIVE_PORT = 9998

# Override number of channels if using fewer than 8
# NUM_CHANNELS = 4

# Enable debugging
# DEBUG_MODE = True
# VERBOSE_OSC = True

# Disable OLED display if not installed
# OLED_ENABLED = False

# Change button pin
# BUTTON_PIN = 27

# Use specific network interface for IP display
# PREFERRED_NETWORK_INTERFACE = "wlan0"

# Adjust DRV2605L settings for your actuators
# DRV2605_RATED_VOLTAGE = 120
# DRV2605_OVERDRIVE_VOLTAGE = 180

# Enable file logging
# LOG_TO_FILE = True
# LOG_FILE_PATH = "/home/pi/octopulse.log"
# LOG_LEVEL = "DEBUG"

# Simulate hardware for testing without actual devices
# SIMULATE_HARDWARE = True
