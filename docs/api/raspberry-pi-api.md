# Raspberry Pi + I2C API Reference

Complete API documentation for the Raspberry Pi + I2C implementation (OctoPulse).

## Table of Contents

- [Overview](#overview)
- [OSC Message Format](#osc-message-format)
- [Python Library API](#python-library-api)
- [I2C Architecture](#i2c-architecture)
- [Effect Library](#effect-library)
- [Configuration](#configuration)
- [Utilities](#utilities)
- [Examples](#examples)

## Overview

The Raspberry Pi + I2C implementation (OctoPulse) uses:
- **Python OSC Server**: Receives OSC messages via UDP
- **I2C Controller**: Manages TCA9548A multiplexer and DRV2605L drivers
- **OLED Display**: Shows IP address on button press (optional)
- **DRV2605L Drivers**: Control haptic motors with 120+ effects

**Communication Flow:**
```
OSC Client → OSC Server (Python) → I2C Controller → TCA9548A → DRV2605L → Motors
```

## OSC Message Format

### Effect Control

```
/belt_{belt_id}/buzz_{motor_id}
Arguments: [duration, pattern]
```

**Parameters:**
- `belt_id`: Belt number (1 = first belt, reserved for future multi-belt support)
- `motor_id`: Motor/channel number (0-7, maps to TCA9548A channels)
- `duration`: Effect duration in seconds (float, max 1.27s due to DRV2605L limits)
- `pattern`: DRV2605L effect ID (integer, 1-123)

**Examples:**

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Channel 0, 0.5 second duration, effect 118 (strong click)
client.send_message("/belt_1/buzz_0", [0.5, 118])

# Channel 3, 1.0 second, effect 14 (strong click 100%)
client.send_message("/belt_1/buzz_3", [1.0, 14])

# Channel 5, 0.25 second, effect 33 (pulsing)
client.send_message("/belt_1/buzz_5", [0.25, 33])
```

### Duration Limits

Due to DRV2605L hardware limitations:
- **Maximum duration**: 1.27 seconds
- Durations > 1.27s are automatically clamped
- For longer effects, send multiple commands

## Python Library API

### Main Entry Point

Located in `src/main.py`

```python
#!/usr/bin/env python3
from lib import I2CHapticController, OctoPulseServer
import config

# Initialize I2C controller
i2c_controller = I2CHapticController(
    num_channels=config.NUM_CHANNELS,
    use_lra=(config.DRV2605_LIBRARY == 2),
    queue_size=config.COMMAND_QUEUE_SIZE
)
i2c_controller.start()

# Initialize OSC server
osc_server = OctoPulseServer(
    i2c_controller=i2c_controller,
    osc_ip=config.OSC_RECEIVE_IP,
    osc_port=config.OSC_RECEIVE_PORT
)

# Start server (blocking)
osc_server.start()
```

### I2CHapticController Class

Located in `src/lib/i2c_controller.py`

Thread-safe controller for I2C haptic motor drivers.

#### Constructor

```python
from lib import I2CHapticController

controller = I2CHapticController(
    num_channels=8,        # Number of haptic channels
    use_lra=True,          # Use LRA motors (False for ERM)
    queue_size=100,        # Command queue size
    name="I2C-Haptic"      # Thread name
)
```

**Parameters:**
- `num_channels` (int): Number of haptic channels, default 8
- `use_lra` (bool): Use Linear Resonant Actuator mode (True) or Eccentric Rotating Mass mode (False), default True
- `queue_size` (int): Maximum command queue size, default 100
- `name` (str): Thread name for debugging, default "I2C-Haptic"

#### Methods

**`start()`**

Starts the I2C controller thread.

```python
controller.start()
```

**`stop()`**

Stops the controller and turns off all motors.

```python
controller.stop()
```

**`send_command(command)`**

Sends haptic command to queue (non-blocking).

```python
command = {
    "start": 1,           # 1 = start effect, 0 = stop
    "belt": 1,            # Belt ID (reserved for future use)
    "buzz": 3,            # Motor/channel index (0-7)
    "pattern": 118,       # DRV2605L effect ID (1-123)
    "duration": 0.5       # Duration in seconds
}

success = controller.send_command(command)
if not success:
    print("Queue full, command dropped")
```

Returns: `True` if queued successfully, `False` if queue full

**`test_motor(motor_index, effect_id, duration)`**

Tests a single motor with specified effect.

```python
# Test motor 0 with effect 118 for 0.5 seconds
controller.test_motor(0, 118, 0.5)

# Test motor 5 with effect 14 for 1.0 second
controller.test_motor(5, 14, 1.0)
```

#### Attributes

- `num_channels` (int): Number of configured channels
- `drivers` (list): List of DRV2605L driver objects
- `command_queue` (Queue): Thread-safe command queue
- `i2c` (busio.I2C): I2C bus object
- `tca` (TCA9548A): I2C multiplexer object

### OctoPulseServer Class

Located in `src/lib/osc_server.py`

OSC server for receiving and routing haptic commands.

#### Constructor

```python
from lib import OctoPulseServer, I2CHapticController

osc_server = OctoPulseServer(
    i2c_controller=controller,    # I2CHapticController instance
    osc_ip="0.0.0.0",             # IP to bind to
    osc_port=9999                  # OSC port
)
```

**Parameters:**
- `i2c_controller` (I2CHapticController): Required, I2C controller instance
- `osc_ip` (str): IP address to bind OSC server, default from config
- `osc_port` (int): UDP port for OSC messages, default from config

#### Methods

**`start()`**

Starts the OSC server (blocking). This method blocks until Ctrl+C is pressed.

```python
try:
    server.start()
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    controller.stop()
```

**`stop()`**

Stops the OSC server.

```python
server.stop()
```

### OLEDDisplay Class

Located in `src/lib/oled_display.py`

Optional OLED display manager for showing IP address.

#### Constructor

```python
from lib import OLEDDisplay
import board

display = OLEDDisplay(
    button_pin=board.D26,    # GPIO pin for button
    display_time=10.0,       # How long to show info (seconds)
    width=128,               # Display width in pixels
    height=32,               # Display height in pixels
    name="OLED-Display"      # Thread name
)
```

#### Methods

**`start()`**

Starts the display thread.

```python
display.start()
```

**`stop()`**

Stops the display and clears it.

```python
display.stop()
```

**`show_ip()`**

Displays IP address on OLED (called automatically on button press).

**`clear_display()`**

Clears the OLED display.

## I2C Architecture

### Hardware Configuration

```
Raspberry Pi I2C Bus (GPIO 2/3)
    |
TCA9548A I2C Multiplexer (0x70)
    |
    +-- Channel 0 --> DRV2605L (0x5A) --> Motor 0
    +-- Channel 1 --> DRV2605L (0x5A) --> Motor 1
    +-- Channel 2 --> DRV2605L (0x5A) --> Motor 2
    +-- Channel 3 --> DRV2605L (0x5A) --> Motor 3
    +-- Channel 4 --> DRV2605L (0x5A) --> Motor 4
    +-- Channel 5 --> DRV2605L (0x5A) --> Motor 5
    +-- Channel 6 --> DRV2605L (0x5A) --> Motor 6
    +-- Channel 7 --> DRV2605L (0x5A) --> Motor 7
```

### I2C Addresses

- **TCA9548A Multiplexer**: 0x70 (default, configurable)
- **DRV2605L Drivers**: 0x5A (same address on all mux channels)
- **SSD1306 OLED** (optional): 0x3C

### Pin Connections

**I2C Bus:**
- GPIO 2 (SDA): Data line
- GPIO 3 (SCL): Clock line

**Button (optional):**
- GPIO 26 (D26): OLED display button

### Enabling I2C

```bash
sudo raspi-config
# Interface Options > I2C > Enable

# Verify I2C is enabled
ls /dev/i2c-*

# Check devices
sudo i2cdetect -y 1
```

## Effect Library

The DRV2605L provides 123 haptic effects across 6 libraries. OctoPulse uses Library 2 (LRA) by default.

### Common Effects

#### Clicks

| ID | Name | Description |
|----|------|-------------|
| 1 | Strong Click 100% | Sharp, strong tactile click |
| 7 | Soft Fuzz 60% | Gentle fuzzy sensation |
| 10 | Strong Click 60% | Medium strength click |
| 12 | Strong Click 30% | Subtle click |
| 14 | Strong Click 100% | Strongest click available |
| 15 | Sharp Click 100% | Sharp, crisp click |
| 16 | Soft Click 100% | Soft, gentle click |

#### Bumps

| ID | Name | Description |
|----|------|-------------|
| 17 | Medium Bump 100% | Medium strength bump |
| 18 | Soft Bump 100% | Soft, gentle bump |
| 19 | Medium Bump 50% | Medium bump, half strength |

#### Multiple Clicks

| ID | Name | Description |
|----|------|-------------|
| 20 | Double Click 100% | Two strong clicks |
| 21 | Double Click 60% | Two medium clicks |
| 27 | Double Sharp Click 100% | Two sharp clicks |
| 30 | Triple Click 100% | Three strong clicks |
| 31 | Triple Click 60% | Three medium clicks |
| 38 | Triple Sharp Click 100% | Three sharp clicks |

#### Pulses

| ID | Name | Description |
|----|------|-------------|
| 33 | Pulsing Strong 1 (100%) | Strong pulsing pattern |
| 34 | Pulsing Strong 2 (60%) | Medium pulsing pattern |
| 35 | Pulsing Medium 1 (100%) | Medium pulsing |
| 36 | Pulsing Medium 2 (60%) | Gentle pulsing |
| 43 | Long Buzz 100% | Continuous buzz |
| 47 | Buzz 1 100% | Short buzz |

#### Transitions

| ID | Name | Description |
|----|------|-------------|
| 64 | Ramp Up Long Heavy | Slow intensity increase |
| 65 | Ramp Up Medium Heavy | Medium ramp up |
| 66 | Ramp Up Short Heavy | Quick ramp up |
| 70 | Ramp Down Long Heavy | Slow intensity decrease |
| 71 | Ramp Down Medium Heavy | Medium ramp down |
| 72 | Ramp Down Short Heavy | Quick ramp down |

#### Alerts

| ID | Name | Description |
|----|------|-------------|
| 75 | Alert 750ms | Alert pattern, 750ms |
| 76 | Alert 1000ms | Alert pattern, 1 second |
| 77 | Strong Notification 750ms | Strong alert |
| 82 | Pulsing Strong 1 750ms | Pulsing alert |
| 83 | Medium Notification 1000ms | Medium strength alert |

### Complete Effect List

For the complete list of all 123 effects, see:
- [DRV2605L Datasheet Table 11.2](http://www.ti.com/lit/ds/symlink/drv2605.pdf)
- `config.py` CUSTOM_EFFECTS mapping

### Testing Effects

Use the buzz_test.py utility to cycle through effects:

```bash
python utils/buzz_test.py
```

Or test a specific effect:

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Try different effects
for effect_id in [1, 14, 15, 18, 20, 33, 75, 118]:
    client.send_message("/belt_1/buzz_0", [0.5, effect_id])
    time.sleep(1)
```

## Configuration

Located in `src/config.py`

### OSC Configuration

```python
OSC_RECEIVE_IP = "0.0.0.0"  # Bind to all interfaces
OSC_RECEIVE_PORT = 9999      # Port to receive OSC messages
OSC_SEND_PORT = 3333         # Port for responses (optional)
```

### I2C Configuration

```python
I2C_BUS = 1                  # I2C bus number
I2C_MULTIPLEXER_ADDRESS = 0x70  # TCA9548A address
DRV2605_ADDRESS = 0x5A       # DRV2605L address
NUM_CHANNELS = 8             # Number of haptic channels
I2C_SPEED = 100000           # 100kHz (can increase to 400kHz)
```

### DRV2605L Configuration

```python
DRV2605_LIBRARY = 2          # 1=ERM, 2=LRA
DRV2605_RATED_VOLTAGE = 100  # 0-255
DRV2605_OVERDRIVE_VOLTAGE = 150  # 0-255
```

### OLED Display Configuration

```python
OLED_ENABLED = True
OLED_I2C_ADDRESS = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 32
BUTTON_PIN = 17              # GPIO pin (BCM numbering)
```

### Threading & Performance

```python
COMMAND_QUEUE_SIZE = 100     # Command queue size
I2C_THREAD_SLEEP = 0.01      # 10ms thread sleep
THREAD_DEBUG = False         # Enable thread debugging
```

### Logging

```python
LOG_LEVEL = "INFO"           # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = False
LOG_FILE_PATH = "/var/log/octopulse/server.log"
VERBOSE_OSC = False          # Print all OSC messages
```

### Safety Limits

```python
MAX_EFFECT_DURATION = 5000   # Maximum duration (ms)
MIN_EFFECT_INTERVAL = 10     # Minimum time between effects (ms)
THERMAL_PROTECTION = True    # Enable thermal protection
```

### Custom Effects Mapping

```python
CUSTOM_EFFECTS = {
    "click": 14,             # Strong click
    "sharp": 15,             # Sharp click
    "soft": 18,              # Soft bump
    "double": 20,            # Double click
    "triple": 30,            # Triple click
    "pulse": 33,             # Pulsing strong
}
```

### Local Configuration Override

Create `config_local.py` to override default settings:

```python
# config_local.py
OSC_RECEIVE_PORT = 8000
VERBOSE_OSC = True
LOG_LEVEL = "DEBUG"
```

## Utilities

Located in `firmware/utils/`

### buzz_test.py - Motor Test

Tests all motors sequentially.

```bash
python utils/buzz_test.py
```

### buzz_off.py - Emergency Stop

Stops all motors immediately.

```bash
python utils/buzz_off.py
```

### gpio-check.py - Button Test

Tests GPIO button functionality.

```bash
python utils/gpio-check.py
```

### ip-display.py - Network Info Display

Shows IP address on OLED when button pressed.

```bash
python utils/ip-display.py
```

See [utilities README](../../implementations/raspberry-pi-i2c/firmware/utils/README.md) for detailed documentation.

## Examples

### Basic Python Client

```python
from pythonosc import udp_client
import time

# Connect to OctoPulse server
client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Single effect
client.send_message("/belt_1/buzz_0", [0.5, 118])
time.sleep(1)

# Sequence of effects on different channels
for channel in range(8):
    client.send_message(f"/belt_1/buzz_{channel}", [0.3, 14])
    time.sleep(0.4)

# Different effects
effects = [14, 15, 18, 20, 33]
for effect_id in effects:
    client.send_message("/belt_1/buzz_0", [0.5, effect_id])
    time.sleep(1)
```

### Spatial Pattern Example

```python
# Clockwise rotation
channels_cw = [0, 1, 2, 3, 4, 5, 6, 7]
for ch in channels_cw:
    client.send_message(f"/belt_1/buzz_{ch}", [0.2, 14])
    time.sleep(0.15)

# Counter-clockwise
channels_ccw = [7, 6, 5, 4, 3, 2, 1, 0]
for ch in channels_ccw:
    client.send_message(f"/belt_1/buzz_{ch}", [0.2, 14])
    time.sleep(0.15)

# Pulse all
for ch in range(8):
    client.send_message(f"/belt_1/buzz_{ch}", [0.3, 33])
```

### Unity VR Integration

```csharp
using UnityEngine;
using OscCore;

public class OctoPulseController : MonoBehaviour
{
    OscClient client;

    void Start()
    {
        client = new OscClient("192.168.1.100", 9999);
    }

    public void TriggerHaptic(int channel, float duration, int effectId)
    {
        client.Send($"/belt_1/buzz_{channel}", duration, effectId);
    }

    // Trigger on collision
    void OnCollisionEnter(Collision collision)
    {
        TriggerHaptic(0, 0.3f, 14);  // Strong click
    }
}
```

### Max/MSP Patch

```
[udpsend]
|
[connect 192.168.1.100 9999(
|
[pack /belt_1/buzz_0 f i]
|
[0.5 118]  [1.0 14]  [0.3 33]
```

## Troubleshooting

### I2C Not Found

```bash
# Check I2C is enabled
sudo raspi-config

# List I2C devices
sudo i2cdetect -y 1

# Should show:
# - 0x70: TCA9548A multiplexer
# - 0x5A: DRV2605L drivers (on each mux channel)
```

### Permission Denied

```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER

# Logout and login again

# Or run with sudo (not recommended for production)
sudo python src/main.py
```

### Motor Not Responding

1. Check I2C connections (SDA, SCL, GND, power)
2. Verify motor is connected to correct channel
3. Test with buzz_test.py
4. Check motor power supply (adequate current)
5. Verify motor type (LRA vs ERM) matches config

### OSC Messages Not Received

1. Check server is running: `python src/main.py`
2. Verify IP and port: `config.OSC_RECEIVE_PORT`
3. Check firewall: `sudo ufw allow 9999/udp`
4. Test with example: `python utils/send-test.py`

## Performance

**Latency:** 10-30ms total
- Network transmission: 1-10ms
- OSC parsing: 1-5ms
- Python processing: 1-5ms
- I2C communication: 5-10ms
- DRV2605L: 1-5ms

**Throughput:** ~30 effects/second per channel

**I2C Speed:** 100kHz default (can increase to 400kHz in config)

## See Also

- [OSC Protocol Specification](osc-protocol.md)
- [Arduino API Reference](arduino-api.md)
- [Raspberry Pi Quickstart](../getting-started/raspberry-pi-quickstart.md)
- [Hardware Assembly Guide](../hardware/assembly-guide.md)
- [DRV2605L Datasheet](http://www.ti.com/lit/ds/symlink/drv2605.pdf)

## Contributing

Found an issue or want to improve the API? See [CONTRIBUTING.md](../../CONTRIBUTING.md).
