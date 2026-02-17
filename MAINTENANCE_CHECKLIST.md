# Maintenance Checklist

> **Quick reference for keeping documentation and metadata synchronized**

This document lists all files that should be reviewed and updated together when making certain types of changes.

---

## 📦 When Releasing a New Version

**Update version numbers in:**
- [ ] `CITATION.cff` (line 54: `version:`)
- [ ] `CHANGELOG.md` (add new version section)
- [ ] `README.md` (if version is mentioned in text)
- [ ] `paper.md` (if submitting updated JOSS paper)
- [ ] `.zenodo.json` (title includes version)
- [ ] Create git tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
- [ ] Create GitHub Release
- [ ] Update Zenodo record (automatic if GitHub-Zenodo integration is on)

**Update dates in:**
- [ ] `CITATION.cff` (line 55: `date-released:`)
- [ ] `CHANGELOG.md` (date for new version)
- [ ] `SECURITY.md` (line 223: "Last Updated")

---

## 👤 When Changing Author/Contributor Information

**Update all of these:**
- [ ] `AUTHORS.md` - Primary documentation of all contributors
- [ ] `CITATION.cff` - Machine-readable citation metadata
- [ ] `.zenodo.json` - Zenodo archive metadata
- [ ] `README.md` - Citation section at bottom
- [ ] `paper.md` - JOSS paper (if applicable)
- [ ] `paper.bib` - JOSS references (if applicable)

**Verify identity mapping is consistent:**
- GitHub handle: `MissCrispenCakes`
- Academic name: `S.C. Vollmer`
- ORCID: `0000-0002-3359-2810`
- Affiliation: `York University, Canada`

---

## 🏆 When Adding Publications or Press

**Update these files:**
- [ ] `AUTHORS.md` - "Publications & Dissemination" section (if you add one)
- [ ] `README.md` - "Press & Features" section
- [ ] `paper.md` - Citations and references (if JOSS paper)
- [ ] `paper.bib` - Add BibTeX entries
- [ ] `docs/research/context.md` - Research context section
- [ ] `index.html` - Timeline or featured section

---

## 🔐 When Updating Licenses

**Update all of these:**
- [ ] `LICENSE` - MIT License (software)
- [ ] `LICENSE-HARDWARE` - CERN-OHL-P (hardware)
- [ ] `README.md` - License badges and section
- [ ] `CITATION.cff` - License field
- [ ] `.zenodo.json` - License field (currently only lists MIT)
- [ ] `index.html` - Footer license links

---

## 🏛️ When Institutional Affiliations Change

**Update all of these:**
- [ ] `AUTHORS.md` - Institutional Affiliations section
- [ ] `CITATION.cff` - Author affiliation
- [ ] `.zenodo.json` - Creator affiliation
- [ ] `paper.md` - Author affiliation header
- [ ] `README.md` - Acknowledgments section (if mentioned)
- [ ] `docs/research/context.md` - Academic partnerships

---

## 💰 When Funding Changes

**Update all of these:**
- [ ] `AUTHORS.md` - Funding Acknowledgments section
- [ ] `paper.md` - Acknowledgments section
- [ ] `docs/research/context.md` - Research funding section
- [ ] `README.md` - Acknowledgments (if mentioned)
- [ ] `.zenodo.json` - Grants field (currently empty)

---

## 🔗 When DOIs Are Added/Changed

**Update all badge/citation locations:**
- [ ] `README.md` - DOI badge at top
- [ ] `AUTHORS.md` - DOI badge at top
- [ ] `CITATION.cff` - Identifiers section
- [ ] `.zenodo.json` - Related identifiers
- [ ] `paper.md` - References (if self-citing)
- [ ] `paper.bib` - Add DOI entries

---

## 🌐 When Website (index.html) Changes

**Review consistency with:**
- [ ] `README.md` - Feature descriptions should match
- [ ] `AUTHORS.md` - Credits should match
- [ ] Timeline events should match actual project history
- [ ] External links should have `rel="noopener"`
- [ ] Press/features should match "Press & Features" in README

---

## 🔒 When Security Info Changes

**Update:**
- [ ] `SECURITY.md` - Main security documentation
- [ ] Update "Last Updated" date at bottom
- [ ] Update version number if significant changes
- [ ] `README.md` - Link to SECURITY.md (if adding)

**Contact methods:**
- `SECURITY.md`: GitHub Security Advisories (preferred) or obfuscated email
- Email is NOT in CITATION.cff to prevent scraping

---

## 🧪 When Hardware/Software Changes

**For hardware changes:**
- [ ] `hardware/` directory - Update designs
- [ ] `docs/hardware/bom.md` - Update Bill of Materials
- [ ] `docs/hardware/assembly-guide.md` - Update instructions
- [ ] `CITATION.cff` - Update hardware license info if needed
- [ ] `README.md` - Update hardware specifications
- [ ] Consider OSHWA certification update

**For software/firmware changes:**
- [ ] `implementations/` directories - Update code
- [ ] `docs/api/` - Update API documentation
- [ ] `docs/getting-started/` - Update quick-start guides
- [ ] `README.md` - Update feature descriptions
- [ ] `CHANGELOG.md` - Document changes

---

## 📋 Quarterly Maintenance Tasks

**Every 3 months, review:**
- [ ] Dependencies (npm audit, pip list --outdated)
- [ ] External links (check for 404s)
- [ ] GitHub Issues and Discussions
- [ ] Security advisories
- [ ] Documentation accuracy
- [ ] README badges (check if services are down)

---

## 🎯 Before Major Milestones

**Before JOSS submission:**
- [ ] Verify paper.md word count (750-1750)
- [ ] Check all citations in paper.bib are legitimate
- [ ] Update paper.md with latest acknowledgments
- [ ] Verify CITATION.cff matches paper.md
- [ ] Run GitHub Actions to build PDF

**Before conference presentations:**
- [ ] Update README with upcoming talks
- [ ] Verify all documentation is current
- [ ] Check that quick-start guides work
- [ ] Update AUTHORS.md with latest affiliations

**Before creating GitHub Release:**
- [ ] Update CHANGELOG.md
- [ ] Update version in all files (see "When Releasing" above)
- [ ] Build and test both implementations
- [ ] Review SECURITY.md is current
- [ ] Create release notes

---

## 🔧 Files That Should Always Match

| Concept | Files That Must Match |
|---------|----------------------|
| **Project version** | CITATION.cff, CHANGELOG.md, git tags |
| **Author name** | CITATION.cff, AUTHORS.md, .zenodo.json, paper.md |
| **Author email** | CITATION.cff, SECURITY.md |
| **Author ORCID** | CITATION.cff, .zenodo.json, paper.md |
| **Affiliation** | CITATION.cff, .zenodo.json, paper.md, AUTHORS.md |
| **Zenodo DOI** | README.md, AUTHORS.md, CITATION.cff |
| **Licenses** | LICENSE files, README badges, CITATION.cff, .zenodo.json |
| **Contributors** | AUTHORS.md, CITATION.cff (contributors), .zenodo.json (contributors) |

---

## 📝 Notes

- **Identity mapping**: Always maintain "MissCrispenCakes is the open-source handle of S.C. Vollmer" in README.md
- **Contributor timeline**: rglenn = hardware contributor (2019-2020 only)
- **Publication lineage**: 2019 Tactical Tactile Textiles report → 2026 formalization (no EVA references)
- **When in doubt**: Check AUTHORS.md first (it's the single source of truth for credits)

---

**Last Updated**: 2026-02-17
**Maintained by**: S.C. Vollmer (MissCrispenCakes)
