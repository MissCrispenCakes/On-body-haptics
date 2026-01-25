# Hardware Designs

All hardware in this directory is licensed under **CERN-OHL-P v2** (CERN Open Hardware License - Permissive).

See [LICENSE-HARDWARE](../LICENSE-HARDWARE) for full license text.

**OSHWA Certified Ready**: This hardware uses an [OSHWA-approved license](https://oshwa.org/) and meets all requirements for Open Source Hardware certification. See [OSHWA Certification Guide](../docs/OSHWA_CERTIFICATION.md) for details.

## Contents

### PCB Designs (`pcb/`)
- **haptic-belt/** - Wearable haptic belt PCB
- **haptic-uhat/** - Raspberry Pi HAT for haptic control

Each includes:
- KiCad project files (`.kicad_pcb`, `.sch`, `.pro`)
- Gerber files for manufacturing (in `gerbers/` subdirectory)
- Schematic PDFs and assembly photos (in `docs/` subdirectory)

### 3D Enclosures (`enclosures/`)
- **raspberry-pi-case/** - 3D printable enclosure for Raspberry Pi setup
  - Source: OpenSCAD (`.scad`)
  - Ready to print: STL files

### Bill of Materials
- **bom.xlsx** - Complete component list with part numbers and suppliers

### Datasheets (`datasheets/`)
- Component datasheets for reference

## Manufacturing

### PCB Fabrication

1. **Choose your PCB**:
   - `hardware/pcb/haptic-belt/gerbers/haptic-belt.zip` - Belt version
   - `hardware/pcb/haptic-uhat/gerbers/haptic-uhat.zip` - Raspberry Pi HAT

2. **Upload to PCB manufacturer**:
   - JLCPCB: https://jlcpcb.com/
   - PCBWay: https://www.pcbway.com/
   - OSH Park: https://oshpark.com/

3. **Settings**:
   - Layers: 2
   - Thickness: 1.6mm
   - Surface Finish: HASL or ENIG
   - Copper Weight: 1oz

See [docs/hardware/pcb-fabrication.md](../docs/hardware/pcb-fabrication.md) for detailed instructions.

### 3D Printing

1. **Files**: `hardware/enclosures/raspberry-pi-case/picase.stl`
2. **Settings**:
   - Material: PLA or PETG
   - Layer Height: 0.2mm
   - Infill: 20%
   - Supports: Yes (for overhangs)

See [docs/hardware/enclosure-printing.md](../docs/hardware/enclosure-printing.md) for detailed instructions.

## Modifications

You are free to modify these designs under CERN-OHL-P v2. If you make improvements, please consider:
- Sharing them back (pull request)
- Documenting your changes
- Maintaining attribution

## Source Location

As required by CERN-OHL-P v2 section 4:

**Source Location**: https://github.com/MissCrispenCakes/On-body-haptics

If you manufacture hardware based on these designs, you must maintain this source location visible in documentation or on the product.

## Attribution

**Hardware Designers:**
- **Initial design & prototypes**: MissCrispenCakes
- **Production PCB files & Gerbers**: rglenn ([@rglenn](https://github.com/rglenn))
- **3D enclosures**: MissCrispenCakes (initial designs), rglenn (sample prints with battery compartment)

When sharing or manufacturing these designs, please include:
```
Based on On-Body Haptics by MissCrispenCakes & rglenn
https://github.com/MissCrispenCakes/On-body-haptics
Licensed under CERN-OHL-P v2

Production PCB designs by rglenn
Initial hardware design by MissCrispenCakes
```

## Questions?

- Hardware assembly guide: [docs/hardware/assembly-guide.md](../docs/hardware/assembly-guide.md)
- General questions: [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)
- Issues: [GitHub Issues](https://github.com/MissCrispenCakes/On-body-haptics/issues)
