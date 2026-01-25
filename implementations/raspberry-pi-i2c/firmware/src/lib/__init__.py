"""
OctoPulse Core Library

Core modules for the Raspberry Pi I2C haptic feedback system.
"""

from .i2c_controller import I2CHapticController
from .oled_display import OLEDDisplay
from .osc_server import OctoPulseServer

__all__ = ['I2CHapticController', 'OLEDDisplay', 'OctoPulseServer']
