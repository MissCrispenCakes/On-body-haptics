---
title: 'On-Body Haptics: Open-Source Wearable Haptic Feedback Systems for Spatial Audio and VR/AR'
tags:
  - Python
  - JavaScript
  - Arduino
  - haptics
  - wearable computing
  - tactile feedback
  - virtual reality
  - augmented reality
  - human-computer interaction
  - open hardware
  - OSC protocol
authors:
  - name: MissCrispenCakes
    orcid: 0000-0000-0000-0000
    corresponding: true
    affiliation: 1
affiliations:
 - name: Independent Researcher, USA
   index: 1
date: 25 January 2024
bibliography: paper.bib
---

# Summary

On-Body Haptics is an open-source project providing complete hardware and software for building wearable haptic feedback systems. The project enables researchers, artists, and developers to create tactile interfaces for spatial audio, virtual reality (VR), augmented reality (AR), and interactive installations. By responding to Open Sound Control (OSC) messages, the system integrates seamlessly with popular creative coding platforms including Max/MSP, TouchDesigner, Unity, and Pure Data.

The project provides two distinct implementations: an Arduino-based Bluetooth system optimized for portability with support for up to six independent wearable devices, and a Raspberry Pi-based I2C system offering high-fidelity haptic effects through professional-grade DRV2605L haptic drivers. Both implementations include complete PCB designs, 3D-printable enclosures, firmware, control software, and comprehensive documentation.

# Statement of Need

Haptic feedback is increasingly recognized as essential for immersive experiences in VR/AR and spatial audio applications [@Choi2015; @Kreimeier2019]. However, existing haptic development platforms are often expensive, closed-source, or require specialized hardware that limits accessibility for researchers and independent developers [@Culbertson2018]. Commercial haptic devices typically cost hundreds to thousands of dollars and offer limited customization options [@Schneider2017].

On-Body Haptics addresses these barriers by providing:

1. **Affordability**: Complete systems can be built for $50-150 using readily available components
2. **Openness**: Full hardware designs (CERN-OHL-P v2) and software (MIT License) are provided
3. **Accessibility**: Step-by-step documentation enables users without extensive electronics experience to build functional systems
4. **Flexibility**: Two implementations serve different use cases from portable performance to laboratory research
5. **Integration**: OSC protocol support enables seamless integration with existing creative coding workflows

The project has been designed for use in human-computer interaction research, accessibility applications, artistic performances, and educational contexts. By lowering the barrier to entry for haptic development, On-Body Haptics enables broader exploration of tactile interfaces in spatial computing.

# Key Features

## Hardware Implementations

### Arduino + Bluetooth Implementation
The Arduino implementation provides a portable, battery-powered solution using readily available microcontrollers (Arduino Uno/Nano) and HC-05/HC-06 Bluetooth modules. Each device supports five haptic actuators arranged spatially around the body, with support for up to six independent devices communicating simultaneously. The system includes pre-programmed patterns (clockwise/counter-clockwise rotation, pulse, wave) and supports custom pattern definitions. A Node.js OSC bridge provides network connectivity and WebSocket support for browser-based applications.

### Raspberry Pi + I2C Implementation
The Raspberry Pi implementation leverages the TCA9548A I2C multiplexer and Adafruit DRV2605L haptic drivers to provide eight independent channels with access to 120+ distinct haptic effects [@AdafruitDRV2605]. The system includes an SSD1306 OLED display for network configuration and supports systemd auto-start for production deployments. The DRV2605L's extensive effect library enables nuanced tactile feedback including clicks, ramps, buzzes, and complex waveforms.

## Software Architecture

Both implementations utilize the Open Sound Control (OSC) protocol [@Wright2003], a widely-adopted standard in creative technology and research applications. The OSC implementation supports:

- Regex-based pattern matching for multi-device addressing
- WebSocket bridging for web-based control interfaces
- Queue-based command processing with threading for responsive performance
- Configurable intensity and timing parameters

The modular architecture allows researchers to extend functionality without modifying core code, with configuration files separating hardware-specific parameters from application logic.

## Documentation and Reproducibility

The project includes:

- 15-minute quick-start guides for both implementations
- Complete PCB designs with Gerber files ready for manufacturing
- Bill of Materials with specific part numbers and supplier information
- 3D-printable enclosures with both source (OpenSCAD) and ready-to-print (STL) files
- Comprehensive API documentation for the OSC protocol
- Integration examples for popular platforms (Max/MSP, TouchDesigner, Unity, Pure Data)

All hardware designs use CERN Open Hardware License (CERN-OHL-P v2), ensuring users can manufacture, modify, and distribute derivative works [@CERN2020].

# Research Applications

On-Body Haptics has been designed to support research in:

- **Spatial Audio**: Directional haptic cues to complement spatial audio systems
- **Navigation**: Tactile wayfinding for accessibility applications
- **Virtual/Augmented Reality**: Haptic feedback for immersive experiences
- **Human-Computer Interaction**: Studies of tactile perception and multi-modal interaction
- **Artistic Performance**: Wearable haptic interfaces for live performance and installation art

The system's modularity and open design facilitate controlled experiments while enabling creative applications beyond the original intended use cases.

# Comparison with Existing Systems

Compared to commercial haptic development platforms:

| Feature | On-Body Haptics | Commercial Systems |
|---------|----------------|-------------------|
| Cost | $50-150 | $500-5000+ |
| Hardware Source | Open (CERN-OHL-P) | Closed/Proprietary |
| Software Source | Open (MIT) | Often Proprietary |
| Customization | Full access to designs | Limited |
| Integration | OSC (widely supported) | Varies |

Compared to research prototypes described in the literature, On-Body Haptics provides complete documentation and manufacturability, addressing the common challenge of replicating research hardware [@Schneider2017].

# Future Development

Planned enhancements include:

- Expanded effect library for the Arduino implementation
- Wireless communication options for the Raspberry Pi implementation
- Additional hardware designs (vests, gloves, headbands)
- Integration examples for additional platforms
- Automated testing infrastructure for OSC protocol validation

Community contributions are welcomed through the project's GitHub repository.

# Acknowledgments

This project builds upon the Adafruit DRV2605L CircuitPython library and the broader open-source hardware and software communities. Thanks to early testers and users who provided valuable feedback during development.

# References
