# Raspberry Pi + I2C Quick Start

Get your Raspberry Pi haptic system running in 15 minutes.

## What You'll Build

A high-fidelity haptic system with 8 independent channels, 120+ haptic effects, WiFi control, and OLED display.

**Time**: 15-30 minutes (plus OS installation)
**Difficulty**: ⭐⭐⭐⭐ Advanced

## Prerequisites

### Hardware Required

- **Raspberry Pi 3/4/Zero 2W** (~$35-55)
- **TCA9548A I2C Multiplexer** (~$5-8)
- **8x Adafruit DRV2605L Haptic Drivers** (~$7 each = $56)
- **8x Linear Resonant Actuators (LRAs)** (~$3 each = $24)
- **SSD1306 OLED Display** (128x32, I2C) (~$5)
- **Push button** (for display control) (~$0.50)
- **MicroSD card** (16GB+) (~$8)
- **USB power supply** (2.4A+) (~$10)
- **Breadboard/PCB and wires** (~$10)

**Total Cost**: ~$150-180

### Optional

- Custom PCB (Gerber files provided in `hardware/pcb/`)
- 3D printed enclosure (STL files in `hardware/enclosures/`)
- USB power bank for portability

### Software Required

- **Raspberry Pi OS Lite** (or Desktop) - [Download here](https://www.raspberrypi.com/software/)
- **Raspberry Pi Imager** - [Download here](https://www.raspberrypi.com/software/)

## Step 1: Set Up Raspberry Pi OS (10 minutes)

### 1.1 Flash OS to SD Card

1. **Download Raspberry Pi Imager**
2. **Insert SD card** into your computer
3. **Open Imager** and select:
   - **OS**: Raspberry Pi OS Lite (64-bit) or Desktop
   - **Storage**: Your SD card
4. **Click gear icon** ⚙️ for advanced options:
   - ✅ Enable SSH
   - ✅ Set username/password (e.g., `pi` / `YourSecurePassword`)
   - ✅ Configure WiFi (SSID and password)
   - ✅ Set locale/timezone
5. **Click Write** and wait

### 1.2 Boot Raspberry Pi

1. **Insert SD card** into Raspberry Pi
2. **Connect power** (wait 30-60 seconds for first boot)
3. **Find IP address**:
   - Check your router's connected devices
   - Or use: `ping raspberrypi.local`

### 1.3 SSH into Raspberry Pi

```bash
ssh pi@raspberrypi.local
# Or use IP: ssh pi@192.168.1.100

# First login: change password
passwd
```

⚠️ **CRITICAL SECURITY**: Change default password immediately!

## Step 2: Enable I2C (2 minutes)

### 2.1 Configure I2C

```bash
sudo raspi-config
```

Navigate:
1. **Interface Options** → **I2C** → **Yes**
2. **Finish** and **Reboot**

Or use command line:
```bash
sudo raspi-config nonint do_i2c 0
sudo reboot
```

### 2.2 Verify I2C Enabled

After reboot:

```bash
lsmod | grep i2c
# Should show: i2c_bcm2835 or similar
```

## Step 3: Wire the Hardware (15 minutes)

### I2C Address Map

| Device | I2C Address | Bus |
|--------|-------------|-----|
| TCA9548A Multiplexer | 0x70 | I2C1 |
| SSD1306 OLED | 0x3C | I2C1 (main bus) |
| DRV2605L #0 | 0x5A | Mux channel 0 |
| DRV2605L #1 | 0x5A | Mux channel 1 |
| ... | 0x5A | ... |
| DRV2605L #7 | 0x5A | Mux channel 7 |

### Raspberry Pi GPIO Pinout

```
Raspberry Pi GPIO (BCM numbering):
┌─────────────────┐
│  3.3V  (Pin 1)  ├──► Power for I2C devices
│  5V    (Pin 2)  ├──► Power for DRV2605L (if needed)
│  SDA   (GPIO 2) ├──► TCA9548A SDA & OLED SDA
│  SCL   (GPIO 3) ├──► TCA9548A SCL & OLED SCL
│  GPIO 17        ├──► Button for OLED display
│  GND   (Pin 6)  ├──► Common ground
└─────────────────┘
```

### Wiring Diagram

```
Raspberry Pi I2C Bus:
  SDA (GPIO 2) ──┬──► TCA9548A SDA
                 └──► SSD1306 OLED SDA

  SCL (GPIO 3) ──┬──► TCA9548A SCL
                 └──► SSD1306 OLED SCL

TCA9548A Multiplexer:
  Channel 0 ──► DRV2605L #0 (SDA/SCL)
  Channel 1 ──► DRV2605L #1 (SDA/SCL)
  Channel 2 ──► DRV2605L #2 (SDA/SCL)
  ...
  Channel 7 ──► DRV2605L #7 (SDA/SCL)

Each DRV2605L:
  OUT+ / OUT- ──► Linear Resonant Actuator (LRA)

OLED Button:
  GPIO 17 ──► Button ──► GND (with internal pull-up)
```

### Detailed Connections

#### TCA9548A I2C Multiplexer

| TCA9548A Pin | Raspberry Pi Pin | Notes |
|--------------|------------------|-------|
| VCC | 3.3V (Pin 1) | Power |
| GND | GND (Pin 6) | Ground |
| SDA | GPIO 2 (Pin 3) | I2C Data |
| SCL | GPIO 3 (Pin 5) | I2C Clock |
| A0, A1, A2 | GND | Address: 0x70 (default) |

#### SSD1306 OLED Display

| OLED Pin | Raspberry Pi Pin |
|----------|------------------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 2 (shared with TCA9548A) |
| SCL | GPIO 3 (shared with TCA9548A) |

#### Each DRV2605L (x8)

Connect to TCA9548A channels 0-7:

| DRV2605L Pin | Connection |
|--------------|------------|
| VIN | 3.3V or 5V (check board voltage) |
| GND | GND |
| SDA | TCA9548A SDx (channel 0-7) |
| SCL | TCA9548A SCx (channel 0-7) |
| OUT+ | LRA positive |
| OUT- | LRA negative |

#### Button

| Button | Connection |
|--------|------------|
| One side | GPIO 17 |
| Other side | GND |

(Code uses internal pull-up resistor)

### Quick Breadboard Tips

- Use **short wires** for I2C connections (reduce noise)
- **Common ground** for all devices
- **Power distribution** - Use breadboard power rails
- **Label channels** - Keep track of which DRV2605L is which

## Step 4: Install Software (5 minutes)

### 4.1 Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 4.2 Install Dependencies

```bash
# I2C tools
sudo apt-get install -y i2c-tools python3-pip python3-dev

# Python 3 should already be installed
python3 --version  # Should be 3.7+
```

### 4.3 Clone Repository

```bash
cd ~
git clone https://github.com/yourusername/On-body-haptics.git
cd On-body-haptics/implementations/raspberry-pi-i2c/firmware
```

### 4.4 Install Python Packages

```bash
pip3 install -r requirements.txt
```

This installs:
- Adafruit CircuitPython libraries (DRV2605L, TCA9548A, SSD1306)
- python-osc
- netifaces
- RPi.GPIO
- Pillow (for OLED)

Installation takes 2-5 minutes.

## Step 5: Test I2C Devices (5 minutes)

### 5.1 Scan I2C Bus

```bash
i2cdetect -y 1
```

Expected output:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 -- -- -- -- -- -- --
```

You should see:
- **0x3c** - SSD1306 OLED
- **0x70** - TCA9548A Multiplexer

### 5.2 Test GPIO

```bash
python3 utils/gpio_check.py
```

Should output GPIO pin status.

### 5.3 Test DRV2605L Boards

```bash
python3 utils/buzz_test.py
```

This cycles through all 8 channels, triggering a haptic effect on each. You should feel vibrations!

If any channel doesn't work:
- Check wiring
- Verify DRV2605L power
- Check LRA connections

## Step 6: Configure Server (3 minutes)

### 6.1 Create Local Configuration

```bash
cd src
cp config_example.py config_local.py
nano config_local.py  # or vim/vi
```

### 6.2 Customize Settings (Optional)

Basic settings are fine for most users. Optionally adjust:

```python
# Change OSC port if needed
OSC_RECEIVE_PORT = 9999

# Disable OLED if not installed
OLED_ENABLED = False

# Change button pin if using different GPIO
BUTTON_PIN = 17

# Enable debug logging
LOG_LEVEL = "DEBUG"
VERBOSE_OSC = True
```

Save and exit.

## Step 7: Run the Server (2 minutes)

### 7.1 Start Server Manually

```bash
python3 src/octopulse_server.py
```

You should see:
```
Octopulse Haptic Server v2.0.0
Initializing I2C devices...
✓ TCA9548A multiplexer found at 0x70
✓ DRV2605L channel 0 initialized
✓ DRV2605L channel 1 initialized
...
✓ DRV2605L channel 7 initialized
✓ OLED display initialized
OSC Server listening on 0.0.0.0:9999
Ready to receive haptic commands!
```

### 7.2 Test OLED Display (if installed)

Press the button connected to GPIO 17. The OLED should cycle through network interfaces showing IP addresses.

## Step 8: Send Your First Haptic Effect! (2 minutes)

### From Your Computer

On your **development computer** (not the Raspberry Pi):

#### Option A: Python

```bash
pip install python-osc
```

Create `test_haptics.py`:

```python
from pythonosc import udp_client
import time

# Replace with your Raspberry Pi's IP
client = udp_client.SimpleUDPClient("192.168.1.100", 9999)

print("Testing haptic effects...")

# Test each channel
for channel in range(8):
    print(f"Channel {channel}: Strong click")
    client.send_message("/onbody/effect/14", channel)
    time.sleep(0.5)

# Test different effects
effects = [14, 15, 18, 20, 33]  # Click, sharp, bump, double, pulse
for effect in effects:
    print(f"Effect {effect} on all channels")
    client.send_message(f"/onbody/effect/{effect}")
    time.sleep(1)

print("Test complete!")
```

Run it:
```bash
python test_haptics.py
```

#### Option B: Command Line

```bash
# Install OSC tools
sudo apt-get install liblo-tools  # Linux
brew install liblo                 # macOS

# Send effects
oscsend 192.168.1.100 9999 /onbody/effect/14 i 0   # Channel 0
oscsend 192.168.1.100 9999 /onbody/effect/14 i 3   # Channel 3
oscsend 192.168.1.100 9999 /onbody/effect/33       # All channels
```

### From the Raspberry Pi Itself

```bash
# In a new SSH session or terminal
cd ~/On-body-haptics/implementations/raspberry-pi-i2c/firmware

# Test script
python3 -c "
from pythonosc import udp_client
import time

client = udp_client.SimpleUDPClient('localhost', 9999)

for ch in range(8):
    print(f'Testing channel {ch}')
    client.send_message('/onbody/effect/14', ch)
    time.sleep(0.5)
"
```

## 🎉 Success!

If you felt haptic effects, congratulations! Your system is working!

## Step 9: Set Up Auto-Start (Optional, 5 minutes)

### 9.1 Install Systemd Service

```bash
cd ~/On-body-haptics/implementations/raspberry-pi-i2c/firmware

# Copy service file
sudo cp systemd/octopulse-server.service /etc/systemd/system/

# Edit paths if needed
sudo nano /etc/systemd/system/octopulse-server.service
```

Verify the `WorkingDirectory` and `ExecStart` paths match your installation:

```ini
[Service]
User=pi
WorkingDirectory=/home/pi/On-body-haptics/implementations/raspberry-pi-i2c/firmware
ExecStart=/usr/bin/python3 src/octopulse_server.py
```

### 9.2 Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable octopulse-server

# Start service now
sudo systemctl start octopulse-server

# Check status
sudo systemctl status octopulse-server
```

### 9.3 View Logs

```bash
# Real-time logs
sudo journalctl -u octopulse-server -f

# Recent logs
sudo journalctl -u octopulse-server -n 50
```

### 9.4 Control Service

```bash
# Stop
sudo systemctl stop octopulse-server

# Restart
sudo systemctl restart octopulse-server

# Disable auto-start
sudo systemctl disable octopulse-server
```

## Step 10: Optional - OLED IP Display Auto-Start

```bash
# Install IP display service
sudo cp systemd/ip-display.service /etc/systemd/system/
sudo systemctl enable ip-display
sudo systemctl start ip-display
```

Now the OLED will show the IP address on boot automatically!

## Next Steps

### Explore DRV2605L Effects

The DRV2605L has 123 effects. Common ones:

```python
# Clicks
client.send_message("/onbody/effect/14", 0)  # Strong click
client.send_message("/onbody/effect/15", 0)  # Sharp click

# Bumps
client.send_message("/onbody/effect/18", 0)  # Soft bump

# Patterns
client.send_message("/onbody/effect/20", 0)  # Double click
client.send_message("/onbody/effect/30", 0)  # Triple click
client.send_message("/onbody/effect/33", 0)  # Pulsing

# Ramps
client.send_message("/onbody/effect/64", 0)  # Ramp up long
client.send_message("/onbody/effect/70", 0)  # Ramp down long
```

See [DRV2605L datasheet](../../hardware/datasheets/DRV2605L.pdf) for complete effect library.

### Create Custom Patterns

Edit `src/octopulse_server.py` to add custom pattern sequences:

```python
def custom_wave_pattern(client):
    """Create a wave pattern across all channels"""
    for ch in range(8):
        client.send_message("/onbody/effect/14", ch)
        time.sleep(0.1)
```

### Make It Wearable

1. **Use custom PCB** - Gerber files in `hardware/pcb/haptic-uhat/`
2. **3D print enclosure** - STL files in `hardware/enclosures/raspberry-pi-case/`
3. **Add power bank** - Use 2.4A+ USB power bank
4. **Position actuators** - Mount around belt/band with equal spacing

## Troubleshooting

### I2C Devices Not Detected

```bash
# Check I2C is enabled
sudo raspi-config
# Interface Options → I2C → Enabled

# Check for device conflicts
sudo i2cdetect -y 1

# Check kernel module
lsmod | grep i2c
```

### Permission Errors

```bash
# Add user to i2c and gpio groups
sudo usermod -a -G i2c,gpio $USER

# Logout and login again
logout
```

### OLED Not Working

```bash
# Check address (should be 0x3c)
i2cdetect -y 1

# Test OLED directly
python3 utils/ip_display.py
```

### DRV2605L Not Responding

- Check power supply (needs stable 3.3V or 5V)
- Verify I2C wiring (SDA/SCL)
- Check multiplexer channel selection
- Test with multimeter on LRA outputs

### OSC Not Receiving

```bash
# Check server is running
sudo systemctl status octopulse-server

# Check firewall (if enabled)
sudo ufw allow 9999/udp

# Test locally first
python3 -c "
from pythonosc import udp_client
client = udp_client.SimpleUDPClient('localhost', 9999)
client.send_message('/onbody/effect/14', 0)
"
```

### No Haptic Sensation

1. **Check LRA connections** - Verify polarity (doesn't matter but should be consistent)
2. **Test effect IDs** - Some effects are subtle, try effect 14 (strong click)
3. **Check DRV2605L library setting** - Should be set to LRA (library 2)
4. **Verify voltage settings** - Adjust in `config_local.py` if needed

### High Latency

- Use wired Ethernet instead of WiFi
- Reduce network hops
- Check CPU usage: `top` or `htop`
- Disable unnecessary services

## Integration Examples

### Max/MSP

```
[udpsend raspberrypi.local 9999]
|
[prepend /onbody/effect/14]
|
[0( [1( [2( [3( [4( [5( [6( [7(
```

### TouchDesigner

```python
# In Execute DAT
def onValueChange(channel, sampleIndex, val, prev):
    op('oscout1').sendOSC('/onbody/effect/14', [channel])
```

### Unity

```csharp
using UnityEngine;
using OscCore;

public class HapticController : MonoBehaviour {
    OscClient client;

    void Start() {
        client = new OscClient("raspberrypi.local", 9999);
    }

    public void TriggerHaptic(int channel, int effect) {
        client.Send($"/onbody/effect/{effect}", channel);
    }
}
```

## Performance Tips

- **Wired connection** - Use Ethernet for lowest latency
- **Disable WiFi power save** - `sudo iwconfig wlan0 power off`
- **Use Raspberry Pi 4** - Better performance than Pi 3 or Zero
- **Minimize services** - Use Raspberry Pi OS Lite
- **Monitor CPU** - Should be under 50% during normal use

## Further Reading

- [OSC Protocol Specification](../api/osc-protocol.md)
- [DRV2605L Effects Library](../api/raspberry-pi-api.md)
- [Hardware Assembly Guide](../hardware/assembly-guide.md)
- [PCB Fabrication Guide](../hardware/pcb-fabrication.md)

## Get Help

- [GitHub Discussions](https://github.com/yourusername/On-body-haptics/discussions)
- [Report Issues](https://github.com/yourusername/On-body-haptics/issues)

---

**Enjoy your high-fidelity haptic system!** Share your projects in [Discussions](https://github.com/yourusername/On-body-haptics/discussions/categories/show-and-tell)! 🎉
