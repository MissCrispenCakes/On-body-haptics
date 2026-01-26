# On-Body Haptics

> **Open-source wearable haptic feedback systems for spatial audio, VR/AR, and interactive installations**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Sponsor](https://img.shields.io/badge/Sponsor-❤-red)](https://github.com/sponsors/MissCrispenCakes)

Transform spatial information into tactile sensations with wearable haptic devices. This project provides complete hardware designs, firmware, and software for building custom haptic feedback systems that respond to OSC (Open Sound Control) messages.

## ✨ Features

- **Audio-Reactive by Design**
  - Originally built as audio-reactive LED wearables (sound → light patterns)
  - Evolved into audio-haptic feedback systems (sound → tactile patterns)
  - Signal-agnostic: responds to any OSC-formatted input (audio, sensors, game engines, etc.)

- **Two Complete Implementations**
  - **Arduino + Bluetooth**: Portable system with up to 6 wireless haptic belts
  - **Raspberry Pi + I2C**: High-fidelity system with 8 channels and 120+ haptic effects

- **Professional Hardware**
  - Custom PCB designs (KiCad projects included)
  - Gerber files ready for manufacturing (JLCPCB, PCBWay)
  - 3D-printable enclosures (STL and OpenSCAD source)
  - Complete Bill of Materials with part numbers

- **OSC Protocol Integration**
  - Standard OSC namespace for haptic control
  - Works with Max/MSP, TouchDesigner, Unity, Pure Data, and more
  - WebSocket bridge for web applications
  - Regex-based multi-device addressing

- **Pre-programmed Patterns**
  - Clockwise/counter-clockwise rotation
  - Pulse and wave patterns
  - 7 customizable pattern slots
  - Real-time pattern updates via OSC

- **Production Ready**
  - Systemd services for auto-start
  - OLED IP display for network debugging
  - Proper dependency management
  - Configuration templates (no hardcoded credentials)

## 🚀 Quick Start

### Choose Your Platform

| Feature | Arduino + Bluetooth | Raspberry Pi + I2C |
|---------|--------------------|--------------------|
| **Haptic Channels** | 5 per belt, up to 6 belts | 8 channels |
| **Connectivity** | Bluetooth (HC-05/HC-06) | WiFi |
| **Haptic Effects** | On/Off patterns | 120+ DRV2605L effects |
| **Portability** | ⭐⭐⭐⭐⭐ Highly portable | ⭐⭐⭐ Portable with power bank |
| **Setup Complexity** | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Advanced |
| **Cost** | ~$30 per belt | ~$150 total |

**New to haptics?** Start with the **[Arduino + Bluetooth](docs/getting-started/arduino-quickstart.md)** implementation.

**Need high fidelity?** Use the **[Raspberry Pi + I2C](docs/getting-started/raspberry-pi-quickstart.md)** implementation.

### 15-Minute Setup Guides

1. **[Arduino + Bluetooth Quick Start](docs/getting-started/arduino-quickstart.md)**
   - Flash firmware to Arduino
   - Pair Bluetooth module
   - Run Node.js OSC bridge
   - Send your first haptic pattern

2. **[Raspberry Pi + I2C Quick Start](docs/getting-started/raspberry-pi-quickstart.md)**
   - Install Raspberry Pi OS
   - Clone and install software
   - Configure I2C devices
   - Send your first haptic effect

## 📖 Documentation

### Getting Started
- [Choosing a Platform](docs/getting-started/choosing-platform.md) - Detailed comparison and decision guide
- [Arduino Quick Start](docs/getting-started/arduino-quickstart.md) - 15-minute setup
- [Raspberry Pi Quick Start](docs/getting-started/raspberry-pi-quickstart.md) - 15-minute setup

### Hardware
- [Assembly Guide](docs/hardware/assembly-guide.md) - Step-by-step with photos
- [PCB Fabrication](docs/hardware/pcb-fabrication.md) - How to order PCBs
- [Bill of Materials](docs/hardware/bom.md) - Where to buy components
- [3D Printing Guide](docs/hardware/enclosure-printing.md) - Print settings and materials

### API & Integration
- [OSC Protocol Specification](docs/api/osc-protocol.md) - Complete OSC namespace
- [Arduino API Reference](docs/api/arduino-api.md) - Serial protocol and patterns
- [Raspberry Pi API Reference](docs/api/raspberry-pi-api.md) - I2C and effects library
- [Max/MSP Integration](docs/integration/max-msp.md)
- [TouchDesigner Integration](docs/integration/touchdesigner.md)
- [Unity VR Integration](docs/integration/unity-vr.md)

### Research Context
- [Research Background](docs/research/context.md) - Academic context and publications

## 🛠 Project Structure

```
on-body-haptics/
├── implementations/          # Platform-specific implementations
│   ├── arduino-bluetooth/   # Arduino + Node.js + Bluetooth
│   └── raspberry-pi-i2c/    # Raspberry Pi + I2C
├── hardware/                # PCB designs and enclosures
│   ├── pcb/                # KiCad projects and Gerbers
│   └── enclosures/         # 3D-printable cases
├── protocol/               # OSC protocol specification
├── docs/                   # Documentation
└── tools/                  # Development and testing tools
```

## 🔧 Use Cases

- **Spatial Audio Feedback**: Directional cues for immersive audio experiences
- **VR/AR Navigation**: Haptic waypoints and object proximity alerts
- **Interactive Installations**: Responsive art installations with tactile feedback
- **Accessibility**: Spatial information for visually impaired users
- **Research**: Haptic perception studies and HCI research
- **Gaming**: Immersive tactile feedback for games
- **Telepresence**: Remote touch and directional communication

## 💡 Integration Examples

### Send a Haptic Pattern (OSC)

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Trigger clockwise rotation on belt 1
client.send_message("/onbody/1/pattern", "CW")

# Trigger specific effect on Raspberry Pi
client.send_message("/onbody/effect/14", 1)  # Strong click 100%
```

### Send via WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8080');

ws.onopen = () => {
  // Send haptic pulse pattern
  ws.send(JSON.stringify({
    address: '/onbody/1/pattern',
    args: ['PULSE']
  }));
};
```

### Max/MSP

```
[udpsend 192.168.1.100 9999]
|
[prepend /onbody/1/pattern]
|
[CW(  [CCW(  [PULSE(
```

## 🏗 Hardware Implementations

### Arduino + Bluetooth
- **Microcontroller**: Arduino Uno/Nano
- **Bluetooth**: HC-05 or HC-06 module
- **Haptic Drivers**: 5x coin vibration motors or LRAs
- **Power**: 3.7V LiPo battery
- **Total Cost**: ~$30 per belt

### Raspberry Pi + I2C
- **Computer**: Raspberry Pi 3/4/Zero 2W
- **I2C Multiplexer**: TCA9548A (8 channels)
- **Haptic Drivers**: 8x Adafruit DRV2605L boards
- **Actuators**: 8x Linear Resonant Actuators (LRAs)
- **Display**: SSD1306 OLED (128x32)
- **Total Cost**: ~$150

Complete schematics, PCB designs, and assembly instructions are available in the [hardware documentation](docs/hardware/).

## 🤝 Contributing

We welcome contributions! Whether you're fixing bugs, improving documentation, or adding new features, please see our [Contributing Guide](CONTRIBUTING.md).

### Development Setup

```bash
# Clone the repository
git clone https://github.com/MissCrispenCakes/On-body-haptics.git
cd On-body-haptics

# For Arduino implementation
cd implementations/arduino-bluetooth/server
npm install

# For Raspberry Pi implementation
cd implementations/raspberry-pi-i2c/firmware
pip install -r requirements.txt
```

## 📄 License

This project uses **dual licensing** to cover both software and hardware:

### Software License
**MIT License** - All software, firmware, and code are licensed under the MIT License.
- See [LICENSE](LICENSE) for details
- Includes: Arduino firmware, Python code, Node.js server, test scripts

### Hardware License
**CERN-OHL-P v2** (CERN Open Hardware License - Permissive) - All hardware designs are licensed under CERN-OHL-P v2.
- See [LICENSE-HARDWARE](LICENSE-HARDWARE) for details
- Includes: PCB designs (KiCad), Gerber files, 3D enclosures (STL/OpenSCAD), schematics, BOM

This ensures both software and hardware freedom while using licenses designed for their respective domains.

### Open Source Hardware Certification

**This project is ready for OSHWA certification!** ✅

All requirements for [Open Source Hardware Association (OSHWA)](https://oshwa.org/) certification are met:
- ✅ OSHWA-approved licenses (CERN-OHL-P v2 + MIT)
- ✅ Complete design files (KiCad, OpenSCAD, Gerbers)
- ✅ Clear documentation and accessibility
- ✅ Third-party component datasheets included

See [OSHWA Certification Guide](docs/OSHWA_CERTIFICATION.md) for step-by-step instructions to get your official OSHW certification mark and UID.

## 🙏 Acknowledgments

- **[@rglenn](https://github.com/rglenn)** for:
  - Production-ready PCB designs and Gerber files for manufacturing
  - 3D printed enclosure samples with battery compartment (a wonderful surprise!)
  - I2C system implementation and hardware testing
  - Expert soldering skills for prototype assembly (saving the project from shaky hands and twitchy eyeballs!)
- Research context from tactile feedback and spatial audio studies
- DRV2605L haptic driver library by Adafruit
- OSC protocol implementation using `osc-min` and `python-osc`

See [AUTHORS.md](AUTHORS.md) for complete contributor details.

## 📰 Press & Features

- **[Hackaday](https://hackaday.com/2020/02/12/in-pursuit-of-haptics-for-a-better-vr-experience/)** - "In Pursuit of Haptics for a Better VR Experience" (February 2020)
- **[Mitacs Grant](https://www.mitacs.ca/our-projects/washable-wearables-for-affordable-and-aesthetic-augmentation-of-visuo-tactile-sensory-perception-enhancement-in-mixed-reality/)** - "Washable Wearables for Affordable and Aesthetic Augmentation of Visuo-Tactile Sensory Perception Enhancement in Mixed Reality"

> 💡 **Maker Tip**: Swap the haptic motors for LEDs and you've got a wearable light display! Same control protocol, different sensory modality. The original prototype used audio-reactive LEDs before evolving into haptic feedback. 🌈

## 💖 Support This Project

If you find this project useful, consider:

- ⭐ Starring this repository
- 🐛 Reporting bugs and suggesting features
- 📖 Improving documentation
- 💰 [Sponsoring development](https://github.com/sponsors/KDF-dev)

Your support helps maintain and improve this open-source project!

## 📞 Contact & Community

- **Issues**: [GitHub Issues](https://github.com/MissCrispenCakes/On-body-haptics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)
- **Website**: [KDF Entertainment](https://www.kdfentertainment.com/about)

## 📚 Citation

If you use this project in your research, please cite using the information in [CITATION.cff](CITATION.cff) or:

**Suggested Citation:**

MissCrispenCakes, & rglenn. (2026). On-Body Haptics: Open-Source Wearable Haptic Feedback Systems (Version 2.0.0) [Computer software]. https://github.com/MissCrispenCakes/On-body-haptics

**BibTeX:**
```bibtex
@software{onbodyhaptics2026,
  author = {MissCrispenCakes and rglenn},
  title = {On-Body Haptics: Open-Source Wearable Haptic Feedback Systems},
  version = {2.0.0},
  year = {2026},
  url = {https://github.com/MissCrispenCakes/On-body-haptics}
}
```

**Zenodo DOI**: Coming soon (archive and get DOI by connecting this repo to Zenodo)

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata and [AUTHORS.md](AUTHORS.md) for contributor information.

---

**Built with ❤️ for the haptics and HCI community**
