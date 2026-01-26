# Arduino + Bluetooth Quick Start

Get your Arduino-based haptic system running in 15 minutes.

## What You'll Build

A portable, battery-powered haptic belt with 5 vibration motors controlled via Bluetooth and OSC protocol.

**Time**: 15-30 minutes
**Difficulty**: ⭐⭐⭐ Moderate

## Prerequisites

### Hardware Required

- **Arduino Uno or Nano** (~$5-25)
- **HC-05 or HC-06 Bluetooth module** (~$5-10)
- **5x Vibration motors** (coin motors or LRAs) (~$2-10)
- **5x NPN transistors** (2N2222 or similar) (~$1)
- **5x 1kΩ resistors** (~$0.50)
- **5x 1N4001 diodes** (~$0.50)
- **Breadboard and jumper wires** (~$5)
- **3.7V LiPo battery** (~$5-10)

**Total Cost**: ~$25-50 per belt

### Software Required

- **Arduino IDE** (1.8.x or 2.x) - [Download here](https://www.arduino.cc/en/software)
- **Node.js** (14.x or higher) - [Download here](https://nodejs.org/)
- **Python 3** (for Bluetooth bridge) - [Download here](https://www.python.org/)

### Optional

- Soldering equipment (for permanent builds)
- Battery holder or connector
- Enclosure or belt material

## Step 1: Wire the Hardware (10 minutes)

### Wiring Diagram

```
Arduino Uno Connections:
┌─────────────────┐
│  Arduino Uno    │
│                 │
│  D3  ───────────┼──► Motor 1 circuit
│  D5  ───────────┼──► Motor 2 circuit
│  D6  ───────────┼──► Motor 3 circuit
│  D9  ───────────┼──► Motor 4 circuit
│  D10 ───────────┼──► Motor 5 circuit
│                 │
│  RX  ───────────┼──► HC-05 TX
│  TX  ───────────┼──► HC-05 RX
│                 │
│  5V  ───────────┼──► HC-05 VCC
│  GND ───────────┼──► HC-05 GND, Motor GND
└─────────────────┘

Motor Driver Circuit (repeat for each motor):
Arduino Pin ──► 1kΩ Resistor ──► Transistor Base
                                  │
Transistor Collector ──► Motor (+) ──► Diode ──► 5V
                                  │
Transistor Emitter ────────────────► GND

Note: Diode protects against back-EMF (stripe toward 5V)
```

### Detailed Connections

#### Bluetooth Module (HC-05/HC-06)

| HC-05 Pin | Arduino Pin | Notes |
|-----------|-------------|-------|
| VCC | 5V | Power |
| GND | GND | Ground |
| TXD | RX (Pin 0) | Data from HC-05 to Arduino |
| RXD | TX (Pin 1) | Data from Arduino to HC-05 |

⚠️ **Important**: Some HC-05 modules are 3.3V logic. Use a voltage divider on TX→RXD if needed.

#### Motors (repeat for each of 5 motors)

For Motor 1 on Pin D3:

1. **Arduino D3** → 1kΩ resistor → **Transistor Base**
2. **5V** → **Motor positive** → **Transistor Collector**
3. **Transistor Emitter** → **GND**
4. **1N4001 Diode** across motor (stripe to 5V side)

Repeat for:
- Motor 2: Pin D5
- Motor 3: Pin D6
- Motor 4: Pin D9
- Motor 5: Pin D10

### Quick Breadboard Layout

```
Power Rails:
  Red (+):  5V from Arduino
  Blue (-): GND from Arduino

Row by Row:
  Row 1-5:   Five motor driver circuits
  Row 6:     HC-05 Bluetooth module

Keep motor wires short to reduce noise!
```

## Step 2: Flash Arduino Firmware (5 minutes)

### 2.1 Get the Code

```bash
cd implementations/arduino-bluetooth/firmware/AudioHaptics
```

### 2.2 Configure Pins (if needed)

Open `config.h` and verify pin assignments match your wiring:

```cpp
#define MOTOR_1_PIN 3
#define MOTOR_2_PIN 5
#define MOTOR_3_PIN 6
#define MOTOR_4_PIN 9
#define MOTOR_5_PIN 10

#define SERIAL_BAUD 57600
```

### 2.3 Upload to Arduino

1. **Open Arduino IDE**
2. **Open** `AudioHaptics.ino`
3. **Select Board**: Tools → Board → Arduino Uno (or your board)
4. **Select Port**: Tools → Port → (your Arduino's port)
5. **Click Upload** ✅

### 2.4 Verify Upload

Open **Serial Monitor** (Tools → Serial Monitor):
- Set baud rate to **57600**
- You should see: "Haptic Belt Ready"

Test a motor manually:
- Type: `CW` and press Enter
- Motors should activate in clockwise sequence

## Step 3: Pair Bluetooth (5 minutes)

### 3.1 Find Your Bluetooth Module

The HC-05/HC-06 should be visible as a Bluetooth device.

#### On Linux:

```bash
bluetoothctl
scan on
# Wait for "HC-05" or similar to appear
# Note the MAC address (e.g., 00:11:22:33:44:55)
pair 00:11:22:33:44:55
trust 00:11:22:33:44:55
connect 00:11:22:33:44:55
exit
```

#### On Windows:

1. Settings → Bluetooth & devices → Add device
2. Select "HC-05" or "HC-06"
3. Enter PIN (default: `1234` or `0000`)
4. Note the COM port assigned (e.g., COM5)

#### On macOS:

1. System Preferences → Bluetooth
2. Find "HC-05" and click "Connect"
3. Enter PIN: `1234`
4. Note: macOS doesn't show Bluetooth serial ports easily; use Linux or Windows for development

### 3.2 Find the MAC Address

**Linux**:
```bash
bluetoothctl
devices
# Look for your HC-05, note the MAC address
```

**Windows**:
```bash
# PowerShell
Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like "*HC*"}
```

Write down the MAC address - you'll need it for configuration!

## Step 4: Set Up OSC Bridge (10 minutes)

### 4.1 Install Node.js Dependencies

```bash
cd implementations/arduino-bluetooth/server
npm install
```

This installs:
- `osc-min` - OSC protocol handling
- `ws` - WebSocket server

### 4.2 Install Python Dependencies

```bash
# From same directory
pip install -r ../requirements.txt
```

This installs:
- `pyserial` - Serial communication
- `pybluez` - Bluetooth (Linux)

### 4.3 Configure Bluetooth Device

```bash
cd server
cp config/example.json config/local.json
nano config/local.json  # or your favorite editor
```

Edit the Bluetooth MAC address:

```json
{
  "bluetooth": {
    "devices": [
      {
        "id": 1,
        "mac": "00:11:22:33:44:55",  // ← Replace with YOUR MAC address
        "name": "HC-05-Belt-1",
        "autoReconnect": true
      }
    ]
  },
  "osc": {
    "receivePort": 9999,
    "sendPort": 3333
  }
}
```

Save and exit.

### 4.4 Start the Server

```bash
npm start
```

You should see:
```
OSC Server listening on port 9999
Bluetooth connected to HC-05-Belt-1 (00:11:22:33:44:55)
Ready to receive haptic commands
```

## Step 5: Send Your First Haptic Pattern! (2 minutes)

### Option A: Use the Example Script

In a **new terminal**:

```bash
cd implementations/arduino-bluetooth/server
npm test
```

This sends test patterns to your belt. You should feel vibrations!

### Option B: Python OSC Client

Create `test_haptics.py`:

```python
from pythonosc import udp_client
import time

# Connect to server
client = udp_client.SimpleUDPClient("localhost", 9999)

# Test patterns
print("Testing CW (clockwise)...")
client.send_message("/onbody/1/pattern", "CW")
time.sleep(2)

print("Testing CCW (counter-clockwise)...")
client.send_message("/onbody/1/pattern", "CCW")
time.sleep(2)

print("Testing PULSE...")
client.send_message("/onbody/1/pattern", "PULSE")
time.sleep(2)

print("All tests complete!")
```

Run it:
```bash
pip install python-osc
python test_haptics.py
```

### Option C: Command Line (Linux/Mac)

```bash
# Install oscsend
sudo apt-get install liblo-tools  # Linux
brew install liblo                 # macOS

# Send patterns
oscsend localhost 9999 /onbody/1/pattern s CW
oscsend localhost 9999 /onbody/1/pattern s CCW
oscsend localhost 9999 /onbody/1/pattern s PULSE
```

## 🎉 Success!

If you felt vibrations, congratulations! Your haptic belt is working!

## Next Steps

### Customize Patterns

Edit `firmware/AudioHaptics/patterns.h` to create custom patterns:

```cpp
void customPattern1() {
  // Example: Alternating motors
  activateMotor(0, MOTOR_INTENSITY_HIGH);
  activateMotor(2, MOTOR_INTENSITY_HIGH);
  activateMotor(4, MOTOR_INTENSITY_HIGH);
  delay(200);
  allMotorsOff();

  activateMotor(1, MOTOR_INTENSITY_HIGH);
  activateMotor(3, MOTOR_INTENSITY_HIGH);
  delay(200);
  allMotorsOff();
}
```

Re-upload firmware, then trigger with:
```python
client.send_message("/onbody/1/pattern", "CUSTOM1")
```

### Make It Wearable

1. **Solder connections** for reliability
2. **Add enclosure** (3D print or use project box)
3. **Attach to belt** with velcro or elastic
4. **Use battery power** (9V or USB power bank)
5. **Position motors** around waist/arm (equal spacing)

### Add More Belts

To control multiple belts (up to 6):

1. Build additional belts with different Bluetooth modules
2. Pair each module
3. Add to `config/local.json`:

```json
{
  "bluetooth": {
    "devices": [
      {
        "id": 1,
        "mac": "00:11:22:33:44:55",
        "name": "Belt-1"
      },
      {
        "id": 2,
        "mac": "00:11:22:33:44:66",
        "name": "Belt-2"
      }
    ]
  }
}
```

Control individually:
```python
client.send_message("/onbody/1/pattern", "CW")   # Belt 1
client.send_message("/onbody/2/pattern", "CCW")  # Belt 2
client.send_message("/onbody/*/pattern", "PULSE") # All belts
```

## Troubleshooting

### Arduino Not Uploading

- **Check USB cable** - Some cables are power-only
- **Check COM port** - Tools → Port → Select correct port
- **Press reset** right before upload
- **Try different USB port**

### Bluetooth Won't Pair

- **Check power** - HC-05 LED should blink
- **Default PIN**: Try `1234` or `0000`
- **Reset module** - Disconnect power for 10 seconds
- **Check wiring** - VCC to 5V, GND to GND, TX↔RX crossed

### Motors Not Working

- **Check transistor** - Use multimeter to verify switching
- **Check diode direction** - Stripe should face 5V
- **Check power** - Motors need sufficient current (use external power if needed)
- **Test with LED** - Replace motor with LED to verify circuit

### Serial Communication Issues

- **Check baud rate** - Must be 57600
- **Disconnect Bluetooth** - Serial Monitor and Bluetooth can't share port
- **Check TX/RX** - Make sure they're crossed (Arduino TX → HC-05 RX)

### OSC Server Not Receiving

- **Check port** - Default is 9999
- **Check firewall** - Allow UDP port 9999
- **Test locally first** - Use `localhost` before remote IPs
- **Check config** - Verify `config/local.json` is correct

### No Haptic Feedback

1. **Test Arduino directly** - Use Serial Monitor to send "CW"
2. **Check Bluetooth connection** - Server should show "connected"
3. **Check motor power** - May need external power supply
4. **Verify OSC messages** - Add logging to see incoming messages

## Integration Examples

### Max/MSP

```
[udpsend localhost 9999]
|
[prepend /onbody/1/pattern]
|
[CW( [CCW( [PULSE(
```

### TouchDesigner

```python
# In Execute DAT
op('oscout1').sendOSC('/onbody/1/pattern', ['CW'])
```

### Unity

```csharp
using UnityEngine;
using OscCore;

public class HapticBelt : MonoBehaviour {
    OscClient client;

    void Start() {
        client = new OscClient("localhost", 9999);
    }

    public void VibrateClockwise() {
        client.Send("/onbody/1/pattern", "CW");
    }
}
```

## Further Reading

- [OSC Protocol Specification](../api/osc-protocol.md)
- [Custom Pattern Development](../api/arduino-api.md)
- [Hardware Assembly Guide](../hardware/assembly-guide.md)
- [Integration Examples](../integration/)

## Get Help

- [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)
- [Report Issues](https://github.com/MissCrispenCakes/On-body-haptics/issues)

---

**Enjoy your haptic belt!** Share your projects in [Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions/categories/show-and-tell)! 🎉
