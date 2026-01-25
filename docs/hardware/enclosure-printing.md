# 3D Enclosure Printing Guide

How to 3D print enclosures for On-Body Haptics hardware.

## Overview

3D printable enclosures are provided for the Raspberry Pi haptic system. These protect the electronics and provide mounting points for batteries and wearable attachment.

**Design Credits**:
- **Initial OpenSCAD design**: MissCrispenCakes
- **Sample prints with battery compartment**: rglenn ([@rglenn](https://github.com/rglenn)) - A wonderful surprise!

## Available Enclosures

### Raspberry Pi Case
- **Location**: `hardware/enclosures/raspberry-pi-case/`
- **Files**:
  - `picase.scad` - OpenSCAD source (editable, parametric)
  - `picase.stl` - Ready-to-print 3D model
- **Features**:
  - Fits Raspberry Pi 3B+ or 4
  - Battery compartment for portable operation
  - Mounting holes for Haptic uHAT
  - Cutouts for GPIO, USB, HDMI, power

### Future Enclosures
- Arduino belt enclosure (coming soon!)
- Motor mounting brackets
- Wearable attachment clips

## Quick Start

### Option 1: Download & Print STL (Easiest)

1. Download `picase.stl` from repository
2. Open in your slicer (Cura, PrusaSlicer, etc.)
3. Use recommended settings below
4. Print!

### Option 2: Customize OpenSCAD Design

1. Download `picase.scad`
2. Install OpenSCAD (https://openscad.org/)
3. Open file and modify parameters
4. Export to STL
5. Print!

## Recommended Print Settings

### Material Choice

| Material | Pros | Cons | Best For |
|----------|------|------|----------|
| **PLA** | Easy to print, cheap, rigid | Heat sensitive | Prototypes, indoor use |
| **PETG** | Strong, heat resistant | Harder to print | Wearables, outdoor |
| **ABS** | Very strong, heat resistant | Requires heated bed, fumes | Durable enclosures |
| **TPU** | Flexible, shock absorbing | Difficult to print | Wearable padding |

**Recommended**: PETG for final builds, PLA for testing

### Slicer Settings

#### Basic Settings
- **Layer Height**: 0.2mm (standard) or 0.15mm (higher quality)
- **Wall Thickness**: 1.2mm (3 perimeters at 0.4mm nozzle)
- **Infill**: 20% (gyroid or grid pattern)
- **Print Speed**: 50-60mm/s
- **Nozzle Temperature**:
  - PLA: 200-210°C
  - PETG: 230-240°C
- **Bed Temperature**:
  - PLA: 60°C
  - PETG: 80°C

#### Advanced Settings
- **Top/Bottom Layers**: 4-5 layers
- **Supports**: **YES** - Enable for overhangs
  - **Support Pattern**: Grid or Lines
  - **Support Density**: 15%
  - **Support Z Distance**: 0.2mm
- **Adhesion**: Brim (5-10mm) recommended for PETG
- **Cooling**:
  - PLA: 100% after first layer
  - PETG: 50% (less cooling for better layer adhesion)

## Printing Instructions

### Step 1: Prepare the File

1. Download `picase.stl` from `hardware/enclosures/raspberry-pi-case/`
2. Open in your slicer software

### Step 2: Orient the Model

- Place flat side on build plate
- Check for overhangs (red areas in slicer)
- Enable supports if needed

### Step 3: Slice and Check

1. Apply recommended settings
2. Click "Slice"
3. Review print time and material usage
4. Check layer view for issues
5. Look for:
   - Proper support placement
   - No gaps in walls
   - Solid top/bottom surfaces

### Step 4: Print

1. Ensure bed is level and clean
2. Apply adhesive if needed (glue stick for PLA, none for PETG on PEI)
3. Start print
4. Monitor first layer closely
5. Check periodically for failures

### Step 5: Post-Processing

1. **Remove from bed** - Wait until cool, gently peel off
2. **Remove supports** - Use pliers or flush cutters
3. **Test fit** - Check if Raspberry Pi fits
4. **Clean holes** - Use drill bit to clean mounting holes if needed
5. **Smooth surfaces** (optional):
   - Sand with 220-400 grit sandpaper
   - Heat gun for PLA (careful!)
   - Acetone vapor for ABS

## Customizing the Design

### Using OpenSCAD

The `picase.scad` file is parametric, allowing easy modifications:

```openscad
// Example parameters (edit these)
case_length = 100;      // Length in mm
case_width = 70;        // Width in mm
case_height = 40;       // Height in mm
wall_thickness = 2;     // Wall thickness
mounting_hole_dia = 3;  // Hole diameter
```

**Common Modifications**:
- Adjust size for different Raspberry Pi models
- Add custom cutouts for buttons/connectors
- Modify battery compartment size
- Add wearable attachment points

### Exporting Modified Design

1. Edit parameters in OpenSCAD
2. Press F5 to preview
3. Press F6 to render
4. File → Export → Export as STL
5. Import STL into slicer and print

## Battery Compartment

rglenn's sample prints include a battery compartment feature:

- **Battery Type**: Typically holds 18650 cells or AA battery pack
- **Location**: Bottom or side of enclosure
- **Access**: Sliding cover or snap-fit lid
- **Wiring**: Grommet or channel for wires to PCB

**Note**: Exact battery compartment specifications depend on your battery choice. See OpenSCAD source to customize.

## Print Time & Cost Estimates

| Enclosure | Material | Time | Cost |
|-----------|----------|------|------|
| Raspberry Pi Case | ~50g PLA | 3-5 hours | $1-2 |
| Raspberry Pi Case | ~50g PETG | 4-6 hours | $2-3 |

**Note**: Times assume 0.2mm layer height, 50mm/s speed

## Troubleshooting

### Print Won't Stick
**Problem**: Print detaching from bed
- **Solution**: Increase bed temperature
- **Solution**: Clean bed with IPA
- **Solution**: Add brim or raft
- **Solution**: Level bed

### Warping
**Problem**: Corners lifting up
- **Solution**: Use heated bed
- **Solution**: Increase bed temperature
- **Solution**: Reduce cooling fan speed
- **Solution**: Add brim

### Supports Hard to Remove
**Problem**: Supports fused to print
- **Solution**: Increase Z-distance in slicer
- **Solution**: Use different support pattern
- **Solution**: Print support interface layers

### Layers Not Bonding
**Problem**: Layers separating
- **Solution**: Increase nozzle temperature
- **Solution**: Reduce print speed
- **Solution**: Check for drafts/cold room

### Holes Too Tight
**Problem**: Screws or components don't fit
- **Solution**: Scale holes up by 5% in slicer
- **Solution**: Drill out holes with appropriate bit
- **Solution**: Adjust hole diameter in OpenSCAD

## Printing Services

Don't have a 3D printer? Use these services:

- **Shapeways**: https://www.shapeways.com/
- **Craftcloud**: https://craftcloud3d.com/
- **Local maker spaces**: Check your area
- **University fab labs**: Often open to public
- **Library makerspaces**: Many public libraries have 3D printers

## Assembly After Printing

Once your enclosure is printed:

1. See [Assembly Guide](assembly-guide.md) for full assembly
2. Install Raspberry Pi with standoffs
3. Mount Haptic uHAT on top
4. Install battery if using battery compartment
5. Route cables neatly
6. Close enclosure and secure

## Contributing Designs

Made an improvement? Share it!

1. Export your modified STL
2. Include OpenSCAD source if available
3. Add photos
4. Open a pull request
5. Document changes in PR description

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Questions?

- **Printing Issues**: Ask in [GitHub Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)
- **Design Modifications**: Open an [issue](https://github.com/MissCrispenCakes/On-body-haptics/issues)
- **Sharing Improvements**: Submit a pull request!

---

**Design Credits**: Initial design by MissCrispenCakes | Battery compartment samples by rglenn
