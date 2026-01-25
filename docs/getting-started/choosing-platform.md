# Choosing a Platform

This guide helps you decide between the Arduino + Bluetooth and Raspberry Pi + I2C implementations.

## Quick Comparison

| Feature | Arduino + Bluetooth | Raspberry Pi + I2C |
|---------|--------------------|--------------------|
| **Haptic Channels** | 5 per belt, up to 6 belts (30 total) | 8 channels |
| **Connectivity** | Bluetooth (HC-05/HC-06) | WiFi (802.11n/ac) |
| **Range** | ~10 meters | Network-dependent (100+ meters) |
| **Haptic Effects** | On/Off patterns only | 120+ effects (DRV2605L) |
| **Effect Quality** | Basic vibration | High-fidelity LRA effects |
| **Portability** | ⭐⭐⭐⭐⭐ Very portable | ⭐⭐⭐ Portable with power bank |
| **Battery Life** | 8-12 hours (9V battery) | 4-6 hours (power bank) |
| **Setup Complexity** | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Advanced |
| **Cost per System** | ~$50 per belt | ~$150 total |
| **Latency** | ~50-100ms | ~10-30ms |
| **Customization** | Pattern-based | Effect library + patterns |
| **Development Platform** | Arduino IDE + Node.js | Python |

## Use Case Recommendations

### Choose Arduino + Bluetooth if:

✅ **Portability is critical**
- Wearable for outdoor use, performances, or mobile installations
- No WiFi infrastructure required
- Battery-powered operation

✅ **Budget constraints**
- Lower cost per device
- Good for multiple users/belts

✅ **Simple haptic patterns sufficient**
- Directional cues (clockwise, counter-clockwise)
- Basic pulse patterns
- Spatial audio feedback

✅ **Multiple independent devices**
- Up to 6 belts can be controlled simultaneously
- Each belt operates independently
- Good for multi-user installations

✅ **Beginner-friendly**
- Arduino is easier to learn
- Simpler hardware setup
- More forgiving of mistakes

### Choose Raspberry Pi + I2C if:

✅ **High-fidelity haptics required**
- 120+ distinct haptic effects
- Nuanced feedback (clicks, ramps, buzzes, transitions)
- Research applications requiring precise control

✅ **Network integration needed**
- WiFi connectivity
- Network-based control
- Integration with existing WiFi infrastructure

✅ **Single-user, high-quality system**
- 8 channels provide rich spatial feedback
- High-resolution haptic rendering
- Professional installations

✅ **Advanced features needed**
- OLED display for IP address
- Systemd auto-start on boot
- Thread-based command processing
- More sophisticated software architecture

✅ **Research or professional use**
- Academic research requiring validated hardware
- Professional installations
- Custom enclosures and PCBs available

## Detailed Comparison

### Hardware

#### Arduino + Bluetooth
- **Microcontroller**: Arduino Uno/Nano (~$5-25)
- **Bluetooth Module**: HC-05 or HC-06 (~$5-10)
- **Haptic Actuators**: 5x coin vibration motors or LRAs (~$10)
- **Power**: 9V battery or USB power bank
- **PCB**: Optional (can use breadboard or protoboard)
- **Enclosure**: 3D printed or DIY
- **Total**: ~$50 per belt

#### Raspberry Pi + I2C
- **Computer**: Raspberry Pi 3/4/Zero 2W (~$35-55)
- **I2C Multiplexer**: TCA9548A (~$5-8)
- **Haptic Drivers**: 8x Adafruit DRV2605L boards (~$56)
- **Actuators**: 8x Linear Resonant Actuators (~$24)
- **Display**: SSD1306 OLED (~$5)
- **Power**: USB power bank with 2.4A output
- **PCB**: Custom PCB recommended (Gerbers provided)
- **Enclosure**: 3D printed case (STL provided)
- **Total**: ~$150

### Software

#### Arduino + Bluetooth
- **Firmware**: Arduino C/C++ (simple)
- **Bridge**: Python Bluetooth bridge
- **Server**: Node.js OSC server
- **Dependencies**: Minimal (osc-min, ws)
- **Setup Time**: 30-60 minutes
- **Learning Curve**: ⭐⭐⭐ Moderate

#### Raspberry Pi + I2C
- **Firmware**: Python 3
- **Libraries**: Adafruit CircuitPython, python-osc
- **Dependencies**: More complex (10+ packages)
- **Setup Time**: 1-2 hours
- **Learning Curve**: ⭐⭐⭐⭐ Advanced

### Performance

#### Arduino + Bluetooth
- **Latency**: 50-100ms (Bluetooth overhead)
- **Throughput**: ~10 patterns/second
- **Reliability**: Can drop packets on weak Bluetooth
- **Range**: ~10 meters line-of-sight
- **Interference**: Bluetooth interference possible

#### Raspberry Pi + I2C
- **Latency**: 10-30ms (network + I2C)
- **Throughput**: 30+ effects/second
- **Reliability**: Network-dependent (very reliable on local network)
- **Range**: 100+ meters (WiFi dependent)
- **Interference**: WiFi interference possible

### Development & Debugging

#### Arduino + Bluetooth
- **Debugging**: Serial monitor, LED indicators
- **Updates**: Re-flash firmware via USB
- **Testing**: Bluetooth pairing can be finicky
- **Troubleshooting**: Limited debugging capabilities

#### Raspberry Pi + I2C
- **Debugging**: SSH access, Python debugger, logs
- **Updates**: Git pull and restart service
- **Testing**: i2cdetect, comprehensive testing utilities
- **Troubleshooting**: Full Linux debugging tools

## Mixed Deployments

You can use **both implementations** in the same installation:
- Arduino belts for mobile users
- Raspberry Pi for stationary installations
- Both respond to same OSC protocol
- Unified control interface

## Migration Path

### Start with Arduino, Upgrade Later
1. Build Arduino prototype (~$50, 1 hour)
2. Test patterns and use cases
3. If you need more channels or better effects, upgrade to Raspberry Pi
4. OSC protocol is compatible (minimal software changes)

### Start with Raspberry Pi, Scale with Arduino
1. Build high-quality Raspberry Pi system (~$150, 2 hours)
2. Develop and test sophisticated haptic feedback
3. Add Arduino belts for additional users/locations
4. Use same OSC server to control both

## Decision Tree

```
Do you need more than 8 haptic channels?
├─ YES → Arduino + Bluetooth (supports up to 30 channels with 6 belts)
└─ NO
   └─ Is portability critical (outdoor/mobile use)?
      ├─ YES → Arduino + Bluetooth
      └─ NO
         └─ Do you need high-fidelity effects (clicks, ramps, etc.)?
            ├─ YES → Raspberry Pi + I2C
            └─ NO
               └─ What's your budget?
                  ├─ < $75 → Arduino + Bluetooth
                  └─ > $75 → Raspberry Pi + I2C (better long-term)
```

## Still Undecided?

### Try Arduino First
- Lower cost and complexity
- Faster to prototype
- Can always upgrade later
- Good for learning the basics

### Questions to Ask
1. How many haptic channels do I need? (Arduino: 5-30, RPi: 8)
2. Do I need WiFi or is Bluetooth sufficient?
3. What's my budget? (<$75: Arduino, $150+: RPi)
4. Am I comfortable with Linux and Python? (If no: Arduino)
5. Do I need sophisticated haptic effects? (If yes: RPi)

## Next Steps

Once you've chosen your platform:

- **Arduino + Bluetooth**: [Arduino Quick Start Guide](arduino-quickstart.md)
- **Raspberry Pi + I2C**: [Raspberry Pi Quick Start Guide](raspberry-pi-quickstart.md)

## Community Examples

### Arduino Success Stories
- Multi-user VR installations (6 users)
- Outdoor navigation for visually impaired
- Portable spatial audio performances
- Educational workshops (low cost)

### Raspberry Pi Success Stories
- High-fidelity research installations
- Professional haptic displays
- Museum interactive exhibits
- Advanced HCI research projects

## Support

Questions? Check out:
- [GitHub Discussions](https://github.com/yourusername/On-body-haptics/discussions)
- [GitHub Issues](https://github.com/yourusername/On-body-haptics/issues)
