# OSC Protocol Specification

Complete specification for the On-Body Haptics OSC (Open Sound Control) protocol.

## Overview

The On-Body Haptics system uses OSC (Open Sound Control) for communication between control applications and haptic devices. This protocol is platform-agnostic and works with both Arduino and Raspberry Pi implementations.

## OSC Basics

- **Protocol**: UDP (User Datagram Protocol)
- **Default Port**: 9999 (configurable)
- **Message Format**: OSC 1.0 specification
- **Address Pattern**: `/onbody/...`

## Common Messages

### Arduino + Bluetooth Implementation

#### Pattern Control

```
/onbody/[belt_id]/pattern [pattern_name]
```

- **belt_id**: Belt identifier (1-6) or `*` for all belts
- **pattern_name**: String (see Pattern Names below)

**Examples:**
```
/onbody/1/pattern CW        # Clockwise rotation on belt 1
/onbody/2/pattern CCW       # Counter-clockwise on belt 2
/onbody/*/pattern PULSE     # Pulse all belts
/onbody/3/pattern CUSTOM1   # Custom pattern 1 on belt 3
```

#### Pattern Names

| Pattern | Description |
|---------|-------------|
| `CW` | Clockwise rotation around belt |
| `CCW` | Counter-clockwise rotation |
| `PULSE` | Pulse all motors simultaneously |
| `WAVE` | Wave pattern (intensity ramp) |
| `CUSTOM1` to `CUSTOM7` | Custom user-defined patterns |
| `OFF` | Turn off all motors |

### Raspberry Pi + I2C Implementation

#### Effect Control

```
/onbody/effect/[effect_id] [channel]
```

- **effect_id**: DRV2605L effect number (1-123)
- **channel**: Channel number (0-7) or omit for all channels

**Examples:**
```
/onbody/effect/14 0         # Strong click on channel 0
/onbody/effect/14           # Strong click on all channels
/onbody/effect/33 3         # Pulsing on channel 3
```

#### Channel-Specific Control

```
/onbody/channel/[channel]/effect [effect_id]
```

**Example:**
```
/onbody/channel/5/effect 14  # Strong click on channel 5
```

## Effect Library (Raspberry Pi)

The DRV2605L provides 123 haptic effects. Common effects:

### Clicks
- `14` - Strong Click 100%
- `15` - Sharp Click 100%
- `16` - Soft Click 100%

### Bumps
- `18` - Soft Bump 100%
- `19` - Medium Bump 100%

### Double Clicks
- `20` - Double Click 100%
- `21` - Double Click 60%

### Triple Clicks
- `30` - Triple Click 100%
- `31` - Triple Click 60%

### Pulses
- `33` - Pulsing Strong 1 (100%)
- `34` - Pulsing Strong 2 (60%)
- `35` - Pulsing Medium 1 (100%)

### Ramps
- `64` - Ramp Up Long Heavy
- `65` - Ramp Up Medium Heavy
- `70` - Ramp Down Long Heavy

See [DRV2605L datasheet](../../hardware/datasheets/DRV2605L.pdf) for complete effect library.

## Advanced Features

### Regex Pattern Matching (Arduino)

The Arduino implementation supports regex-based addressing for controlling multiple belts:

```
/onbody/*/pattern CW        # All belts
/onbody/[12]/pattern PULSE  # Belts 1 and 2
/onbody/[1-3]/pattern CCW   # Belts 1, 2, and 3
```

### Intensity Control (Future)

Future versions may support intensity parameters:

```
/onbody/1/pattern CW 0.5    # Half intensity (planned)
/onbody/effect/14 0 0.75    # 75% intensity (planned)
```

## Message Format Details

### OSC Message Structure

```
OSC Address Pattern: /onbody/...
OSC Type Tags: Varies by message
OSC Arguments: Strings, integers, floats
```

### Example Messages (Binary)

Arduino Pattern (as OSC bundle):
```
Address: /onbody/1/pattern
Type Tag: ,s (string)
Argument: "CW"
```

Raspberry Pi Effect:
```
Address: /onbody/effect/14
Type Tag: ,i (integer)
Argument: 0
```

## Client Examples

### Python (pythonosc)

```python
from pythonosc import udp_client

# Connect to device
client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Arduino: Send pattern
client.send_message("/onbody/1/pattern", "CW")
client.send_message("/onbody/*/pattern", "PULSE")

# Raspberry Pi: Send effect
client.send_message("/onbody/effect/14", 0)  # Channel 0
client.send_message("/onbody/effect/33", 5)  # Channel 5

# Send to all channels (omit argument)
client.send_message("/onbody/effect/14")
```

### JavaScript (osc-js)

```javascript
const OSC = require('osc-js');

const osc = new OSC();
osc.open({ port: 9999 });

// Arduino: Send pattern
osc.send(new OSC.Message('/onbody/1/pattern', 'CW'));
osc.send(new OSC.Message('/onbody/2/pattern', 'CCW'));

// Raspberry Pi: Send effect
osc.send(new OSC.Message('/onbody/effect/14', 0));
```

### Max/MSP

```
[udpsend 192.168.1.100 9999]
|
[prepend /onbody/1/pattern]
|
[CW(  [CCW(  [PULSE(
```

### TouchDesigner

```python
# In Execute DAT
def onValueChange(channel, sampleIndex, val, prev):
    # Send OSC message
    op('oscout1').sendOSC('/onbody/1/pattern', ['CW'])
```

### Pure Data (Pd)

```
[udpsend]
|
[send 192.168.1.100 9999(
|
[/onbody/1/pattern CW(
```

### Unity (C#)

```csharp
using UnityEngine;
using OscCore;

public class HapticController : MonoBehaviour
{
    OscClient client;

    void Start()
    {
        client = new OscClient("192.168.1.100", 9999);
    }

    public void SendPattern(int belt, string pattern)
    {
        client.Send($"/onbody/{belt}/pattern", pattern);
    }

    public void SendEffect(int effect, int channel)
    {
        client.Send($"/onbody/effect/{effect}", channel);
    }
}
```

## Network Configuration

### Default Ports

- **Receive Port**: 9999 (OSC messages to device)
- **Send Port**: 3333 (OSC responses from device, optional)

### Firewall Configuration

Allow UDP traffic on port 9999:

```bash
# Linux (ufw)
sudo ufw allow 9999/udp

# Linux (iptables)
sudo iptables -A INPUT -p udp --dport 9999 -j ACCEPT

# macOS
# System Preferences > Security & Privacy > Firewall > Firewall Options

# Windows
# Windows Defender Firewall > Advanced Settings > Inbound Rules
```

## Error Handling

### Message Validation

The system performs minimal validation:
- Invalid patterns are ignored (Arduino)
- Invalid effect IDs are clamped to 1-123 (Raspberry Pi)
- Invalid channels are ignored (Raspberry Pi)

### Network Issues

- **Lost packets**: OSC uses UDP, packets may be lost
- **No acknowledgment**: Devices don't send ACK by default
- **No retry**: Clients should implement retry logic if needed

### Debugging

#### Arduino
```bash
# Monitor serial output
# Arduino IDE > Tools > Serial Monitor (57600 baud)
```

#### Raspberry Pi
```bash
# Enable verbose logging in config.py
VERBOSE_OSC = True
LOG_LEVEL = "DEBUG"

# View logs
sudo journalctl -u octopulse-server -f
```

## Performance Considerations

### Latency

- **Arduino + Bluetooth**: 50-100ms total latency
  - Network to server: 1-10ms
  - Bluetooth transmission: 40-80ms
  - Arduino processing: 1-5ms

- **Raspberry Pi + I2C**: 10-30ms total latency
  - Network transmission: 1-10ms
  - OSC parsing: 1-5ms
  - I2C communication: 5-10ms
  - DRV2605L processing: 1-5ms

### Throughput

- **Arduino**: ~10 patterns/second per belt
- **Raspberry Pi**: ~30 effects/second per channel

### Rate Limiting

No built-in rate limiting. Implement in client:

```python
import time

def send_pattern_throttled(client, belt, pattern, min_interval=0.1):
    """Send pattern with minimum interval between calls"""
    client.send_message(f"/onbody/{belt}/pattern", pattern)
    time.sleep(min_interval)
```

## Security

⚠️ **Important**: OSC has no built-in authentication or encryption

- Run on trusted networks only
- Use firewall rules to restrict access
- Consider VPN or SSH tunneling for remote access
- See [SECURITY.md](../../SECURITY.md) for detailed security guidance

## Protocol Extensions

### Custom Namespaces

You can extend the protocol with custom namespaces:

```
/onbody/custom/myapp/...
```

Just ensure they don't conflict with standard messages.

### Future Extensions

Planned for future versions:
- `/onbody/intensity` - Global intensity control
- `/onbody/status` - Device status queries
- `/onbody/calibrate` - Calibration commands
- `/onbody/config` - Runtime configuration updates

## Compatibility

### Tested With

- Max/MSP 8.x
- TouchDesigner 2022.x
- Pure Data 0.52.x
- Unity 2021.x/2022.x
- Python 3.7+
- Node.js 14+

### Standards Compliance

- OSC 1.0 specification
- UDP/IP protocol
- Network byte order (big-endian)

## References

- [OSC 1.0 Specification](http://opensoundcontrol.org/spec-1_0)
- [OSC 1.1 Specification (draft)](http://opensoundcontrol.org/spec-1_1)
- [pythonosc Documentation](https://pypi.org/project/python-osc/)
- [osc-js Documentation](https://www.npmjs.com/package/osc-js)

## Support

Questions about the OSC protocol? Ask in [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions).
