# Changelog

All notable changes to the On-Body Haptics project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-25

### Major Refactor - Repository Revitalization

This release represents a complete restructuring of the repository to make it professional, secure, and user-friendly.

### Added

#### Documentation
- **Comprehensive README.md** - Complete rewrite with professional presentation, feature highlights, and sponsorship information
- **Quick Start Guides** - 15-minute setup guides for both Arduino and Raspberry Pi implementations
- **Platform Selection Guide** - Detailed comparison to help users choose between implementations
- **OSC Protocol Specification** - Complete API reference with examples for multiple platforms
- **SECURITY.md** - Comprehensive security policy covering OSC, Bluetooth, WiFi, and configuration security
- **CONTRIBUTING.md** - Contribution guidelines with code style, PR process, and community standards
- **Implementation READMEs** - Detailed setup instructions for each platform

#### Project Structure
- **Unified directory structure** - All implementations, hardware, and documentation in organized hierarchy
- **implementations/** directory - Separate subdirectories for Arduino and Raspberry Pi platforms
- **hardware/** directory - PCB designs, enclosures, BOM, and datasheets
- **docs/** directory - Getting started guides, API reference, and integration examples
- **tools/** directory - Development and testing utilities
- **tests/** directory - Automated test infrastructure

#### Dependency Management
- **package.json** - Node.js dependencies for Arduino OSC server (osc-min, ws)
- **requirements.txt** - Python dependencies for both implementations
- **setup.py** - Installable Python package for Raspberry Pi implementation

#### Configuration Management
- **Configuration templates** - JSON and Python configuration files with examples
- **Arduino config.h** - Hardware pin configuration extracted from main code
- **Arduino patterns.h** - Pattern definitions modularized
- **Raspberry Pi config.py** - Centralized configuration with local override support
- **No hardcoded credentials** - All IPs, MACs, ports extracted to config files

#### Security
- **.gitignore** - Comprehensive ignore rules for credentials, dependencies, and OS files
- **.gitattributes** - Git LFS configuration for binary files (PCBs, images, documents)
- **Security best practices** - Documentation for network isolation, credential management, and access control

#### Hardware
- **Complete PCB designs** - KiCad projects for both haptic-belt and haptic-uhat
- **Gerber files** - Manufacturing-ready files for both PCB designs
- **3D enclosures** - STL and OpenSCAD files for Raspberry Pi case
- **Bill of Materials** - Complete BOM with part numbers and sources

### Changed

#### Repository Structure
- **Migrated Arduino_Node branch** to `implementations/arduino-bluetooth/`
- **Migrated I2C_python branch** to `implementations/raspberry-pi-i2c/`
- **Reorganized hardware files** from multiple branches into unified `hardware/` directory
- **Consolidated documentation** from docs branch into `docs/` directory

#### Code Organization
- **Extracted configuration** from code to separate config files
- **Modularized Arduino firmware** with config.h and patterns.h
- **Organized Raspberry Pi code** with src/, utils/, and systemd/ subdirectories
- **Renamed files** to follow consistent naming conventions (kebab-case)

#### Documentation
- **README.md** - Completely rewritten from basic branch listing to professional project showcase
- **OSC protocol** - Formalized specification from informal notes
- **Setup instructions** - Expanded from TODO notes to step-by-step guides

### Fixed

#### Security Issues
- **Removed hardcoded credentials** - No more Bluetooth MACs, IPs, or passwords in code
- **Added .gitignore** - Prevents accidental commits of sensitive configuration files
- **Documented default credentials** - Warns users to change default passwords immediately

#### Code Quality
- **Removed commented-out code** - Cleaned up legacy commented sections
- **Extracted magic numbers** - Moved to named constants in config files
- **Fixed inconsistent naming** - Standardized file and variable naming
- **Improved error handling** - Added validation and error messages

#### Documentation
- **Removed TO UPDATE notes** - Replaced placeholder text with actual documentation
- **Fixed broken references** - Updated all cross-references and links
- **Clarified setup steps** - Expanded brief notes into detailed instructions

### Preserved

#### All Features from Previous Branches
- **Arduino_Node features** - Bluetooth communication, OSC regex, 6-belt support, pre-programmed patterns
- **I2C_python features** - I2C multiplexing, DRV2605L effects, OLED display, systemd services
- **Hardware designs** - All PCB projects, Gerber files, 3D models, and BOM preserved
- **Research context** - Original documentation and references maintained

#### Backward Compatibility
- **OSC protocol unchanged** - Existing control applications continue to work
- **Hardware designs unchanged** - PCBs and enclosures remain compatible
- **Branch preservation** - Old branches available for reference (will be tagged)

### Migration Notes

#### From Arduino_Node Branch
- Firmware: `AudioHaptics.ino` → `implementations/arduino-bluetooth/firmware/AudioHaptics/`
- Server: `Audio_Haptics.js`, `server_haptics.js`, etc. → `implementations/arduino-bluetooth/server/src/`
- Bluetooth bridge: `HC05.py` → `implementations/arduino-bluetooth/server/src/bluetooth-bridge.py`

#### From I2C_python Branch
- Python code: `haptics_v2_I2C/code/*.py` → `implementations/raspberry-pi-i2c/firmware/src/` and `utils/`
- Systemd: `*.service` → `implementations/raspberry-pi-i2c/firmware/systemd/`
- PCBs: `haptic-belt/`, `haptic-uhat/` → `hardware/pcb/`
- Enclosure: `pi-enclosure/` → `hardware/enclosures/raspberry-pi-case/`
- BOM: `haptic boards BOM.xlsx` → `hardware/bom.xlsx`

#### Branch Strategy
- **New main branch** - All future development on unified `main` branch
- **Old branches preserved** - Tagged as `archive/arduino-node`, `archive/i2c-python`, etc.
- **No deletion** - Historical branches remain available for reference

### Dependencies

#### Arduino Implementation (Node.js)
- osc-min ^1.1.2
- ws ^8.14.0

#### Arduino Implementation (Python Bluetooth)
- pyserial >=3.5
- pybluez >=0.23 (Linux)

#### Raspberry Pi Implementation
- adafruit-circuitpython-ssd1306 >=2.12.0
- adafruit-circuitpython-drv2605 >=1.2.0
- adafruit-circuitpython-tca9548a >=0.6.0
- adafruit-blinka >=8.20.0
- python-osc >=1.8.3
- netifaces >=0.11.0
- RPi.GPIO >=0.7.1
- pillow >=10.0.0

### Breaking Changes

⚠️ **Configuration Required**
- Users must create local configuration files (not tracked by git)
- Bluetooth MAC addresses must be configured before use
- Default credentials must be changed for security

⚠️ **Directory Structure Changed**
- File paths have changed from old branch structure
- Update any scripts or references to old paths

⚠️ **Installation Required**
- Both implementations now require dependency installation
- Run `npm install` (Arduino) or `pip install -r requirements.txt` (Raspberry Pi)

### Upgrade Guide

#### For Existing Arduino Users
1. Clone the new repository structure
2. Copy your Bluetooth MAC addresses from old `Audio_Haptics.js`
3. Create `implementations/arduino-bluetooth/server/config/local.json`
4. Add your MAC addresses to the config
5. Run `npm install` in server directory
6. Test with `npm start`

#### For Existing Raspberry Pi Users
1. Clone the new repository structure
2. Review `implementations/raspberry-pi-i2c/firmware/src/config.py`
3. Create `config_local.py` with any custom settings
4. Run `pip3 install -r requirements.txt`
5. Test with `python3 src/octopulse_server.py`
6. Update systemd service paths if using auto-start

### Known Issues

- Git LFS required for binary files (PDFs, images, Gerber ZIPs)
- macOS Bluetooth serial ports require additional configuration
- Some HC-05 modules require 3.3V logic level conversion

### Coming Soon

- Hardware assembly guide with photos
- Integration examples for Max/MSP, TouchDesigner, Unity
- GitHub Actions CI/CD for automated testing
- Test infrastructure for both implementations
- Additional pattern examples
- Video demonstrations

## [1.x.x] - Historical

Previous versions existed across multiple branches:
- **Arduino_Node** - Arduino + Bluetooth implementation
- **I2C_python** - Raspberry Pi + I2C implementation
- **docs** - Documentation and research context
- **startup** - Initial project information

These branches are preserved as git tags for reference.

---

## Version History Legend

- **[Unreleased]** - Upcoming changes in development
- **[X.Y.Z]** - Released versions
- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

[2.0.0]: https://github.com/yourusername/On-body-haptics/releases/tag/v2.0.0
