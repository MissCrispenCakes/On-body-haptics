# Contributing to On-Body Haptics

Thank you for your interest in contributing! This project welcomes contributions from everyone.

## Ways to Contribute

- 🐛 **Report bugs** - Help us identify issues
- 💡 **Suggest features** - Share your ideas
- 📖 **Improve documentation** - Fix typos, add examples, clarify instructions
- 🔧 **Submit code** - Fix bugs, add features, improve performance
- 🎨 **Hardware designs** - Improve PCBs, enclosures, or create new designs
- 🧪 **Testing** - Test on different platforms and configurations
- 💬 **Community support** - Help others in Discussions

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/On-body-haptics.git
   cd On-body-haptics
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

## Development Setup

### Arduino Implementation

```bash
cd implementations/arduino-bluetooth/server
npm install
```

### Raspberry Pi Implementation

```bash
cd implementations/raspberry-pi-i2c/firmware
pip install -r requirements.txt
```

## Making Changes

### Code Style

#### Python
- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate
- Add docstrings to functions and classes

#### JavaScript/Node.js
- Use 2 spaces for indentation
- Use semicolons
- Prefer `const` and `let` over `var`
- Use template literals for string formatting
- Add JSDoc comments for functions

#### Arduino/C++
- Use 2 spaces for indentation
- Follow Arduino style guide
- Use descriptive variable names
- Add comments for complex logic

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Support for custom effect library

- Implement custom effect loading from JSON
- Add validation for effect parameters
- Update documentation with examples

Closes #123
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrap at 72 chars)
- Reference issues/PRs

### Documentation

- Update relevant documentation when changing functionality
- Add examples for new features
- Update README if needed
- Check for broken links

## Submitting Changes

### Pull Request Process

1. **Update your branch** with latest `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**:
   - Verify code works on actual hardware (if possible)
   - Check for syntax errors
   - Run any available tests

3. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-feature
   ```

4. **Create Pull Request** on GitHub:
   - Use a clear title
   - Describe what changed and why
   - Reference related issues
   - Add screenshots/videos if relevant

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Hardware design
- [ ] Other (describe)

## Testing
How has this been tested?

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tested on hardware (if applicable)
- [ ] No breaking changes (or documented)
```

## Reporting Bugs

### Before Submitting

1. **Check existing issues** - Has it been reported?
2. **Try latest version** - Is it still a problem?
3. **Minimal reproduction** - Can you provide steps to reproduce?

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Run command '...'
3. See error

**Expected behavior**
What should have happened?

**Screenshots/Logs**
If applicable, add screenshots or logs

**Environment:**
- Platform: [Arduino/Raspberry Pi]
- OS: [Windows/Linux/macOS]
- Version: [e.g., 2.0.0]
- Hardware: [e.g., Arduino Uno, Raspberry Pi 4]

**Additional context**
Any other relevant information
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of what you want

**Describe alternatives considered**
Other solutions you've considered

**Additional context**
Mockups, examples, references, etc.
```

## Hardware Contributions

### PCB Designs

- Provide KiCad project files
- Include Gerber files
- Document BOM with part numbers
- Add assembly instructions
- Include photos of built hardware

### 3D Models

- Provide source files (OpenSCAD, Fusion 360, etc.)
- Include STL files ready for printing
- Document print settings
- Add assembly instructions

## Code Review Process

1. **Maintainer review** - Within 7 days
2. **Discussion** - Address feedback and questions
3. **Approval** - At least one maintainer approval required
4. **Merge** - Squash and merge into `main`

## Community Guidelines

### Code of Conduct

Be respectful and inclusive. We follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

### Communication

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions, ideas, show-and-tell
- **Pull Requests** - Code contributions

### Response Times

- **Issues**: Initial response within 7 days
- **Pull Requests**: Review within 14 days
- **Security issues**: Response within 48 hours

## Recognition

Contributors are recognized in:
- Release notes
- README acknowledgments
- Git commit history

Significant contributors may be invited as project maintainers.

## Questions?

Don't hesitate to ask questions in [GitHub Discussions](https://github.com/yourusername/On-body-haptics/discussions)!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to On-Body Haptics!** 🎉
