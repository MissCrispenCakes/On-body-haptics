# Setting Up Zenodo Integration

This guide explains how to get a DOI (Digital Object Identifier) for your repository using Zenodo.

## What is Zenodo?

Zenodo is a free, open-access repository that allows you to archive your GitHub repository and get a citable DOI. This is essential for academic use.

## Benefits

- **Permanent DOI** - Citable identifier that never changes
- **Archival** - Your code is preserved even if GitHub goes down
- **Academic Recognition** - Proper citation in papers and research
- **Version Tracking** - Each release gets its own DOI

## Step-by-Step Setup

### 1. Create Zenodo Account

1. Go to https://zenodo.org
2. Click "Sign Up" or "Log In"
3. **Use GitHub to sign in** (recommended for integration)
4. Authorize Zenodo to access your GitHub account

### 2. Enable Repository

1. Once logged in, go to https://zenodo.org/account/settings/github/
2. Find "On-body-haptics" in the repository list
3. **Flip the switch to ON** ✅
4. Zenodo will now watch for new releases

### 3. Create a Release on GitHub

1. Go to your GitHub repository
2. Click **Releases** → **Create a new release**
3. Tag version: `v2.0.0` (already done, but for future releases)
4. Release title: `v2.0.0 - Repository Revitalization`
5. Description: Copy from CHANGELOG.md
6. Click **Publish release**

### 4. Get Your DOI

1. Go back to https://zenodo.org/account/settings/github/
2. You should see your repository with a new upload
3. Click on the upload to see the DOI
4. The DOI will look like: `10.5281/zenodo.XXXXXXX`

### 5. Add DOI Badge to README

Once you have your DOI, add this badge to README.md:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

Replace `XXXXXXX` with your actual DOI number.

### 6. Update Citation Files

Update these files with your DOI:

**CITATION.cff**:
```yaml
identifiers:
  - type: doi
    value: 10.5281/zenodo.XXXXXXX
```

**AUTHORS.md**:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

## Metadata Configuration

The `.zenodo.json` file in the repository root contains metadata for Zenodo:

### Required Edits

1. **Replace "Your Name"** with your actual name
2. **Add your ORCID** if you have one (optional but recommended)
   - Get one at https://orcid.org
3. **Update affiliation** with your institution
4. **Review keywords** - add/remove as needed

### Example:

```json
{
  "creators": [
    {
      "name": "Jane Doe",
      "affiliation": "University of Example",
      "orcid": "0000-0002-1234-5678"
    }
  ]
}
```

## ORCID (Optional but Recommended)

### What is ORCID?

ORCID (Open Researcher and Contributor ID) is a persistent digital identifier for researchers.

### Get Your ORCID:

1. Go to https://orcid.org/register
2. Create free account
3. Add to CITATION.cff and .zenodo.json

Format: `0000-0002-1234-5678` (16 digits)

## Future Releases

For each new version:

1. Update version number in:
   - CITATION.cff
   - CHANGELOG.md
   - README.md
2. Create new GitHub release
3. Zenodo automatically creates new version with new DOI
4. Update badges with new DOI

## Concept DOI vs Version DOI

Zenodo provides TWO DOIs:

- **Concept DOI**: Points to ALL versions (use in papers)
- **Version DOI**: Points to specific version (use for reproducibility)

Use the **Concept DOI** in most citations unless you need to reference a specific version.

## Troubleshooting

### Repository Not Showing Up

- Make sure you authorized Zenodo with GitHub
- Refresh the repository list
- Check that repository is public

### DOI Not Generated

- Make sure you created a **release**, not just a tag
- Wait a few minutes for processing
- Check Zenodo upload status

### Metadata Not Correct

- Edit `.zenodo.json` in your repository
- Create new release to update metadata

## Example Citation

Once you have your DOI, citations will look like:

```
MissCrispenCakes. (2026). On-Body Haptics: Open-Source Wearable Haptic
Feedback Systems (Version 2.0.0) [Computer software].
https://doi.org/10.5281/zenodo.XXXXXXX
```

## Resources

- [Zenodo GitHub Integration Guide](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)
- [Zenodo Help](https://help.zenodo.org/)
- [ORCID Registration](https://orcid.org/register)
- [Citation File Format (CFF)](https://citation-file-format.github.io/)

## Questions?

Open an issue on GitHub or check the [Zenodo FAQ](https://help.zenodo.org/faq/).

---

**Ready to set up?** Follow steps 1-6 above to get your DOI! 🎓
