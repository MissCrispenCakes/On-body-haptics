# Arduino + Bluetooth API Reference

Complete API documentation for the Arduino + Bluetooth implementation.

## Table of Contents

- [Overview](#overview)
- [OSC Message Format](#osc-message-format)
- [Node.js Server API](#nodejs-server-api)
- [Serial Protocol](#serial-protocol)
- [Arduino Firmware](#arduino-firmware)
- [Configuration](#configuration)
- [Examples](#examples)

## Overview

The Arduino + Bluetooth implementation uses:
- **Node.js OSC Server**: Receives OSC messages via UDP
- **Bluetooth Bridge**: Python script sends commands via RFCOMM
- **Arduino Firmware**: Controls haptic motors based on serial commands

**Communication Flow:**
```
OSC Client → OSC Server (Node.js) → Bluetooth Bridge (Python) → Arduino → Motors
```

## OSC Message Format

### Buzzer Control (Individual Motor)

```
/belt_{belt_id}/buzzer_{motor_id}/frequency
Arguments: [repetitions, frequency]
```

**Parameters:**
- `belt_id`: Belt number (1-6, where 6 = all belts)
- `motor_id`: Motor/buzzer number (1-5)
- `repetitions`: Number of times to repeat effect (integer)
- `frequency`: Frequency/intensity value (integer)

**Examples:**

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("192.168.1.100", 9998)

# Belt 1, buzzer 3, 5 repetitions, 100 frequency
client.send_message("/belt_1/buzzer_3/frequency", [5, 100])

# Belt 2, buzzer 1, 3 reps, 75 frequency
client.send_message("/belt_2/buzzer_1/frequency", [3, 75])
```

### Pattern Control (Pre-programmed Sequences)

```
/belt_{belt_id}/pattern_{pattern_id}/frequency
Arguments: [repetitions, frequency]
```

**Parameters:**
- `belt_id`: Belt number (1-6, where 6 = all belts)
- `pattern_id`: Pattern number (1-4)
  - Pattern 1: Clockwise rotation (CW)
  - Pattern 2: Counter-clockwise rotation (CCW)
  - Pattern 3: Pulse pattern
  - Pattern 4: Custom pattern
- `repetitions`: Number of times to repeat pattern
- `frequency`: Pattern speed/frequency

**Examples:**

```python
# Belt 1, pattern 1 (CW), 3 repetitions, speed 50
client.send_message("/belt_1/pattern_1/frequency", [3, 50])

# All belts, pattern 2 (CCW), 2 reps, speed 75
client.send_message("/belt_6/pattern_2/frequency", [2, 75])

# Belt 3, pattern 3 (PULSE), 5 reps, speed 100
client.send_message("/belt_3/pattern_3/frequency", [5, 100])
```

### Broadcasting to All Belts

Use `belt_6` to send commands to all configured belts simultaneously:

```python
# Pulse all belts
client.send_message("/belt_6/pattern_3/frequency", [2, 50])

# Activate buzzer 2 on all belts
client.send_message("/belt_6/buzzer_2/frequency", [1, 100])
```

## Node.js Server API

### HapticServer Class

Located in `src/lib/haptic-server.js`

#### Constructor

```javascript
const HapticServer = require('./lib/haptic-server');

const server = new HapticServer({
  host: "0.0.0.0",           // Host to bind to
  port: 9998,                 // OSC port
  configPath: "./config",     // Config directory
  bluetoothScript: "./bluetooth-bridge.py"  // Bluetooth bridge script
});
```

**Options:**
- `host` (string): IP address to bind OSC server (default: from config)
- `port` (number): UDP port for OSC messages (default: from config)
- `configPath` (string): Path to configuration directory
- `bluetoothScript` (string): Path to Bluetooth bridge Python script

#### Methods

**`start()`**

Starts the OSC server (non-blocking).

```javascript
server.start();
```

**`stop()`**

Stops the OSC server gracefully.

```javascript
server.stop();
```

### ConfigLoader Class

Located in `src/lib/config-loader.js`

#### Constructor

```javascript
const ConfigLoader = require('./lib/config-loader');

const config = new ConfigLoader('./config');
```

#### Methods

**`load()`**

Loads configuration from `config/default.json`.

```javascript
const config = loader.load();
```

Returns: Configuration object

**`get(keyPath, defaultValue)`**

Gets configuration value by dot-notation path.

```javascript
const port = loader.get('osc.receivePort', 9998);
const devices = loader.get('bluetooth.devices', []);
```

**`validate()`**

Validates required configuration values. Throws error if validation fails.

```javascript
try {
  loader.validate();
} catch (err) {
  console.error('Invalid configuration:', err.message);
}
```

### Command Line Interface

```bash
# Start with default config
node src/index.js

# Custom host and port
node src/index.js 192.168.1.100 9998

# Or use npm script
npm start
```

## Serial Protocol

### Command Format

Commands sent to Arduino via Bluetooth are 8-character strings:

```
[CommandType][CommandValue][Repetitions][Frequency]
```

**Structure:**
- Position 0: Command Type (1 = buzzer, 2 = pattern)
- Position 1: Command Value (buzzer 1-5 or pattern 1-4)
- Positions 2-3: Repetitions (2 digits, e.g., "05" = 5)
- Positions 4-7: Frequency (4 digits, e.g., "0100" = 100)

**Examples:**

```
"13050100"  → Buzzer 3, 5 reps, frequency 100
"21030075"  → Pattern 1, 3 reps, frequency 75
"24020050"  → Pattern 4, 2 reps, frequency 50
```

### Bluetooth Bridge Script

Located at `src/bluetooth-bridge.py`

**Usage:**
```bash
python bluetooth-bridge.py <mac_address> <command>
```

**Example:**
```bash
python bluetooth-bridge.py 98:D3:31:F0:5A:26 13050100
```

**Python API:**

```python
import bluetooth

def send_command(mac_address, command):
    """Send command to Arduino via Bluetooth."""
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((mac_address, 1))
    sock.send(command)
    sock.close()
```

## Arduino Firmware

### Pin Configuration

Default pin mapping (PWM pins):

```cpp
int LEDPins[] = { 5, 6, 9, 10, 11 };

int FrontLeft = 5;
int FrontRight = 11;
int SideLeft = 6;
int SideRight = 10;
int Center = 9;
```

**Hardware Connections:**
- Pin 5: Front Left motor
- Pin 6: Side Left motor
- Pin 9: Center motor
- Pin 10: Side Right motor
- Pin 11: Front Right motor
- Pin 17/16: Bluetooth RX/TX (SoftwareSerial)

### Pre-programmed Patterns

#### Pattern 1: Clockwise (CW)

Activates motors in clockwise sequence around the belt.

```cpp
int CW[] = { Center, SideLeft, FrontLeft, FrontRight, SideRight, Center };
```

Sequence: Center → Side Left → Front Left → Front Right → Side Right → Center

#### Pattern 2: Counter-Clockwise (CCW)

Activates motors in counter-clockwise sequence.

```cpp
int CCW[] = { Center, SideRight, FrontRight, FrontLeft, SideLeft, Center };
```

Sequence: Center → Side Right → Front Right → Front Left → Side Left → Center

#### Pattern 3: Pulse

Alternating pulse pattern between motors.

```cpp
int PULSE[] = { Center, SideLeft, FrontLeft, Center, SideRight, FrontRight };
```

#### Pattern 4: Custom

User-definable pattern (modify firmware to customize).

### Serial Communication

**Baud Rate:** 57600

**Bluetooth Module:** HC-05 or HC-06

**Initialization:**
```cpp
SoftwareSerial Bluetooth(17, 16); // RX, TX pins
Bluetooth.begin(57600);
```

**Reading Commands:**
```cpp
if (Bluetooth.available()) {
  String command = Bluetooth.readString();
  // Parse and execute command
}
```

### Custom Pattern Development

To create custom patterns, modify the Arduino firmware:

```cpp
// Define motor sequence
int CUSTOM_PATTERN[] = { Pin1, Pin2, Pin3, Pin4, Pin5 };

// Add to pattern handler
if (patternId == 4) {
  executePattern(CUSTOM_PATTERN, sizeof(CUSTOM_PATTERN), repetitions, frequency);
}
```

## Configuration

### Server Configuration

File: `config/default.json`

```json
{
  "bluetooth": {
    "enabled": true,
    "devices": [
      {
        "id": 1,
        "mac": "98:D3:31:F0:5A:26",
        "name": "HC-05-Belt-1",
        "autoReconnect": true
      }
    ],
    "scanTimeout": 10000,
    "connectionRetries": 3
  },

  "osc": {
    "receivePort": 9998,
    "sendPort": 3333,
    "address": "0.0.0.0"
  },

  "websocket": {
    "enabled": true,
    "port": 8080,
    "address": "0.0.0.0"
  },

  "serial": {
    "baudRate": 57600,
    "dataBits": 8,
    "parity": "none",
    "stopBits": 1
  },

  "patterns": {
    "CW": "Clockwise rotation",
    "CCW": "Counter-clockwise rotation",
    "PULSE": "Pulse all motors",
    "CUSTOM1": "Custom pattern 1"
  }
}
```

### Adding Multiple Belts

Add additional devices to the `bluetooth.devices` array:

```json
"devices": [
  {
    "id": 1,
    "mac": "98:D3:31:F0:5A:26",
    "name": "HC-05-Belt-1"
  },
  {
    "id": 2,
    "mac": "98:D3:31:F0:5A:27",
    "name": "HC-05-Belt-2"
  },
  {
    "id": 3,
    "mac": "98:D3:31:F0:5A:28",
    "name": "HC-05-Belt-3"
  }
]
```

## Examples

### Python Client

```python
from pythonosc import udp_client
import time

# Connect to server
client = udp_client.SimpleUDPClient("192.168.1.100", 9998)

# Individual buzzer control
client.send_message("/belt_1/buzzer_1/frequency", [3, 100])
time.sleep(0.5)

client.send_message("/belt_1/buzzer_2/frequency", [3, 100])
time.sleep(0.5)

# Pattern control
client.send_message("/belt_1/pattern_1/frequency", [2, 75])  # CW
time.sleep(2)

client.send_message("/belt_1/pattern_2/frequency", [2, 75])  # CCW
time.sleep(2)

# All belts pulse
client.send_message("/belt_6/pattern_3/frequency", [5, 50])
```

### JavaScript Client

```javascript
const osc = require('osc');

const udpPort = new osc.UDPPort({
    localAddress: "0.0.0.0",
    localPort: 9999,
    remoteAddress: "192.168.1.100",
    remotePort: 9998,
    metadata: true
});

udpPort.open();

// Individual buzzer
udpPort.send({
    address: "/belt_1/buzzer_3/frequency",
    args: [
        { type: "i", value: 5 },
        { type: "i", value: 100 }
    ]
});

// Pattern control
udpPort.send({
    address: "/belt_1/pattern_1/frequency",
    args: [
        { type: "i", value: 3 },
        { type: "i", value: 75 }
    ]
});
```

### Max/MSP Patch

```
[udpsend connect 192.168.1.100 9998]
|
[prepend /belt_1/buzzer_3/frequency]
|
[pack i i]
|
[5 100]  [3 75]  [2 50]
```

## Troubleshooting

### OSC Messages Not Received

1. Check server is running: `npm start`
2. Verify IP address and port in client
3. Check firewall allows UDP on port 9998
4. Test with example script: `npm run test`

### Bluetooth Connection Fails

1. Verify MAC address in `config/default.json`
2. Check Bluetooth module is powered and paired
3. Test Python bluetooth: `pip install pybluez`
4. Check RFCOMM binding: `rfcomm bind 0 <MAC_ADDRESS> 1`

### No Haptic Response

1. Check Arduino is receiving commands (Serial Monitor)
2. Verify motor connections (PWM pins)
3. Test motors directly with Arduino IDE
4. Check power supply is adequate for motors

## Performance

**Latency:** 50-100ms total
- Network: 1-10ms
- OSC processing: 1-5ms
- Bluetooth: 40-80ms
- Arduino: 1-5ms

**Throughput:** ~10 patterns/second per belt

**Range:** ~10 meters (Bluetooth)

## See Also

- [OSC Protocol Specification](osc-protocol.md)
- [Raspberry Pi API Reference](raspberry-pi-api.md)
- [Arduino Quickstart Guide](../getting-started/arduino-quickstart.md)
- [Hardware Assembly Guide](../hardware/assembly-guide.md)

## Contributing

Found an issue or want to improve the API? See [CONTRIBUTING.md](../../CONTRIBUTING.md).
