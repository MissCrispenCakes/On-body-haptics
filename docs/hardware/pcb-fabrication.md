# PCB Fabrication Guide

How to order custom PCBs for On-Body Haptics from online manufacturers.

## Overview

This project includes production-ready PCB designs with Gerber files for manufacturing:
- **Haptic Belt PCB** - Wearable belt version
- **Haptic uHAT PCB** - Raspberry Pi HAT version

**PCB Design Credits**: Production Gerber files and KiCad layouts by rglenn ([@rglenn](https://github.com/rglenn))

## PCB Files Location

Find the manufacturing files in the repository:

```
hardware/pcb/haptic-belt/gerbers/
hardware/pcb/haptic-uhat/gerbers/
```

## Recommended Manufacturers

We recommend these PCB fabrication services (listed in order of typical cost, lowest first):

### 1. JLCPCB (China) - Budget Friendly
- **Website**: https://jlcpcb.com/
- **Minimum Order**: 5 PCBs
- **Typical Cost**: $2-10 for 5 boards + shipping
- **Shipping Time**: 1-2 weeks to USA
- **Quality**: Good for prototypes
- **Notes**: Often the cheapest option, fast turnaround

### 2. PCBWay (China) - Mid-Range
- **Website**: https://www.pcbway.com/
- **Minimum Order**: 5 PCBs
- **Typical Cost**: $5-15 for 5 boards + shipping
- **Shipping Time**: 1-2 weeks to USA
- **Quality**: Excellent, good customer service
- **Notes**: Slightly higher quality than JLCPCB

### 3. OSH Park (USA) - Premium Domestic
- **Website**: https://oshpark.com/
- **Minimum Order**: 3 PCBs
- **Typical Cost**: $15-30 for 3 boards (free shipping USA)
- **Shipping Time**: 2-3 weeks
- **Quality**: Excellent, purple solder mask
- **Notes**: USA-made, open source friendly, no shipping charges

### 4. Other Options
- **Seeed Studio**: https://www.seeedstudio.com/fusion_pcb.html
- **ALLPCB**: https://www.allpcb.com/
- **Elecrow**: https://www.elecrow.com/pcb-manufacturing.html

## Ordering Steps

### Step 1: Choose Your PCB

Decide which design you need:
- **Arduino + Bluetooth system** → Haptic Belt PCB
- **Raspberry Pi + I2C system** → Haptic uHAT PCB

### Step 2: Download Gerber Files

From the repository:
- Haptic Belt: `hardware/pcb/haptic-belt/gerbers/haptic-belt.zip`
- Haptic uHAT: `hardware/pcb/haptic-uhat/gerbers/haptic-uhat.zip`

**Do NOT unzip the file** - manufacturers want the zipped Gerber files.

### Step 3: Upload to Manufacturer

1. Go to manufacturer website (e.g., https://jlcpcb.com/)
2. Click "Order Now" or "Quote Now"
3. Click "Add Gerber file" and upload the .zip file
4. Wait for automatic Gerber parsing

### Step 4: Configure PCB Options

Use these recommended settings:

#### Basic Settings
- **PCB Dimensions**: Auto-detected from Gerber
- **Layers**: 2
- **PCB Thickness**: 1.6mm (standard)
- **PCB Qty**: 5 (or manufacturer minimum)

#### Surface & Material
- **Material**: FR-4 (standard)
- **Surface Finish**: HASL (lead-free) or ENIG
  - **HASL**: Cheaper, good for most uses
  - **ENIG**: More expensive, better for fine pitch soldering
- **Copper Weight**: 1 oz

#### Solder Mask & Silkscreen
- **Solder Mask Color**: Green (or your preference)
- **Silkscreen Color**: White (standard)
- **Remove Order Number**: Optional (usually adds $1.50)

#### Advanced Options (Usually Default is Fine)
- **Gold Fingers**: No
- **Edge Connector**: No
- **Castellated Holes**: No

### Step 5: Review & Checkout

1. Review the PCB preview (usually shows 2D/3D view)
2. Check dimensions match your design
3. Verify number of layers (should be 2)
4. Check price and lead time
5. Add to cart and checkout

### Step 6: Wait for Manufacturing

- **Fabrication**: 24-72 hours typically
- **Shipping**:
  - China (JLCPCB/PCBWay): 1-2 weeks standard, 3-5 days express
  - USA (OSH Park): 2-3 weeks

### Step 7: Inspect Upon Arrival

When your PCBs arrive:
1. Count boards (should match your order)
2. Inspect for obvious defects (scratches, broken traces)
3. Check dimensions with calipers if available
4. Look for solder mask quality
5. Verify all holes are drilled correctly

## PCB Specifications Summary

### Haptic Belt PCB
- **Size**: (TBD - check Gerber files)
- **Layers**: 2
- **Thickness**: 1.6mm
- **Finish**: HASL or ENIG
- **Special Features**: None

### Haptic uHAT PCB
- **Size**: Raspberry Pi HAT form factor
- **Layers**: 2
- **Thickness**: 1.6mm
- **Finish**: HASL or ENIG
- **Special Features**: RPi mounting holes, GPIO header

## Cost Estimates

Typical costs for 5 boards (JLCPCB standard shipping):

| PCB Type | Fabrication | Shipping | Total |
|----------|-------------|----------|-------|
| Haptic Belt | $2-5 | $5-8 | ~$10-15 |
| Haptic uHAT | $2-5 | $5-8 | ~$10-15 |

**Note**: Prices vary by manufacturer and shipping method. Express shipping can add $20-40.

## Troubleshooting

### Gerber Upload Errors
**Problem**: "Invalid Gerber file" or parsing error
- **Solution**: Re-download the .zip file, don't unzip it
- **Solution**: Try a different manufacturer's uploader

### Wrong PCB Size Detected
**Problem**: Dimensions don't match expected size
- **Solution**: Check you uploaded the correct .zip file
- **Solution**: Contact manufacturer support

### Price Higher Than Expected
**Problem**: Quote is much higher than estimates
- **Possible Reasons**:
  - Express shipping selected
  - Special finish (gold plating, ENIG)
  - "Remove order number" option selected
  - Wrong thickness or layers

## Assembly After Fabrication

Once you receive your PCBs:
1. See [Bill of Materials](bom.md) for component ordering
2. Follow [Assembly Guide](assembly-guide.md) for soldering
3. Check [Getting Started](../getting-started/choosing-platform.md) for firmware setup

## Questions?

- **PCB Design Issues**: Open an [issue on GitHub](https://github.com/MissCrispenCakes/On-body-haptics/issues)
- **Manufacturing Questions**: Contact the PCB manufacturer directly
- **Assembly Help**: Check our [Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)

---

**PCB Design**: Production Gerbers by rglenn | Initial design by MissCrispenCakes
