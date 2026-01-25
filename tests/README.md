# Tests

Automated tests for the On-Body Haptics project.

## Structure

```
tests/
├── python/              # Python tests (pytest)
│   ├── conftest.py     # Pytest configuration
│   └── test_*.py       # Test files
└── integration/        # Integration tests
    └── test_*.py       # End-to-end tests
```

## Running Tests

### Python Tests

```bash
# Install test dependencies
pip install pytest python-osc

# Run all tests
pytest tests/python/

# Run with verbose output
pytest tests/python/ -v

# Run specific test file
pytest tests/python/test_osc_protocol.py

# Run with coverage
pip install pytest-cov
pytest tests/python/ --cov=implementations
```

### Integration Tests

Integration tests require actual hardware or mocking:

```bash
# Run integration tests (requires hardware or mocks)
pytest tests/integration/ -v

# Skip hardware tests
pytest tests/integration/ -v -m "not hardware"
```

## Test Categories

### Unit Tests (`tests/python/`)
- OSC protocol validation
- Configuration validation
- Message format testing
- Pattern/effect ID validation

### Integration Tests (`tests/integration/`)
- End-to-end OSC message flow
- Hardware communication (requires actual devices)
- Network communication
- Multi-device coordination

## Writing Tests

### Test File Naming

- `test_*.py` - Test files
- `*_test.py` - Alternative naming

### Test Function Naming

```python
def test_feature_description():
    """Test that feature works as expected"""
    # Arrange
    # Act
    # Assert
```

### Using Fixtures

```python
def test_with_fixture(mock_osc_server, sample_patterns):
    """Test using pytest fixtures"""
    assert "CW" in sample_patterns
```

### Marking Tests

```python
import pytest

@pytest.mark.hardware
def test_requires_hardware():
    """Test that requires actual hardware"""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Test that takes a long time"""
    pass

# Skip hardware tests by default
pytest tests/ -m "not hardware"
```

## Mocking Hardware

For tests that require hardware, use mocks:

```python
from unittest.mock import Mock, patch

def test_i2c_communication():
    """Test I2C communication with mocked hardware"""
    with patch('adafruit_drv2605.DRV2605') as mock_drv:
        # Setup mock
        mock_device = Mock()
        mock_drv.return_value = mock_device

        # Test code
        device = mock_drv()
        device.play()

        # Verify
        mock_device.play.assert_called_once()
```

## Continuous Integration

Tests run automatically on GitHub Actions:
- Arduino CI: Compile checks
- Python CI: Lint and syntax checks
- Documentation CI: Markdown linting

See `.github/workflows/` for CI configuration.

## Test Coverage

Check test coverage:

```bash
pytest tests/ --cov=implementations --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Test Guidelines

### Do's
- ✅ Test one thing per test function
- ✅ Use descriptive test names
- ✅ Use fixtures for common setup
- ✅ Mock hardware dependencies
- ✅ Test edge cases and error conditions
- ✅ Keep tests fast and independent

### Don'ts
- ❌ Don't test external libraries (pytest, osc-min, etc.)
- ❌ Don't require hardware for unit tests
- ❌ Don't use sleep() unless absolutely necessary
- ❌ Don't make tests depend on each other
- ❌ Don't test implementation details

## Example Test

```python
import pytest
from pythonosc import osc_message_builder


def test_osc_message_format():
    """Test OSC message creation and format"""
    # Arrange
    address = "/onbody/1/pattern"
    pattern = "CW"

    # Act
    builder = osc_message_builder.OscMessageBuilder(address=address)
    builder.add_arg(pattern)
    msg = builder.build()

    # Assert
    assert msg.address == address
    assert msg.params[0] == pattern
```

## Contributing Tests

When adding new features:
1. Write tests first (TDD)
2. Ensure tests pass before submitting PR
3. Aim for >80% code coverage
4. Document complex test scenarios

## Troubleshooting

### Import Errors

```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use editable install
pip install -e implementations/raspberry-pi-i2c/firmware/
```

### Pytest Not Found

```bash
pip install pytest
```

### Hardware Tests Failing

```bash
# Skip hardware tests
pytest -m "not hardware"

# Or mark tests as expected to fail
@pytest.mark.xfail(reason="Requires hardware")
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python OSC Documentation](https://pypi.org/project/python-osc/)
- [Mocking in Python](https://docs.python.org/3/library/unittest.mock.html)
