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
  - name: SC Vollmer
    orcid: 0000-0002-3359-2810
    corresponding: true
    affiliation: 1
affiliations:
 - name: York University, Canada
   index: 1
   ror: 05fq50484
date: 25 January 2026
bibliography: paper.bib
---

# Summary

On-Body Haptics is an open-source project providing complete hardware and software for building wearable haptic feedback systems. The project enables researchers, artists, and developers to create tactile interfaces for spatial audio, virtual reality (VR), augmented reality (AR), and interactive installations. By responding to Open Sound Control (OSC) messages, the system integrates seamlessly with popular creative coding platforms including Max/MSP, TouchDesigner, Unity, and Pure Data.

The project provides two distinct implementations: an Arduino-based Bluetooth system optimized for portability with support for up to six independent wearable devices, and a Raspberry Pi-based I2C system offering high-fidelity haptic effects through professional-grade DRV2605L haptic drivers. Both implementations include complete PCB designs, 3D-printable enclosures, firmware, control software, and comprehensive documentation.

# Statement of Need

Haptic feedback provides essential tactile information for immersive experiences in VR/AR and spatial audio applications. However, existing haptic development platforms are often expensive, closed-source, or require specialized hardware that limits accessibility for researchers and independent developers. Commercial haptic devices typically cost hundreds to thousands of dollars and offer limited customization options.

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

# State of the Field

Several commercial and research platforms exist for haptic feedback development, but significant barriers remain for researchers and developers:

**Commercial Platforms**: Systems like Neosensory's Buzz wristband and TactSuit haptic vests offer sophisticated haptic capabilities but typically cost $500-$5000+ and use proprietary closed-source designs. These price points exclude independent researchers, artists, and students. Additionally, commercial systems often require specialized APIs and cannot be modified to support custom hardware configurations or experimental form factors.

**Research Prototypes**: Prior work on wearable haptic systems includes the Ilinx garment [@Giordano2015; @Lamontagne2015], which demonstrated whole-body tactile experiences for multisensory art installations, and Vibropixels [@Hattwick2017], a scalable wireless tactile display system. While these projects advanced the field significantly, publications in academic haptic research often lack manufacturing-ready designs, complete bills of materials, or production firmware that enable direct community replication and extension.

**Open Hardware Projects**: While some open-source haptic projects exist in maker communities, they typically focus on single implementations without providing multiple platform options to serve different research needs. Most lack integration with standard research protocols like Open Sound Control (OSC), limiting their utility in existing laboratory workflows with Max/MSP, TouchDesigner, and other creative coding environments.

On-Body Haptics addresses these limitations by providing: (1) complete production-ready PCB designs with Gerber files that can be manufactured without modification ($50-150 total cost), (2) two distinct implementations serving different research needs (portable Arduino + Bluetooth vs. high-fidelity Raspberry Pi + I2C) without requiring researchers to design custom hardware, (3) OSC protocol integration compatible with existing research workflows, and (4) documentation accessible to users without extensive electronics engineering backgrounds, including 15-minute quick-start guides and step-by-step assembly instructions.

# Software Design

The system architecture reflects three key design principles: hardware-software modularity, signal-agnostic control, and configuration-driven extensibility.

**Modular Hardware-Software Separation**: Both implementations (Arduino + Bluetooth, Raspberry Pi + I2C) share a common OSC-based control protocol but use fundamentally different hardware architectures. This separation enables researchers to choose hardware based on experimental requirements—portability for field studies versus haptic fidelity for controlled laboratory experiments—while maintaining consistent software interfaces. The OSC namespace (`/haptic/[device]/[command]`) abstracts hardware differences, allowing applications written for Max/MSP, TouchDesigner, or Unity to control both implementations without modification. This design emerged from the project's origin as an audio-reactive LED wearable system, where the same signal processing pipeline could drive either visual or haptic outputs by changing only the hardware layer.

**Threading and Queue Architecture**: The Raspberry Pi implementation uses Python's `threading` and `queue` modules to separate OSC message reception from I2C hardware communication. This architectural choice prevents blocking I2C operations from degrading OSC response times, ensuring sub-10ms latency for pattern triggers even when the DRV2605L haptic drivers are executing multi-second effect sequences. The Arduino implementation achieves similar responsiveness through interrupt-driven serial communication, with a lightweight command parser that executes within the main loop without blocking Bluetooth reads.

**Configuration-Driven Design**: Hardware-specific parameters (I2C addresses for the TCA9548A multiplexer channels, Bluetooth serial pins, effect library mappings for the DRV2605L) are externalized to JSON configuration files rather than hardcoded in source. This design enables researchers to modify hardware layouts—such as changing from a five-motor belt to an eight-motor vest, or remapping which DRV2605L effects correspond to OSC commands—without modifying core code. Custom form factors can be supported by editing a configuration file rather than forking the entire codebase.

**Architectural Trade-offs**: The Arduino implementation prioritizes portability, battery life, and cost over haptic fidelity, using simple on/off motor control with software-defined patterns (clockwise rotation, pulses, waves). The Raspberry Pi implementation inverts this trade-off, using DRV2605L haptic drivers that consume more power and require wired connections but provide access to 120+ distinct haptic effects (sharp clicks, soft ramps, buzz patterns, complex waveforms) designed for professional haptic applications. Both implementations are maintained in parallel rather than converging to a single design because research contexts demand both options: portable systems for artistic performances and field studies, high-fidelity systems for controlled perceptual experiments.

# Research Impact Statement

**External Adoption and Recognition**:
This platform has demonstrated research impact and community adoption through multiple channels:

- **Press Coverage**: Featured in Hackaday (2020) as an exemplar of accessible haptic development for VR applications [@Hackaday2020], reaching an audience of over 500,000 hardware developers and researchers
- **Research Funding**: Supported by Mitacs Accelerate Grant for "Washable Wearables for Affordable and Aesthetic Augmentation of Visuo-Tactile Sensory Perception Enhancement in Mixed Reality" [@Mitacs2021], demonstrating peer-reviewed research significance
- **Institutional Partnerships**: KDF Entertainment (established 2009, author's organization for tech/art work) became an official York University procurement vendor, enabling research lab collaborations and equipment supply for academic projects
- **Sustained Public Development**: Six years of continuous public development (October 2019-present) with transparent version control, demonstrating long-term commitment beyond proof-of-concept prototypes
- **Community Engagement**: Active GitHub repository with comprehensive issue tracking, pull request workflows, and community contribution guidelines

**Research Enablement**:
The system supports research and creative work across multiple domains:

- **Spatial Audio Visualization**: Directional haptic cues to complement spatial audio systems for immersive audio experiences
- **Accessibility Applications**: Tactile wayfinding and navigation interfaces for visually impaired users
- **VR/AR Haptic Feedback**: Wearable haptic interfaces for virtual and augmented reality applications
- **Human-Computer Interaction**: Studies of tactile perception, multi-modal interaction, and haptic pattern recognition
- **Artistic Performance**: Wearable haptic interfaces for live performance and interactive installation art

**Significance and Impact**: By providing complete, production-ready designs at $50-150 total cost compared to $500-5000+ for commercial systems, this platform enables haptic research for under-resourced institutions, independent researchers, artists, and students who would otherwise be excluded from this field. The open-source hardware designs (CERN-OHL-P v2) and software (MIT License) ensure that derivative works can be created, shared, and built upon by the research community, addressing the reproducibility gap common in academic haptic systems research.

# AI Usage Disclosure

AI tools assisted with manuscript editing and formatting to JOSS specifications. All technical work is original.

# Acknowledgments

The author thanks Prof. Doug Van Nort (York University, Dispersion Lab) for initial class project support [@Vollmer2019] and subsequent contract work, and Prof. Graham Wakefield (York University, Alice Lab) for PhD supervision and collaborative support on the Mitacs Accelerate grant application.

This research was supported by a Mitacs Accelerate Grant (Lab2Market program). Research collaboration enabled through KDF Entertainment's partnership with York University.

Special thanks to rglenn for assistance with early version production-ready PCB designs, generating manufacturing-ready Gerber files, and 3D printing, and providing expert assembly and soldering work for prototype validation. This project builds upon the Adafruit open-source libraries and broader hardware community.

# References
