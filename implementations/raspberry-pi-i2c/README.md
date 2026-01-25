# Raspberry Pi + I2C Implementation

High-fidelity haptic feedback system using Raspberry Pi, I2C multiplexer, and DRV2605L haptic drivers.

## Overview

- **Hardware**: Raspberry Pi 3/4/Zero 2W
- **Haptic Channels**: 8 channels via I2C multiplexer
- **Communication**: WiFi with OSC protocol
- **Haptic Effects**: 120+ effects from DRV2605L library
- **Display**: SSD1306 OLED for IP address
- **Cost**: ~$150 total

## Features

- 8 independent haptic channels with I2C multiplexing
- 120+ pre-programmed haptic effects (DRV2605L library)
- OLED display with button for IP address cycling
- Systemd service for auto-start on boot
- Queue-based command processing with threading
- Custom PCB design with Raspberry Pi HAT form factor

## Quick Start

See the [Raspberry Pi Quick Start Guide](../../docs/getting-started/raspberry-pi-quickstart.md) for detailed setup instructions.

### 1. Prepare Raspberry Pi

```bash
# Enable I2C
sudo raspi-config
# Interface Options > I2C > Enable

# Reboot
sudo reboot
```

### 2. Install Software

```bash
cd implementations/raspberry-pi-i2c/firmware

# Install dependencies
pip3 install -r requirements.txt

# Or install as package
sudo pip3 install -e .
```

### 3. Configure

```bash
# Copy configuration template
cp src/config.py.example src/config.py

# Edit configuration
nano src/config.py
```

### 4. Test I2C Devices

```bash
# Detect I2C devices
i2cdetect -y 1

# Test GPIO and buzzers
python3 utils/gpio_check.py
python3 utils/buzz_test.py
```

### 5. Run Server

```bash
# Run directly
python3 src/octopulse_server.py

# Or use installed command
octopulse-server

# Or install systemd service (auto-start on boot)
sudo cp systemd/octopulse-server.service /etc/systemd/system/
sudo systemctl enable octopulse-server
sudo systemctl start octopulse-server
```

### 6. Send Haptic Effects

```python
from pythonosc import udp_client

# Connect to Raspberry Pi
client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

# Trigger effect on channel 0
client.send_message("/onbody/effect/14", 0)  # Strong click on channel 0

# Trigger on all channels
for channel in range(8):
    client.send_message("/onbody/effect/14", channel)
```

## Directory Structure

```
raspberry-pi-i2c/
├── firmware/
│   ├── src/
│   │   ├── octopulse.py          # Main Octopulse class
│   │   ├── octopulse_server.py   # OSC server
│   │   ├── i2c_thread.py         # I2C thread handler
│   │   └── config.py             # Configuration
│   ├── systemd/
│   │   ├── octopulse-server.service
│   │   └── ip-display.service
│   ├── utils/
│   │   ├── ip_display.py         # OLED IP display
│   │   ├── gpio_check.py         # GPIO tester
│   │   └── buzz_test.py          # Buzzer tester
│   ├── requirements.txt
│   ├── setup.py
│   └── README.md
└── docs/
    └── wiring-diagram.png
```

## Hardware Setup

### I2C Addresses

- **TCA9548A I2C Multiplexer**: 0x70
- **DRV2605L Haptic Drivers**: 0x5A (8x, on multiplexer channels 0-7)
- **SSD1306 OLED Display**: 0x3C (on main I2C bus)

### Wiring

```
Raspberry Pi GPIO:
├── I2C1 SDA (GPIO 2) ──> TCA9548A SDA
├── I2C1 SCL (GPIO 3) ──> TCA9548A SCL
├── GPIO 17 ──> Button (pull-up, OLED display control)
└── 3.3V/5V/GND ──> Power distribution

TCA9548A Channels (0-7):
├── Channel 0 ──> DRV2605L #0 (I2C address 0x5A)
├── Channel 1 ──> DRV2605L #1 (I2C address 0x5A)
├── ...
└── Channel 7 ──> DRV2605L #7 (I2C address 0x5A)

Each DRV2605L:
└── OUT+ / OUT- ──> Linear Resonant Actuator (LRA)
```

See [hardware documentation](../../docs/hardware/assembly-guide.md) for detailed wiring diagrams.

## Configuration

### config.py

```python
# OSC Configuration
OSC_RECEIVE_PORT = 9999
OSC_SEND_PORT = 3333

# I2C Configuration
I2C_MULTIPLEXER_ADDRESS = 0x70
DRV2605_ADDRESS = 0x5A
NUM_CHANNELS = 8

# OLED Display
OLED_ENABLED = True
OLED_WIDTH = 128
OLED_HEIGHT = 32

# GPIO
BUTTON_PIN = 17  # BCM numbering
```

## OSC Protocol

### Effect Control

```
/onbody/effect/[effect_id] [channel]
```

Effect IDs (DRV2605L library):
- 1-13: Strong clicks (various durations)
- 14-17: Sharp clicks
- 18-28: Soft bumps and double bumps
- 29-36: Triple clicks and pulses
- 37-117: Various effects (ramps, buzzes, transitions)

### Examples

```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("raspberrypi.local", 9999)

# Strong click 100% on channel 0
client.send_message("/onbody/effect/14", 0)

# Sharp click 100% on channel 3
client.send_message("/onbody/effect/15", 3)

# Soft bump 100% on channel 7
client.send_message("/onbody/effect/18", 7)

# Pulsing strong 1 (100%) on all channels
for ch in range(8):
    client.send_message("/onbody/effect/33", ch)
```

### Max/MSP

```
[udpsend raspberrypi.local 9999]
|
[prepend /onbody/effect/14]
|
[0( [1( [2( [3(  <- channel numbers
```

## Systemd Service

### Installation

```bash
# Copy service file
sudo cp systemd/octopulse-server.service /etc/systemd/system/

# Enable auto-start
sudo systemctl enable octopulse-server

# Start service
sudo systemctl start octopulse-server

# Check status
sudo systemctl status octopulse-server

# View logs
sudo journalctl -u octopulse-server -f
```

### Service Configuration

Edit `/etc/systemd/system/octopulse-server.service`:

```ini
[Unit]
Description=Octopulse Haptic Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/On-body-haptics/implementations/raspberry-pi-i2c/firmware
ExecStart=/usr/bin/python3 src/octopulse_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## OLED Display

### IP Display Service

Shows Raspberry Pi IP addresses on OLED display. Press button to cycle through interfaces.

```bash
# Install service
sudo cp systemd/ip-display.service /etc/systemd/system/
sudo systemctl enable ip-display
sudo systemctl start ip-display
```

### Manual Use

```bash
python3 utils/ip_display.py
```

## Troubleshooting

### I2C Device Not Found

```bash
# Check I2C is enabled
sudo raspi-config
# Interface Options > I2C > Enable

# Scan for devices
i2cdetect -y 1

# Expected output:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
# 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 70: 70 -- -- -- -- -- -- --
```

### Permission Errors

```bash
# Add user to i2c and gpio groups
sudo usermod -a -G i2c,gpio $USER

# Logout and login again
```

### OSC Not Receiving

```bash
# Check firewall
sudo ufw status
sudo ufw allow 9999/udp

# Test with Python OSC
python3 -c "
from pythonosc import udp_client
client = udp_client.SimpleUDPClient('localhost', 9999)
client.send_message('/onbody/effect/14', 0)
"
```

## Development

### Testing

```bash
# Test individual components
python3 utils/gpio_check.py
python3 utils/buzz_test.py

# Test full system
python3 src/octopulse_server.py --verbose
```

### Custom Effects

The DRV2605L has 120+ built-in effects. See the [DRV2605L datasheet](../../hardware/datasheets/DRV2605L.pdf) for the complete effect library.

## Hardware Design Files

Complete hardware design files are available in the [hardware directory](../../hardware/):

- KiCad PCB project
- Gerber files for manufacturing
- 3D enclosure models (STL)
- Bill of Materials
- Assembly instructions

## License

MIT License - see [LICENSE](../../LICENSE)
