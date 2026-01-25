# Haptic Belt PCB

Wearable haptic belt printed circuit board design.

## Design Credits

- **Initial concept & prototype**: MissCrispenCakes
- **Production PCB design**: rglenn ([@rglenn](https://github.com/rglenn))
- **KiCad layout**: rglenn
- **Gerber files for manufacturing**: rglenn

## License

Licensed under **CERN-OHL-P v2** (CERN Open Hardware License - Permissive)

See [LICENSE-HARDWARE](../../../LICENSE-HARDWARE) for full license text.

## Files

- **kicad/** - KiCad project files (.kicad_pcb, .sch, .pro)
- **gerbers/** - Manufacturing-ready Gerber files
- **docs/** - Schematics, assembly photos, and documentation

## Manufacturing

The Gerber files in the `gerbers/` directory are ready for PCB fabrication at:
- JLCPCB (https://jlcpcb.com/)
- PCBWay (https://www.pcbway.com/)
- OSH Park (https://oshpark.com/)

### Recommended Settings

- **Layers**: 2
- **Thickness**: 1.6mm
- **Surface Finish**: HASL or ENIG
- **Copper Weight**: 1oz

See [hardware assembly guide](../../../docs/hardware/assembly-guide.md) for complete build instructions.

## Attribution

When manufacturing or sharing this design, please include:

```
Haptic Belt PCB Design
Production design by rglenn
Based on On-Body Haptics by MissCrispenCakes
https://github.com/MissCrispenCakes/On-body-haptics
Licensed under CERN-OHL-P v2
```

## Source Location

As required by CERN-OHL-P v2:

**Source Location**: https://github.com/MissCrispenCakes/On-body-haptics/tree/main/hardware/pcb/haptic-belt
