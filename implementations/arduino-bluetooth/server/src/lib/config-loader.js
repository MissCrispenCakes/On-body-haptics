/**
 * Configuration Management Module
 *
 * Loads and validates configuration from JSON files.
 * Supports default config with environment-specific overrides.
 */

const fs = require('fs');
const path = require('path');

class ConfigLoader {
  constructor(configDir = null) {
    this.configDir = configDir || path.join(__dirname, '../../config');
    this.config = null;
  }

  /**
   * Load configuration from default.json
   * @returns {Object} Configuration object
   */
  load() {
    const defaultPath = path.join(this.configDir, 'default.json');

    if (!fs.existsSync(defaultPath)) {
      throw new Error(`Configuration file not found: ${defaultPath}`);
    }

    try {
      const configData = fs.readFileSync(defaultPath, 'utf8');
      this.config = JSON.parse(configData);
      return this.config;
    } catch (err) {
      throw new Error(`Failed to parse configuration: ${err.message}`);
    }
  }

  /**
   * Get configuration value by path (e.g., 'osc.receivePort')
   * @param {string} keyPath - Dot-notation path to config value
   * @param {*} defaultValue - Default value if path not found
   * @returns {*} Configuration value
   */
  get(keyPath, defaultValue = null) {
    if (!this.config) {
      this.load();
    }

    const keys = keyPath.split('.');
    let value = this.config;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }

    return value;
  }

  /**
   * Validate required configuration values
   * @throws {Error} If validation fails
   */
  validate() {
    if (!this.config) {
      this.load();
    }

    const required = [
      'osc.receivePort',
      'bluetooth.devices',
      'server.name'
    ];

    for (const key of required) {
      const value = this.get(key);
      if (value === null || value === undefined) {
        throw new Error(`Required configuration missing: ${key}`);
      }
    }

    // Check for placeholder MAC addresses
    const devices = this.get('bluetooth.devices', []);
    for (const device of devices) {
      if (device.mac.includes('REPLACE_WITH') || device.mac.includes('XX:XX')) {
        console.warn(`Warning: Bluetooth device ${device.id} has placeholder MAC address`);
      }
    }
  }
}

module.exports = ConfigLoader;
