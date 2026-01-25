# Arduino + Bluetooth Implementation

Portable haptic feedback system using Arduino microcontrollers, Bluetooth communication, and a Node.js OSC bridge.

## Overview

- **Hardware**: Arduino Uno/Nano with HC-05/HC-06 Bluetooth module
- **Haptic Channels**: 5 per belt, supports up to 6 belts
- **Communication**: Bluetooth serial (HC-05/HC-06)
- **OSC Bridge**: Node.js server with WebSocket support
- **Cost**: ~$50 per belt

## Features

- Wireless control via Bluetooth
- OSC regex pattern matching for multi-belt addressing
- Pre-programmed patterns (CW, CCW, PULSE, custom 1-7)
- WebSocket bridge for web applications
- VR/3D interaction examples

## Quick Start

See the [Arduino Quick Start Guide](../../docs/getting-started/arduino-quickstart.md) for detailed setup instructions.

### 1. Install Dependencies

```bash
cd implementations/arduino-bluetooth/server
npm install

# If using Python Bluetooth bridge
pip install -r ../requirements.txt
```

### 2. Flash Firmware

1. Open `firmware/AudioHaptics/AudioHaptics.ino` in Arduino IDE
2. Configure pin numbers in `firmware/AudioHaptics/config.h`
3. Upload to Arduino

### 3. Configure Server

```bash
cd server
cp config/example.json config/local.json
# Edit config/local.json with your Bluetooth MAC addresses
```

### 4. Run Server

```bash
npm start
```

### 5. Send Haptic Patterns

```bash
# Using example script
npm test

# Or send OSC directly
# Address: localhost:9999
# Message: /onbody/1/pattern CW
```

## Directory Structure

```
arduino-bluetooth/
├── firmware/              # Arduino firmware
│   └── AudioHaptics/     # Main sketch
│       ├── AudioHaptics.ino
│       ├── config.h      # Pin configuration
│       └── patterns.h    # Pattern definitions
├── server/               # Node.js OSC bridge
│   ├── src/
│   │   ├── server.js     # Main OSC server
│   │   ├── client.js     # Client example
│   │   ├── audio-haptics.js
│   │   └── bluetooth-bridge.py
│   ├── config/           # Configuration files
│   ├── examples/         # Example scripts
│   └── package.json
└── requirements.txt      # Python dependencies
```

## Configuration

### Bluetooth MAC Addresses

Edit `server/config/local.json`:

```json
{
  "bluetooth": {
    "devices": [
      {
        "id": 1,
        "mac": "00:11:22:33:44:55",
        "name": "HC-05-Belt-1"
      }
    ]
  },
  "osc": {
    "receivePort": 9999,
    "sendPort": 3333
  },
  "websocket": {
    "port": 8080
  }
}
```

### Arduino Pin Configuration

Edit `firmware/AudioHaptics/config.h`:

```cpp
// Haptic motor pins
#define MOTOR_1_PIN 3
#define MOTOR_2_PIN 5
#define MOTOR_3_PIN 6
#define MOTOR_4_PIN 9
#define MOTOR_5_PIN 10

// Serial baud rate
#define SERIAL_BAUD 57600
```

## OSC Protocol

### Pattern Control

```
/onbody/[belt_id]/pattern [pattern_name]
```

Supported patterns:
- `CW` - Clockwise rotation
- `CCW` - Counter-clockwise rotation
- `PULSE` - Pulse all motors
- `CUSTOM1` through `CUSTOM7` - Custom patterns

### Examples

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("localhost", 9999)

# Belt 1 clockwise
client.send_message("/onbody/1/pattern", "CW")

# Belt 2 pulse
client.send_message("/onbody/2/pattern", "PULSE")

# All belts custom pattern
client.send_message("/onbody/*/pattern", "CUSTOM1")
```

## Hardware Assembly

See the [hardware documentation](../../docs/hardware/assembly-guide.md) for:
- Wiring diagrams
- Component list
- Assembly instructions
- Troubleshooting

## Troubleshooting

### Bluetooth Connection Issues

```bash
# Linux: Check Bluetooth status
sudo systemctl status bluetooth

# Pair device
bluetoothctl
> scan on
> pair 00:11:22:33:44:55
> trust 00:11:22:33:44:55
```

### Serial Communication

```bash
# Test serial connection
python -m serial.tools.list_ports

# Monitor Arduino output
# Arduino IDE > Tools > Serial Monitor (57600 baud)
```

## Development

### Testing Patterns

```bash
# Send test pattern
node examples/send-pattern.js

# Interactive client
node src/client.js
```

### Adding Custom Patterns

Edit `firmware/AudioHaptics/patterns.h`:

```cpp
void customPattern8() {
  // Your pattern here
  digitalWrite(MOTOR_1_PIN, HIGH);
  delay(100);
  digitalWrite(MOTOR_1_PIN, LOW);
}
```

## License

MIT License - see [LICENSE](../../LICENSE)
