# Arduino + Bluetooth Implementation

Portable haptic feedback system using Arduino microcontrollers, Bluetooth communication (HC-05/HC-06), and a Node.js OSC bridge.

## Overview

- **Hardware**: Arduino Uno/Nano with HC-05/HC-06 Bluetooth module
- **Haptic Channels**: 5 per belt, supports up to 6 belts
- **Communication**: Bluetooth serial (RFCOMM)
- **OSC Bridge**: Node.js server with clean library architecture
- **Cost**: ~$50 per belt

## Features

- Wireless control via Bluetooth
- OSC regex pattern matching for multi-belt addressing
- Pre-programmed patterns (CW, CCW, PULSE, custom 1-7)
- WebSocket bridge for web applications
- VR/3D interaction examples (Three.js)
- Configuration-driven setup (JSON)
- Clean modular library architecture

## System Architecture

```
OSC Client → OSC Server (Node.js) → Bluetooth Bridge (Python) → Arduino → Haptic Motors
```

## Directory Structure

```
arduino-bluetooth/
├── firmware/              # Arduino firmware
│   └── AudioHaptics/     # Main sketch (.ino file)
├── server/               # Node.js OSC bridge
│   ├── src/
│   │   ├── lib/          # Core library code
│   │   │   ├── haptic-server.js    # OSC server implementation
│   │   │   └── config-loader.js    # Configuration management
│   │   ├── index.js               # Main entry point
│   │   └── bluetooth-bridge.py    # Bluetooth communication script
│   ├── examples/         # Sample implementations
│   │   ├── send-pattern.js         # Basic OSC sender
│   │   ├── websocket-server.js     # WebSocket bridge
│   │   └── threejs-vr-client.js    # VR integration example
│   ├── config/          # Configuration files
│   │   ├── default.json           # Main configuration
│   │   └── example.json           # Configuration template
│   └── package.json     # Node.js dependencies
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## Quick Start

See the [Arduino Quick Start Guide](../../docs/getting-started/arduino-quickstart.md) for detailed setup instructions.

### 1. Install Dependencies

```bash
cd implementations/arduino-bluetooth/server
npm install

# Python Bluetooth bridge dependencies
pip install -r ../requirements.txt
```

### 2. Flash Firmware

1. Open `firmware/AudioHaptics/AudioHaptics.ino` in Arduino IDE
2. Configure pin numbers if needed
3. Upload to Arduino

### 3. Configure Server

Edit `server/config/default.json`:

```json
{
  "bluetooth": {
    "devices": [
      {
        "id": 1,
        "mac": "98:D3:31:F0:5A:26",  // Replace with your HC-05 MAC
        "name": "HC-05-Belt-1"
      }
    ]
  },
  "osc": {
    "receivePort": 9998,
    "address": "0.0.0.0"
  }
}
```

### 4. Run Server

```bash
npm start
```

Or with custom host/port:

```bash
node src/index.js 192.168.1.100 9998
```

### 5. Send Test Pattern

```bash
npm run test
```

## Usage

### Starting the Server

**Default configuration:**
```bash
npm start
```

**Custom configuration:**
```bash
node src/index.js [host] [port]
```

### Sending OSC Messages

**Buzzer control (individual motor):**
```
/belt_1/buzzer_3/frequency
Arguments: [repetitions, frequency]
```

**Pattern control (pre-programmed sequence):**
```
/belt_1/pattern_2/frequency
Arguments: [repetitions, frequency]
```

**Belt addressing:**
- `belt_1` to `belt_5`: Individual belts
- `belt_6`: Broadcast to all configured belts

**Example with python-osc:**
```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("192.168.1.100", 9998)

# Belt 1, buzzer 3, 5 repetitions, 100 frequency
client.send_message("/belt_1/buzzer_3/frequency", [5, 100])

# Belt 2, pattern 1, 3 repetitions, 75 frequency
client.send_message("/belt_2/pattern_1/frequency", [3, 75])

# All belts, pattern 2
client.send_message("/belt_6/pattern_2/frequency", [2, 50])
```

**Example with Max/MSP:**
```
udpsend connect 192.168.1.100 9998
sendtyped /belt_1/pattern_1/frequency ii 3 75
```

## Examples

See the [examples/](server/examples/) directory for sample code:

- **send-pattern.js** - Basic OSC pattern sender for testing
- **websocket-server.js** - WebSocket to OSC bridge for web apps
- **threejs-vr-client.js** - VR head tracking integration

Run examples:
```bash
npm run example:pattern
npm run example:websocket
```

## Configuration

### Bluetooth Devices

Configure multiple belts by adding devices to `config/default.json`:

```json
"bluetooth": {
  "devices": [
    {
      "id": 1,
      "mac": "98:D3:31:F0:5A:26",
      "name": "HC-05-Belt-1",
      "autoReconnect": true
    },
    {
      "id": 2,
      "mac": "98:D3:31:F0:5A:27",
      "name": "HC-05-Belt-2",
      "autoReconnect": true
    }
  ]
}
```

### OSC Settings

```json
"osc": {
  "receivePort": 9998,
  "sendPort": 3333,
  "address": "0.0.0.0"
}
```

### Pre-programmed Patterns

Patterns are defined in the Arduino firmware:
- Pattern 1: Clockwise rotation
- Pattern 2: Counter-clockwise rotation
- Pattern 3: Pulse all motors
- Pattern 4: Custom pattern (user-defined)

## Hardware Assembly

See the [Hardware Assembly Guide](../../docs/hardware/assembly-guide.md) for:
- Wiring diagrams
- Component list and sourcing
- Assembly instructions
- Troubleshooting

## Troubleshooting

### Bluetooth Connection Issues

**Problem:** Cannot connect to Bluetooth device

**Solutions:**

```bash
# Linux: Check Bluetooth status
sudo systemctl status bluetooth

# Pair device
bluetoothctl
> scan on
> pair 98:D3:31:F0:5A:26
> trust 98:D3:31:F0:5A:26

# Check RFCOMM binding
rfcomm bind 0 98:D3:31:F0:5A:26 1
```

**Check configuration:**
1. Verify MAC address in `config/default.json`
2. Ensure Bluetooth module is powered and paired
3. Check Python bluetooth module is installed: `pip install pybluez`

### OSC Not Receiving

**Problem:** Server receives no OSC messages

**Solutions:**
1. Check firewall allows UDP traffic on OSC port
2. Verify client is sending to correct IP and port
3. Test with `npm run test` to confirm server is working
4. Check server console for error messages

### Python Bluetooth Module

**Problem:** `ImportError: No module named bluetooth`

**Solution:**
```bash
pip install pybluez
```

On Linux, you may also need:
```bash
sudo apt-get install bluetooth libbluetooth-dev
```

### Serial Communication

```bash
# Test serial connection
python -m serial.tools.list_ports

# Monitor Arduino output
# Arduino IDE > Tools > Serial Monitor (57600 baud)
```

## Development

### Library Architecture

The server uses a clean modular architecture:

- **Core Library** (`src/lib/`): Reusable OSC server and configuration management
- **Entry Point** (`src/index.js`): Clean entry point using the library
- **Examples** (`examples/`): Sample implementations demonstrating different use cases

### Testing Patterns

```bash
# Send test pattern
npm run test

# Run WebSocket example
npm run example:websocket
```

### Adding Custom Patterns

Edit the Arduino firmware to add custom patterns. Pattern 4 and above can be customized for specific haptic sequences.

## Performance Notes

- **Latency**: Bluetooth typically adds 10-30ms latency
- **Range**: HC-05/HC-06 range is approximately 10 meters
- **Multiple Belts**: Server can handle 6+ belts simultaneously
- **OSC Rate**: Can process 100+ OSC messages per second

## Integration Guides

- [Max/MSP Integration](../../docs/integration/max-msp.md)
- [TouchDesigner Integration](../../docs/integration/touchdesigner.md)
- [Unity VR Integration](../../docs/integration/unity-vr.md)

## API Documentation

- [Arduino API Reference](../../docs/api/arduino-api.md)
- [OSC Protocol Specification](../../docs/api/osc-protocol.md)

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.

## License

MIT License - See [LICENSE](../../LICENSE) for details.
