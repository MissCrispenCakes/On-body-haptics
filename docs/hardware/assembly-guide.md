# Hardware Assembly Guide

Complete step-by-step guide for assembling On-Body Haptics hardware.

## Overview

This guide covers assembly for both hardware implementations:
- **Arduino + Bluetooth** - Portable, battery-powered system
- **Raspberry Pi + I2C** - High-fidelity haptic effects

## Prerequisites

Before starting assembly, ensure you have:

- PCB boards (ordered from manufacturer - see [PCB Fabrication Guide](pcb-fabrication.md))
- All components from [Bill of Materials](bom.md)
- 3D printed enclosures (see [Enclosure Printing Guide](enclosure-printing.md))
- Soldering equipment (iron, solder, flux)
- Multimeter for testing
- Safety glasses

## Arduino + Bluetooth Assembly

### Components Needed

- Arduino Uno or Nano
- HC-05 or HC-06 Bluetooth module
- 5x haptic motors or vibration motors
- MOSFETs or motor drivers
- Power supply (battery pack or USB)
- Connecting wires

### Assembly Steps

**Note**: Detailed step-by-step instructions with photos coming soon!

1. **Prepare the PCB**
   - Inspect PCB for manufacturing defects
   - Clean with isopropyl alcohol if needed

2. **Solder Components**
   - Start with smallest components (resistors, capacitors)
   - Add ICs and modules
   - Solder headers for Arduino
   - Add power connectors

3. **Install Motors**
   - Connect haptic motors to motor driver outputs
   - Secure motors in enclosure

4. **Connect Bluetooth Module**
   - Solder HC-05/HC-06 to UART pins
   - Ensure proper power and ground connections

5. **Testing**
   - Visual inspection of all solder joints
   - Continuity testing with multimeter
   - Power-on test (without motors first)
   - Upload test firmware

## Raspberry Pi + I2C Assembly

### Components Needed

- Raspberry Pi (3B+ or 4 recommended)
- Custom PCB (haptic-uhat)
- TCA9548A I2C multiplexer
- Up to 8x Adafruit DRV2605L breakouts
- 8x haptic motors (ERM or LRA)
- SSD1306 OLED display (optional)
- Power supply (5V 3A recommended)

### Assembly Steps

**Note**: Detailed step-by-step instructions with photos coming soon!

1. **Prepare the HAT PCB**
   - Inspect PCB for manufacturing defects
   - Test fit on Raspberry Pi

2. **Solder Components** (precision work recommended!)
   - Solder I2C multiplexer
   - Add headers for DRV2605L breakouts
   - Install OLED display header
   - Solder GPIO header for Raspberry Pi connection
   - **Special thanks to rglenn for expert soldering on prototype boards!**

3. **Connect DRV2605L Modules**
   - Insert Adafruit DRV2605L breakouts into headers
   - Verify I2C address configuration

4. **Install Motors**
   - Connect motors to DRV2605L outputs
   - Secure in enclosure or mounting positions

5. **Connect Display**
   - Solder SSD1306 OLED to I2C header
   - Test display separately before final assembly

6. **Testing**
   - Visual inspection
   - I2C address scanning
   - Individual motor tests
   - Full system integration test

## Troubleshooting

### Common Issues

**No power**
- Check power supply voltage and current rating
- Verify polarity
- Test continuity of power traces

**Motors not responding**
- Check motor driver connections
- Verify motor polarity
- Test motor driver outputs with multimeter

**Communication errors**
- Check TX/RX connections (Arduino)
- Scan I2C bus for device addresses (Raspberry Pi)
- Verify ground connections

**Weak vibration**
- Check motor voltage
- Verify PWM settings
- Test motor separately

## Safety Notes

- Always wear safety glasses when soldering
- Work in well-ventilated area
- Disconnect power before modifying connections
- Check for shorts before powering on
- Use proper current-rated power supplies

## Next Steps

After successful assembly:
- Follow [Arduino Quickstart](../getting-started/arduino-quickstart.md) or [Raspberry Pi Quickstart](../getting-started/raspberry-pi-quickstart.md)
- Configure firmware/software
- Test OSC protocol communication
- Build your haptic application!

## Need Help?

- **GitHub Discussions**: https://github.com/MissCrispenCakes/On-body-haptics/discussions
- **Issue Tracker**: https://github.com/MissCrispenCakes/On-body-haptics/issues

---

**Contributors**: Assembly documentation by MissCrispenCakes. Hardware design by MissCrispenCakes (initial) and rglenn (production PCBs).
