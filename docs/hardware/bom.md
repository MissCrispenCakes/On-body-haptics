# Bill of Materials (BOM)

Complete component list for building On-Body Haptics hardware systems.

## Overview

This BOM covers both implementations. You only need components for the system you're building:
- **Arduino + Bluetooth** - Portable wearable system
- **Raspberry Pi + I2C** - High-fidelity haptic system

**Note**: A detailed Excel spreadsheet with part numbers is available at `hardware/bom.xlsx`

## Arduino + Bluetooth System

### Electronics

| Component | Quantity | Description | Example Part | Approx. Cost |
|-----------|----------|-------------|--------------|--------------|
| Arduino Uno/Nano | 1 | Microcontroller | Arduino Uno R3 | $25 |
| HC-05 or HC-06 | 1 | Bluetooth module | HC-05 | $5-10 |
| Haptic Motors | 5 | Vibration motors | Adafruit Product 1201 | $5-10 ea |
| MOSFETs | 5 | Motor drivers | 2N7000 or similar | $0.50 ea |
| Resistors | 10 | 10kΩ pull-down | 1/4W resistor | $0.10 ea |
| Capacitors | 5 | 100µF decoupling | Electrolytic | $0.25 ea |
| Diodes | 5 | Flyback diodes | 1N4148 | $0.10 ea |
| Power Jack | 1 | Barrel jack | 2.1mm | $1 |
| USB Cable | 1 | Programming cable | USB A to B | $3 |

### Power

| Component | Quantity | Description | Approx. Cost |
|-----------|----------|-------------|--------------|
| Battery Pack | 1 | 4xAA or LiPo | $10-20 |
| Power Switch | 1 | SPST toggle | $1 |

### PCB & Assembly

| Component | Quantity | Description | Approx. Cost |
|-----------|----------|-------------|--------------|
| Custom PCB | 1 | Haptic Belt PCB | $2-5 |
| Headers | 1 set | Arduino headers | $2 |
| Connecting Wire | 1 pack | 22-24 AWG | $5 |

**Total Estimated Cost**: $100-150

## Raspberry Pi + I2C System

### Main Components

| Component | Quantity | Description | Example Part | Approx. Cost |
|-----------|----------|-------------|--------------|--------------|
| Raspberry Pi | 1 | 3B+ or 4 recommended | RPi 4 (2GB) | $45 |
| microSD Card | 1 | 16GB+ Class 10 | SanDisk 32GB | $10 |
| Power Supply | 1 | 5V 3A USB-C | Official RPi PSU | $8 |

### Custom PCB & Components

| Component | Quantity | Description | Example Part | Approx. Cost |
|-----------|----------|-------------|--------------|--------------|
| Haptic uHAT PCB | 1 | Custom PCB | From Gerbers | $2-5 |
| TCA9548A | 1 | I2C multiplexer | Adafruit 2717 | $7 |
| DRV2605L Breakouts | 8 | Haptic drivers | Adafruit 2305 | $8 ea |
| Haptic Motors | 8 | ERM or LRA motors | Included with DRV2605L | - |
| SSD1306 OLED | 1 | Display (optional) | 0.96" I2C OLED | $5 |
| GPIO Header | 1 | 2x20 female | Raspberry Pi HAT header | $2 |
| Button | 1 | Tactile switch | 6mm tactile | $0.25 |

### Hardware & Assembly

| Component | Quantity | Description | Approx. Cost |
|-----------|----------|-------------|--------------|
| M2.5 Standoffs | 4 | PCB spacers | 11mm | $2 |
| M2.5 Screws | 8 | PCB mounting | | $1 |
| Jumper Wires | 1 set | Female-Female | Dupont cables | $5 |

**Total Estimated Cost**: $150-200

## Common Components (Both Systems)

### Tools & Supplies

| Item | Description | Approx. Cost |
|------|-------------|--------------|
| Soldering Iron | Temperature controlled | $20-50 |
| Solder | 60/40 or lead-free | $5 |
| Flux | Rosin flux pen | $5 |
| Multimeter | Basic DMM | $15-30 |
| Wire Strippers | 22-24 AWG | $10 |
| Helping Hands | Soldering jig | $10 |
| Safety Glasses | PPE | $5 |

### 3D Printed Parts

| Component | Quantity | Description | Cost |
|-----------|----------|-------------|------|
| Enclosure | 1 | Raspberry Pi case | $2-5 (filament) |

**Files**: See `hardware/enclosures/raspberry-pi-case/` for STL files

## Where to Buy

### Electronics Suppliers

#### USA
- **Adafruit**: https://www.adafruit.com/ (DRV2605L, TCA9548A, quality components)
- **Digi-Key**: https://www.digikey.com/ (Large selection, fast shipping)
- **Mouser**: https://www.mouser.com/ (Professional components)
- **SparkFun**: https://www.sparkfun.com/ (Hobbyist-friendly)
- **Amazon**: https://www.amazon.com/ (Quick shipping, mixed quality)

#### International
- **AliExpress**: https://www.aliexpress.com/ (Cheapest, slow shipping)
- **Banggood**: https://www.banggood.com/ (Good for motors)
- **eBay**: https://www.ebay.com/ (Used/surplus components)

### Raspberry Pi
- **Official**: https://www.raspberrypi.com/products/
- **Distributors**: Adafruit, SparkFun, CanaKit, Amazon

### PCB Manufacturing
See [PCB Fabrication Guide](pcb-fabrication.md) for ordering custom PCBs.

## Component Notes

### Haptic Motors
- **ERM (Eccentric Rotating Mass)**: Cheaper, good vibration
- **LRA (Linear Resonant Actuator)**: Better control, crisper feedback
- Adafruit DRV2605L breakouts often include LRA motors

### Bluetooth Modules
- **HC-05**: Master/slave mode, more versatile
- **HC-06**: Slave only, simpler, cheaper
- Either works for this project (slave mode only needed)

### Capacitors
- Use electrolytic capacitors near power pins
- 100µF typical for motor driver decoupling

### Wire Gauge
- **22 AWG**: Good for most connections
- **24 AWG**: Better for tight spaces
- Use stranded for flexibility

## Cost Breakdown Summary

| System | Components | PCB | Tools (one-time) | Total |
|--------|------------|-----|------------------|-------|
| Arduino + BT | $85-120 | $10-15 | $70-115 | $165-250 |
| Raspberry Pi | $130-170 | $10-15 | $70-115 | $210-300 |

**Note**: Tool costs are one-time purchases. Additional builds only need component costs.

## Detailed Excel BOM

A detailed Excel spreadsheet with specific part numbers, supplier links, and exact pricing is available in the repository:

📄 **File**: `hardware/bom.xlsx`

This spreadsheet includes:
- Specific part numbers
- Direct supplier links
- Current pricing (updated periodically)
- Alternative part options
- Bulk purchase discounts

## Bulk Purchasing

If building multiple units:
- Order 10+ of each component for discounts
- PCB prices drop significantly at 10-50 boards
- Consider group buys with other makers

## Questions?

- **Component Selection**: Ask in [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)
- **Substitutions**: Most components have acceptable alternatives
- **Sourcing Help**: Open an [issue](https://github.com/MissCrispenCakes/On-body-haptics/issues)

---

**Assembly**: See [Assembly Guide](assembly-guide.md) after ordering components
