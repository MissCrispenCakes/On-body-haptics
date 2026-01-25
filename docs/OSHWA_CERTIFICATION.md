# OSHWA Certification Guide

Guide for getting your On-Body Haptics project officially certified by the Open Source Hardware Association (OSHWA).

## ✅ Compliance Status

**Your project ALREADY MEETS all OSHWA requirements!**

### Requirements Checklist

- ✅ **Open Source Hardware License**: CERN-OHL-P v2 (OSHWA-approved)
- ✅ **Open Source Software License**: MIT (OSHWA-approved)
- ✅ **Design Files Provided**: KiCad source files, OpenSCAD files
- ✅ **Manufacturing Files**: Gerber files for PCB production
- ✅ **Documentation Links**: Clear links to design files in README and hardware/README.md
- ✅ **Source Location**: Repository URL specified in LICENSE-HARDWARE
- ✅ **Component Datasheets**: Third-party component datasheets included
- ✅ **Clear Licensing**: Dual licensing clearly explained
- ✅ **Version Control**: Git repository with full history

## What is OSHWA Certification?

The Open Source Hardware Association provides a **free self-certification program** that:

- Gives your project an official **Open Source Hardware (OSHW) certification mark**
- Provides a **unique identifier (UID)** for your project (e.g., US000123)
- Lists your project in the **official OSHWA directory**
- Lets you **legally use the OSHW logo** on hardware and documentation
- Increases visibility and credibility in the open hardware community

## About CERN-OHL-P v2

Your hardware license (CERN-OHL-P v2) is **one of the seven OSHWA-recommended licenses**:

**OSHWA-Approved Licenses:**
- ✅ **CERN-OHL** (Permissive, Weakly Reciprocal, Strongly Reciprocal) - **← You use this!**
- ✅ TAPR Open Hardware License
- ✅ GNU General Public License (GPL)
- ✅ Creative Commons Attribution-ShareAlike (CC BY-SA)
- ✅ FreeBSD License
- ✅ MIT License
- ✅ Creative Commons Attribution (CC BY)

**Why CERN-OHL-P is excellent:**
- Only hardware-specific license approved by Open Source Initiative (OSI)
- Designed for hardware, software, and documentation together
- Version 2 is modern (2020) and well-maintained
- "P" (Permissive) variant allows maximum freedom for users

**No license change needed!** You're already using an optimal license.

## How to Get Certified

### Step 1: Prepare Your Information

You'll need:

1. **Project Name**: On-Body Haptics
2. **Your Name/Organization**: MissCrispenCakes (or your real name if you prefer)
3. **Project URL**: https://github.com/MissCrispenCakes/On-body-haptics
4. **Hardware License**: CERN-OHL-P-2.0
5. **Software License**: MIT
6. **Documentation License**: MIT (same as software)
7. **Country**: USA (or your country)
8. **Project Description**: "Open-source wearable haptic feedback systems for spatial audio, VR/AR, and interactive installations."

9. **Links to Design Files**:
   - Hardware designs: https://github.com/MissCrispenCakes/On-body-haptics/tree/main/hardware
   - PCB KiCad files: https://github.com/MissCrispenCakes/On-body-haptics/tree/main/hardware/pcb
   - Gerber files: Available in each PCB subdirectory
   - 3D enclosures: https://github.com/MissCrispenCakes/On-body-haptics/tree/main/hardware/enclosures
   - Bill of Materials: https://github.com/MissCrispenCakes/On-body-haptics/blob/main/hardware/bom.xlsx

10. **Project Type**: Select "wearable technology" or "haptic device"

### Step 2: Self-Certify Online

1. Go to **https://certification.oshwa.org/**

2. Click **"Certify a Project"** or **"Apply for Certification"**

3. Fill out the **Certification Mark License Agreement**:
   - Read and agree to the terms
   - Confirm all parts under your control are open source
   - Confirm third-party components have accessible datasheets
   - Agree to yearly renewal emails

4. Submit the form

5. **You'll receive a unique OSHW UID immediately!**
   - Format: `US000XXX` (if in USA) or `XX000XXX` (for other countries)
   - Example: `US000789`

6. Your project will be listed in the **OSHWA Directory**: https://certification.oshwa.org/list.html

### Step 3: Add the OSHW Certification Mark

Once certified, you **CAN and SHOULD** use the official OSHW logo!

#### Where to Use the Logo

You can use the OSHW certification mark on:

1. **Hardware itself** - Silkscreen on PCB, printed on enclosure
2. **README.md** - Badge at the top
3. **Hardware documentation** - Hardware README, assembly guide
4. **Product website** - If you have one
5. **Product packaging** - If you sell kits

#### Logo Design Files

Download official logo files from: **https://github.com/oshwa/certification-mark**

Available formats:
- **SVG** - Vector (best for scaling)
- **PNG** - Raster (web use)
- **EPS** - Print production

#### Logo Usage Rules

**Colors:**
- **Preferred**: Graphite + Coral (brand colors)
- **Alternative**: Black, white, or gray when color isn't possible

**UID Display:**
- The logo is required
- Your unique ID (e.g., `US000123`) is optional but **highly recommended**

**Plaintext:**
- Where graphics aren't possible, use: `[OSHW] US000123`
- Similar to how © can be written as (c)

#### Logo Placement Examples

**On PCB Silkscreen:**
```
┌─────────────────────┐
│                     │
│  On-Body Haptics    │
│  [OSHW] US000XXX    │
│                     │
└─────────────────────┘
```

**In README.md:**
```markdown
[![OSHW Certification](https://github.com/oshwa/certification-mark/raw/master/open-source-hardware-logo.svg)](https://certification.oshwa.org/us000xxx.html)
```

**On 3D Printed Enclosure:**
- Emboss or print the OSHW logo on the case
- Include UID on label or embossed text

### Step 4: Update Project Documentation

After certification, update these files:

1. **README.md** - Add OSHW badge near the top (see Step 3)

2. **hardware/README.md** - Add certification notice:
   ```markdown
   ## OSHWA Certification

   This project is certified as Open Source Hardware by OSHWA.

   Certification UID: **US000XXX**

   [![OSHW](https://github.com/oshwa/certification-mark/raw/master/open-source-hardware-logo.svg)](https://certification.oshwa.org/us000xxx.html)
   ```

3. **CITATION.cff** - Add OSHWA identifier:
   ```yaml
   identifiers:
     - type: other
       value: "OSHW-US000XXX"
       description: "OSHWA Open Source Hardware Certification"
   ```

4. **PCB designs** - Add OSHW logo to silkscreen (for next PCB revision)

5. **3D enclosure** - Update OpenSCAD/STL to include logo emboss

### Step 5: Maintain Certification

**Annual Renewal:**
- OSHWA will send yearly renewal emails
- Confirm your project still meets requirements
- Update documentation links if your repo moved
- **It's free** - no fees for renewal

**Version Updates:**
- When you release new hardware versions, you can:
  - Update the existing certification (for minor changes)
  - Register a new certification UID (for major new designs)

## Benefits of Certification

Once certified, you get:

1. **Credibility** - Official recognition from OSHWA
2. **Discoverability** - Listed in OSHWA directory
3. **Logo Usage** - Legal permission to use OSHW mark
4. **Community** - Join the global open hardware movement
5. **Academic Recognition** - Some institutions recognize OSHW certification
6. **Grant Eligibility** - Some open hardware grants require OSHWA certification

## Timeline

- **Certification application**: 10-15 minutes
- **Approval**: Immediate (it's self-certification!)
- **Logo download and integration**: 30-60 minutes
- **Total time**: Less than 2 hours to be fully certified!

## Frequently Asked Questions

### Do I need to pay for certification?
**No!** OSHWA certification is completely free, including renewal.

### What if I use third-party components (ICs, modules)?
That's fine! As long as:
- The parts YOU designed are open source (✅ you do this)
- Third-party components have accessible datasheets (✅ you provide these)

### Can I use the logo before certification?
**No.** You must complete certification before using the OSHW certification mark. However, you can say "open source hardware" without the mark.

### What if I make changes to my hardware?
- **Minor changes** (bug fixes, component substitutions): Update existing certification
- **Major redesign**: Consider getting a new UID for the new version
- You can have multiple certified versions

### Do I need to certify software separately?
No. OSHWA certification covers the complete project (hardware + software + docs). Your MIT license for software is already OSHWA-approved.

### Can I use multiple licenses?
Yes! Your dual licensing (MIT + CERN-OHL-P) is perfect and fully compliant.

## Resources

- **OSHWA Certification**: https://certification.oshwa.org/
- **OSHWA Definition**: https://oshwa.org/definition/
- **Certification Requirements**: https://certification.oshwa.org/requirements.html
- **Logo Files**: https://github.com/oshwa/certification-mark
- **Certified Projects Directory**: https://certification.oshwa.org/list.html
- **OSHWA FAQ**: https://oshwa.org/resources/open-source-hardware-faq/

## Next Steps

**You're ready to certify right now!**

1. Go to https://certification.oshwa.org/
2. Fill out the 10-minute self-certification form
3. Get your unique OSHW UID
4. Download and add the logo to your project
5. Update README.md and hardware documentation
6. Announce your certification! 🎉

---

**Questions?**
- OSHWA Contact: certification@oshwa.org
- GitHub Discussions: https://github.com/MissCrispenCakes/On-body-haptics/discussions
