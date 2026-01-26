# Research Context

Academic and research context for On-Body Haptics project.

## Overview

This project builds upon decades of research in haptic feedback, tactile perception, and human-computer interaction. This page provides context and references for researchers using this platform.

## Design Philosophy: Audio-Reactive Haptics

The On-Body Haptics project originated as an **audio-reactive wearable LED system**. The first Arduino prototype responded to audio input - claps, music, and environmental sounds would trigger spatial light patterns worn around the body. This sound-to-light mapping proved so compelling that it inspired the next evolution: translating the same patterns into tactile feedback.

### From Light to Touch

The transition from LEDs to haptic motors revealed something interesting: **the control architecture didn't need to change**. The same OSC protocol that drove light patterns could drive haptic patterns. The same audio analysis that triggered LEDs could trigger vibrations. The system was inherently **signal-agnostic** - it doesn't care whether the input comes from:

- Audio analysis (FFT, beat detection, amplitude)
- MIDI controllers and musical instruments
- Game engines and VR systems
- Sensor networks (proximity, motion, biometric)
- Creative coding platforms (Max/MSP, TouchDesigner, Processing)
- Custom applications via OSC

This flexibility emerged from the original audio-reactive design and became a core principle: **any signal can become a haptic experience**.

### Hardware Modularity

The same principle applies to outputs: swap haptic motors for LEDs and you have a wearable light display. Swap for speakers and you have a spatial audio system. The modular design means the platform supports experimentation across sensory modalities.

### Research Context & Funding

**Press Coverage:**
- [Hackaday (2020)](https://hackaday.com/2020/02/12/in-pursuit-of-haptics-for-a-better-vr-experience/) - "In Pursuit of Haptics for a Better VR Experience"

**Research Funding:**
- [Mitacs Grant](https://www.mitacs.ca/our-projects/washable-wearables-for-affordable-and-aesthetic-augmentation-of-visuo-tactile-sensory-perception-enhancement-in-mixed-reality/) - "Washable Wearables for Affordable and Aesthetic Augmentation of Visuo-Tactile Sensory Perception Enhancement in Mixed Reality"

**Academic Partnerships:**
- [York University](https://www.yorku.ca/procurement/oba/kdf-entertainment/) - KDF Entertainment is an official procurement vendor, enabling direct collaboration with York University research groups

## Key Research Areas

### Haptic Feedback in VR/AR

Coming soon: Literature review of haptic feedback in immersive experiences.

### Tactile Spatial Perception

Coming soon: Research on how humans perceive directional tactile cues.

### Wearable Haptic Systems

Coming soon: Survey of existing wearable haptic research platforms.

## Related Work

For academic context, see references in:
- [JOSS Paper](../../paper.md)
- [Bibliography](../../paper.bib)

## Applications

### Research Applications

Coming soon: Examples of research studies using this platform.

### Use Cases

- Spatial audio visualization
- Navigation assistance for accessibility
- VR/AR haptic feedback
- Interactive art installations
- Multi-modal notifications

## Contributing Research

Using this platform in your research? We'd love to hear about it!

- Add your publication to our [showcase](#) (coming soon)
- Cite this project using [CITATION.cff](../../CITATION.cff)
- Share your findings in [Discussions](https://github.com/MissCrispenCakes/On-body-haptics/discussions)

## Contact

For research collaborations or questions, open a [Discussion](https://github.com/MissCrispenCakes/On-body-haptics/discussions).
