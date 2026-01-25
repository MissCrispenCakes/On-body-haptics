# Component Datasheets

This directory contains datasheets for key components used in On-Body Haptics hardware.

## DRV2605L Haptic Driver

**File**: DRV2605L.pdf (not included in repository due to size/licensing)

**Download from**: https://www.ti.com/product/DRV2605L

**Direct PDF link**: https://www.ti.com/lit/ds/symlink/drv2605l.pdf

### Key Specifications

- 2.5V to 5.2V operation
- I2C interface (up to 400 kHz)
- Built-in library of 120+ haptic effects
- ERM and LRA motor support
- PWM input for analog control

## TCA9548A I2C Multiplexer

**Download from**: https://www.ti.com/product/TCA9548A

**Direct PDF link**: https://www.ti.com/lit/ds/symlink/tca9548a.pdf

### Key Specifications

- 8-channel I2C multiplexer
- 1.65V to 5.5V operation
- 400 kHz I2C speed
- Hot insertion support

## Other Components

Additional component datasheets can be found from the manufacturers listed in the [Bill of Materials](../../docs/hardware/bom.md).

## Usage

These datasheets are referenced by:
- [OSC Protocol Specification](../../docs/api/osc-protocol.md) - DRV2605L effect codes
- [Assembly Guide](../../docs/hardware/assembly-guide.md) - Pinouts and connections
- [Raspberry Pi Quickstart](../../docs/getting-started/raspberry-pi-quickstart.md) - I2C addresses

## License Note

Datasheets are copyright their respective manufacturers (Texas Instruments, etc.) and are provided here as reference links only.
