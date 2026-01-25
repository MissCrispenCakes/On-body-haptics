# JOSS Submission Guide

Guide for submitting On-Body Haptics to the Journal of Open Source Software (JOSS).

## What is JOSS?

[JOSS](https://joss.theoj.org/) is a developer-friendly, open-access journal for research software packages. It provides:
- Peer review of software quality and documentation
- Archival publication with DOI
- Academic credit for open-source software development
- Increased visibility in the research community

## Prerequisites

Before submitting, ensure:

- ✅ Open source license (MIT + CERN-OHL-P - we have this!)
- ✅ Hosted on public repository (GitHub - we have this!)
- ✅ Documentation (README, API docs - we have this!)
- ✅ Tests (pytest framework - we have this!)
- ✅ `paper.md` describing the software (created!)
- ✅ `paper.bib` with references (created!)

## Checklist Before Submission

### Required Files

- [x] `paper.md` - JOSS paper describing the software
- [x] `paper.bib` - BibTeX references
- [x] `LICENSE` and `LICENSE-HARDWARE` - Open source licenses
- [x] `README.md` - Clear documentation
- [x] `CONTRIBUTING.md` - Contribution guidelines

### Paper Requirements

Your `paper.md` should include:

- [x] **Summary** - Brief overview (we have this)
- [x] **Statement of need** - Why this software is needed (we have this)
- [x] **Key features** - Technical description (we have this)
- [x] **Comparison** - How it compares to alternatives (we have this)
- [x] **References** - Cited literature (we have this)

### To Update in `paper.md`

1. **Add your ORCID** (line 12):
   - Get one at https://orcid.org/register
   - Replace `0000-0000-0000-0000` with your actual ORCID

2. **Update affiliation** (line 14 and 16-17):
   - Replace "Independent Researcher, USA" with your actual affiliation
   - Or keep as independent if that's accurate

3. **Add co-authors** (if any):
   - Add additional author entries in the `authors:` section

## Submission Process

### 1. Finalize Paper Content

```bash
# Edit paper.md with your info
nano paper.md

# Update ORCID (line 12)
# Update affiliation (lines 14, 16-17)
# Review all sections
```

### 2. Test Paper Rendering

Install JOSS dependencies:

```bash
# Install Pandoc
sudo apt-get install pandoc  # Linux
brew install pandoc          # macOS

# Install pandoc-citeproc
sudo apt-get install pandoc-citeproc  # Linux
brew install pandoc-citeproc          # macOS
```

Generate PDF preview:

```bash
pandoc paper.md --bibliography paper.bib --citeproc -o paper.pdf
```

Review `paper.pdf` to ensure formatting is correct.

### 3. Create a Release

JOSS requires a versioned release:

```bash
# Tag the release
git tag -a v2.0.0 -m "Version 2.0.0 for JOSS submission"
git push origin v2.0.0

# Create GitHub Release
# Go to: https://github.com/MissCrispenCakes/On-body-haptics/releases
# Click "Create a new release"
# Select tag: v2.0.0
# Title: "v2.0.0 - JOSS Submission"
# Description: Copy from CHANGELOG.md
# Publish release
```

### 4. Archive on Zenodo (Recommended)

Get a DOI for your software:

1. Connect repository to Zenodo:
   - Go to https://zenodo.org/account/settings/github/
   - Find On-body-haptics and flip the switch ON

2. Zenodo will automatically archive your v2.0.0 release

3. Get your DOI from Zenodo

4. Update `paper.md` with the DOI in the archive section

### 5. Submit to JOSS

1. Go to https://joss.theoj.org/papers/new

2. Fill in the submission form:
   - **Repository URL**: https://github.com/MissCrispenCakes/On-body-haptics
   - **Version**: v2.0.0
   - **Archive DOI**: Your Zenodo DOI (from step 4)
   - **Editor**: Select "Any available editor"

3. Click "Submit"

4. You'll receive a submission issue on JOSS's GitHub repository

### 6. Review Process

The JOSS review typically involves:

1. **Editor Assignment** - An editor will be assigned to your submission
2. **Reviewer Assignment** - 2-3 reviewers will be assigned
3. **Review** - Reviewers check:
   - Software functionality
   - Documentation quality
   - Installation instructions
   - Test coverage
   - Paper content

4. **Revisions** - Address reviewer comments (usually minor)
5. **Acceptance** - Once approved, paper is published

**Timeline**: Typical review takes 4-8 weeks.

## Common Review Comments

Based on typical JOSS reviews, be prepared to address:

### Documentation
- ✅ Installation instructions (we have detailed quick-starts)
- ✅ API documentation (we have OSC protocol spec)
- ✅ Examples (we have integration examples)

### Testing
- ⚠️ May need to expand test coverage
- Add more unit tests if reviewers request

### Paper
- May need to expand comparison with related work
- May need to add more citations
- May need to clarify technical details

## After Acceptance

Once your paper is accepted:

1. **Update README** with JOSS badge:
   ```markdown
   [![JOSS](https://joss.theoj.org/papers/10.21105/joss.XXXXX/status.svg)](https://joss.theoj.org/papers/10.21105/joss.XXXXX)
   ```

2. **Update CITATION.cff** with DOI:
   ```yaml
   identifiers:
     - type: doi
       value: 10.21105/joss.XXXXX
   ```

3. **Announce** on social media, mailing lists, etc.

## Resources

- [JOSS Submission Guidelines](https://joss.readthedocs.io/en/latest/submitting.html)
- [JOSS Review Criteria](https://joss.readthedocs.io/en/latest/review_criteria.html)
- [JOSS Paper Format](https://joss.readthedocs.io/en/latest/submitting.html#paper-format)
- [Example JOSS Papers](https://joss.theoj.org/papers/published)

## Questions?

- JOSS Help: https://joss.theoj.org/about#contact
- GitHub Discussions: https://github.com/MissCrispenCakes/On-body-haptics/discussions

---

**Ready to submit?** Follow steps 1-5 above! 🎓
