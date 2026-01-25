# OctoPulse Utility Scripts

Diagnostic and testing utilities for the Raspberry Pi I2C haptic system.

## Utilities

### buzz_test.py - Haptic Motor Test

Tests all haptic motors by playing a single effect on each channel sequentially.

**Usage:**
```bash
python buzz_test.py
```

**What it does:**
- Initializes all 8 DRV2605L drivers via I2C multiplexer
- Plays effect #118 (strong click) on each channel in sequence
- Useful for verifying I2C connections and motor functionality

**Press Ctrl+C to stop**

### buzz_off.py - Emergency Stop

Stops all haptic motors immediately.

**Usage:**
```bash
python buzz_off.py
```

**What it does:**
- Sends stop command to all 8 DRV2605L drivers
- Useful for cleanup after testing or emergency stop

### gpio-check.py - Button Test

Tests GPIO button input functionality.

**Usage:**
```bash
python gpio-check.py
```

**What it does:**
- Monitors GPIO4 (D4) button pin
- Prints state changes (pressed/released)
- Useful for verifying button wiring

**Press Ctrl+C to stop**

### ip-display.py - Network Info Display

Displays IP and MAC address on OLED display when button is pressed.

**Usage:**
```bash
python ip-display.py
```

**What it does:**
- Monitors GPIO26 (D26) button
- Shows network info on SSD1306 OLED display when button pressed
- Clears display after 10 seconds
- Can run as systemd service for persistent functionality

**Press Ctrl+C to stop**

## Installation

If you installed via setup.py, these utilities are available as commands:

```bash
octopulse-buzz-test     # Test all motors
octopulse-buzz-off      # Stop all motors
octopulse-gpio-check    # Test button
octopulse-ip-display    # IP display service
```

## Hardware Requirements

All utilities require:
- Raspberry Pi (tested on Pi 3/4)
- I2C enabled (`sudo raspi-config` → Interface Options → I2C)

**buzz_test.py and buzz_off.py:**
- TCA9548A I2C multiplexer
- 8x DRV2605L haptic drivers
- Haptic motors (LRA or ERM)

**gpio-check.py:**
- Button connected to GPIO4 (D4)
- Pull-up/pull-down resistor (or use internal pull-up)

**ip-display.py:**
- SSD1306 OLED display (128x32 or 128x64)
- Button connected to GPIO26 (D26)

## Troubleshooting

**"Could not import adafruit modules"**
```bash
pip install -r ../requirements.txt
```

**"I2C device not found"**
```bash
# Check I2C is enabled
sudo raspi-config

# List I2C devices
sudo i2cdetect -y 1

# TCA9548A should appear at 0x70
# DRV2605L should appear at 0x5A (on each mux channel)
```

**"Permission denied" errors**
```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER

# Or run with sudo (not recommended for production)
sudo python buzz_test.py
```

## Development

These utilities are simple standalone scripts for testing. They can be used as reference for building custom haptic applications.

### Extending

To create custom test patterns:

1. Copy `buzz_test.py` as a template
2. Modify the `effect_id` or add custom sequences
3. See DRV2605L datasheet for all 123 effect IDs

### Effect IDs Reference

Common DRV2605L effects:
- 14: Strong Click (100%)
- 15: Sharp Click (75%)
- 18: Soft Bump
- 20: Double Click
- 30: Triple Click
- 33: Pulsing Strong
- 118: Long Double Sharp Click Strong

Full list: [DRV2605L Datasheet Table 11.2](http://www.ti.com/lit/ds/symlink/drv2605.pdf)

## License

MIT License - See [LICENSE](../../../LICENSE) for details.
