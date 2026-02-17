# Security Policy

## Overview

On-Body Haptics is an open-source project for building wearable haptic feedback systems. While this project is primarily intended for research, education, and personal use, we take security seriously.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Security Considerations

### Network Security

#### OSC Protocol
- **No built-in authentication**: The OSC (Open Sound Control) protocol does not include authentication or encryption
- **Network exposure**: OSC servers bind to network interfaces and accept UDP packets
- **Recommendations**:
  - Run on isolated networks (separate VLAN or local-only network)
  - Use firewall rules to restrict access to OSC ports
  - Consider VPN or SSH tunneling for remote access
  - Do not expose OSC ports to the internet without additional security layers

#### WiFi (Raspberry Pi Implementation)
- **Default credentials**: Raspberry Pi OS ships with default credentials (user: `pi`, password: `raspberry`)
- **⚠️ CRITICAL**: Change default password immediately after setup:
  ```bash
  passwd
  ```
- Use WPA2/WPA3 for WiFi encryption
- Consider using a dedicated WiFi network for haptic devices

#### Bluetooth (Arduino Implementation)
- **Pairing security**: HC-05/HC-06 modules use PIN-based pairing (default: `1234` or `0000`)
- **⚠️ CRITICAL**: Change Bluetooth PIN using AT commands:
  ```
  AT+PSWD=<your-pin>
  ```
- Bluetooth range is typically limited to ~10 meters, providing some physical security
- Consider disabling Bluetooth when not in use

### Configuration Security

#### Credential Management
- **Never commit credentials**: Configuration files with real MAC addresses, passwords, or API keys should never be committed to version control
- **Use .gitignore**: Sensitive config files are already in `.gitignore` (`config/local.json`, `config/production.json`, `.env`)
- **Environment variables**: For production deployments, use environment variables or secrets management
- **Configuration files**:
  - Arduino implementation: `implementations/arduino-bluetooth/server/config/local.json`
  - Raspberry Pi implementation: `implementations/raspberry-pi-i2c/firmware/src/config_local.py`

#### Systemd Services (Raspberry Pi)
- **Default user**: Example systemd services run as user `pi`
- **Recommendation**: Create a dedicated user with minimal permissions:
  ```bash
  sudo useradd -r -s /bin/false octopulse
  sudo usermod -a -G i2c,gpio octopulse
  ```
- Edit service files to use dedicated user:
  ```ini
  [Service]
  User=octopulse
  Group=octopulse
  ```

### Hardware Security

#### Physical Access
- Devices with physical access can be tampered with
- Consider tamper-evident enclosures for sensitive deployments
- Store devices securely when not in use

#### I2C Security
- I2C bus has no built-in security mechanisms
- Physical access to I2C bus allows device manipulation
- Use secure enclosures to prevent unauthorized access

### Software Security

#### Dependency Management
- Regularly update dependencies for security patches:
  ```bash
  # Node.js
  npm audit
  npm update

  # Python
  pip list --outdated
  pip install --upgrade <package>
  ```

#### Code Execution
- This project executes code on embedded devices and servers
- Review all code before deployment
- Use virtual environments (Python) and project-local dependencies (Node.js)

### Data Privacy

#### Network Traffic
- OSC messages are transmitted in cleartext
- Haptic patterns may reveal sensitive information about user activity
- Consider data retention policies for logs

#### Logging
- Default configuration logs to console
- Enable file logging only when necessary
- Rotate logs and limit retention time
- Review logs for sensitive information before sharing

## Known Security Limitations

### 1. OSC Protocol
- **Limitation**: No authentication, no encryption
- **Impact**: Anyone on the network can send commands
- **Mitigation**: Use network isolation, firewall rules, or VPN

### 2. Default Credentials
- **Limitation**: Raspberry Pi default credentials are well-known
- **Impact**: Unauthorized access if not changed
- **Mitigation**: Change password immediately after setup

### 3. Bluetooth PIN
- **Limitation**: Default PIN is easily guessable
- **Impact**: Unauthorized Bluetooth pairing
- **Mitigation**: Change PIN using AT commands

### 4. No Rate Limiting
- **Limitation**: OSC server does not implement rate limiting
- **Impact**: Potential denial of service or device damage from excessive commands
- **Mitigation**: Implement rate limiting at network or application level

### 5. No Command Validation
- **Limitation**: Minimal validation of OSC message parameters
- **Impact**: Invalid commands may cause unexpected behavior
- **Mitigation**: Use validated client libraries and implement input validation

## Best Practices

### For Development
1. Use example configurations with sanitized values
2. Never commit real MAC addresses, IPs, or credentials
3. Test security configurations before deployment
4. Review code changes for security implications
5. Keep dependencies up to date

### For Production
1. Change all default credentials
2. Use dedicated user accounts with minimal permissions
3. Implement network segmentation
4. Enable firewall rules to restrict access
5. Use VPN or SSH tunneling for remote access
6. Regularly update software and dependencies
7. Monitor logs for suspicious activity
8. Implement rate limiting at network level
9. Use hardware security (enclosures, physical access control)
10. Document security configurations

### For Research/Educational Use
1. Inform participants about data collection and network traffic
2. Obtain consent for data usage
3. Follow institutional review board (IRB) guidelines
4. Secure data storage and transmission
5. Implement data retention and deletion policies

## Reporting a Vulnerability

If you discover a security vulnerability in On-Body Haptics, please report it responsibly:

1. **Do NOT open a public GitHub issue**
2. **Email**: workscv@yorku.ca
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### Response Timeline
- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Fix timeline**: Depends on severity (critical: 7 days, high: 30 days, medium: 90 days)

### Disclosure Policy
- We follow responsible disclosure practices
- Public disclosure only after patch is available
- Credit given to reporters (unless anonymity requested)

## Security Updates

Security updates will be released as patch versions and announced via:
- GitHub Security Advisories
- Release notes
- Project README

Subscribe to repository notifications to stay informed.

## Compliance

### Open Source License
- This project is licensed under MIT License
- No warranties provided (see LICENSE file)
- Use at your own risk

### Research Use
- Follow institutional guidelines for human subjects research
- Obtain necessary approvals (IRB, ethics committee)
- Comply with data protection regulations (GDPR, CCPA, etc.)

## Additional Resources

- [OWASP IoT Security Project](https://owasp.org/www-project-internet-of-things/)
- Raspberry Pi Security Guidelines (see official Raspberry Pi documentation)
- [OSC Protocol Specification](http://opensoundcontrol.org/spec-1_0)

## Acknowledgments

We thank the security research community for helping keep this project secure.

---

**Last Updated**: 2026-02-17
**Version**: 2.0.0
