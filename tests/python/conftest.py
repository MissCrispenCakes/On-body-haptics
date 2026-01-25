"""
Pytest configuration for On-Body Haptics tests
"""

import pytest
import sys
from pathlib import Path

# Add implementations to path for imports
repo_root = Path(__file__).parent.parent.parent
arduino_path = repo_root / "implementations" / "arduino-bluetooth" / "server" / "src"
rpi_path = repo_root / "implementations" / "raspberry-pi-i2c" / "firmware" / "src"

sys.path.insert(0, str(arduino_path))
sys.path.insert(0, str(rpi_path))


@pytest.fixture
def mock_osc_server():
    """Mock OSC server for testing"""
    class MockOSCServer:
        def __init__(self):
            self.messages = []

        def handle_message(self, address, *args):
            self.messages.append((address, args))

    return MockOSCServer()


@pytest.fixture
def sample_patterns():
    """Sample haptic patterns for testing"""
    return {
        "CW": "Clockwise",
        "CCW": "Counter-clockwise",
        "PULSE": "Pulse",
        "WAVE": "Wave",
        "OFF": "Off"
    }


@pytest.fixture
def sample_effects():
    """Sample DRV2605L effect IDs"""
    return {
        "strong_click": 14,
        "sharp_click": 15,
        "soft_bump": 18,
        "double_click": 20,
        "triple_click": 30,
        "pulsing": 33
    }


@pytest.fixture
def arduino_config():
    """Sample Arduino configuration"""
    return {
        "bluetooth": {
            "devices": [
                {
                    "id": 1,
                    "mac": "00:11:22:33:44:55",
                    "name": "Test-Belt-1"
                }
            ]
        },
        "osc": {
            "receivePort": 9999,
            "sendPort": 3333
        }
    }


@pytest.fixture
def raspberry_pi_config():
    """Sample Raspberry Pi configuration"""
    return {
        "OSC_RECEIVE_PORT": 9999,
        "I2C_MULTIPLEXER_ADDRESS": 0x70,
        "DRV2605_ADDRESS": 0x5A,
        "NUM_CHANNELS": 8,
        "OLED_ENABLED": True
    }
