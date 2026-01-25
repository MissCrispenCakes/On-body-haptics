/**
 * Haptic Server Core Library
 *
 * OSC server for routing haptic feedback commands to Arduino devices via Bluetooth.
 * Supports multiple belts with individual buzzer control and pre-programmed patterns.
 */

const osc = require('osc-min');
const dgram = require('dgram');
const { spawn } = require('child_process');
const ConfigLoader = require('./config-loader');

class HapticServer {
  /**
   * @param {Object} options - Server configuration options
   * @param {string} options.host - Host address to bind to
   * @param {number} options.port - Port to listen on
   * @param {string} options.configPath - Path to configuration directory
   * @param {string} options.bluetoothScript - Path to Bluetooth bridge script
   */
  constructor(options = {}) {
    this.configLoader = new ConfigLoader(options.configPath);
    this.config = this.configLoader.load();

    this.host = options.host || this.config.osc.address;
    this.port = options.port || this.config.osc.receivePort;
    this.bluetoothScript = options.bluetoothScript || './bluetooth-bridge.py';

    this.udp = null;
    this.remoteAddress = null;
    this.remotePort = null;

    // OSC message regex pattern for belt addressing
    // Matches: /belt_{1-6}/buzzer_{1-5}/(repetitions|frequency)
    //       OR /belt_{1-6}/pattern_{1-4}/(repetitions|frequency)
    this.oscRegex = /(\/belt_(?<beltb>[1-6]){1}\/buzzer_(?<buzzer>[1-5]){1}\/((repititions)|(frequency)))|(\/belt_(?<beltp>[1-6]){1}\/pattern_(?<pattern>[1-4]){1}\/((repititions)|(frequency)))/;

    this.bluetoothDevices = this.config.bluetooth.devices || [];
  }

  /**
   * Start the OSC server
   */
  start() {
    this.udp = dgram.createSocket('udp4');

    this.udp.on('message', (msg, rinfo) => this.handleMessage(msg, rinfo));
    this.udp.on('error', (err) => this.handleError(err));
    this.udp.on('listening', () => this.handleListening());

    this.udp.bind({
      port: this.port,
      exclusive: true
    });

    this.setupSignalHandlers();
  }

  /**
   * Handle incoming OSC message
   * @param {Buffer} msg - OSC message buffer
   * @param {Object} rinfo - Remote address info
   */
  handleMessage(msg, rinfo) {
    this.remoteAddress = rinfo.address;
    this.remotePort = rinfo.port;

    try {
      const incoming = osc.fromBuffer(msg);
      if (!incoming) {
        return;
      }

      const oscPath = incoming.address;
      const oscArgs = incoming.args;

      const match = oscPath.match(this.oscRegex);

      if (match) {
        this.processHapticCommand(match, oscArgs);
      } else {
        console.log('OSC message does not match expected pattern:', oscPath);
      }
    } catch (err) {
      console.error('Could not decode OSC message:', err.message);
    }
  }

  /**
   * Process validated haptic command
   * @param {Object} match - Regex match object with groups
   * @param {Array} oscArgs - OSC message arguments
   */
  processHapticCommand(match, oscArgs) {
    const tags = match.groups;

    let belt, commandType, commandValue;

    // Determine if it's a buzzer or pattern command
    if (tags.buzzer) {
      belt = tags.beltb;
      commandType = 1; // Buzzer
      commandValue = tags.buzzer;
      console.log(`Buzzer command: Belt ${belt}, Buzzer ${commandValue}`);
    } else if (tags.pattern) {
      belt = tags.beltp;
      commandType = 2; // Pattern
      commandValue = tags.pattern;
      console.log(`Pattern command: Belt ${belt}, Pattern ${commandValue}`);
    } else {
      console.warn('Malformed OSC command - no buzzer or pattern found');
      return;
    }

    // Extract repetitions and frequency from OSC arguments
    const repetitions = oscArgs[0]?.value || 0;
    const frequency = oscArgs[1]?.value || 0;

    console.log(`Repetitions: ${repetitions}, Frequency: ${frequency}`);

    // Build command string for Arduino
    // Format: [commandType][commandValue][repetitions][frequency]
    const command = `${commandType}${commandValue}${repetitions}${frequency}`;

    // Send to appropriate belt(s)
    this.sendToBelt(belt, command);
  }

  /**
   * Send command to specific belt(s) via Bluetooth
   * @param {string} belt - Belt number (1-6, where 6 = all belts)
   * @param {string} command - Command string to send
   */
  sendToBelt(belt, command) {
    const beltNum = parseInt(belt);

    if (beltNum === 6) {
      // Send to all configured belts
      console.log(`Sending to all belts: ${command}`);
      this.bluetoothDevices.forEach(device => {
        this.sendBluetooth(device.mac, command);
      });
    } else {
      // Send to specific belt
      const device = this.bluetoothDevices.find(d => d.id === beltNum);
      if (device) {
        console.log(`Sending to Belt ${beltNum} (${device.name}): ${command}`);
        this.sendBluetooth(device.mac, command);
      } else {
        console.warn(`Belt ${beltNum} not configured`);
      }
    }
  }

  /**
   * Send command via Bluetooth bridge script
   * @param {string} macAddress - Bluetooth MAC address
   * @param {string} command - Command string to send
   */
  sendBluetooth(macAddress, command) {
    if (macAddress.includes('REPLACE_WITH') || macAddress.includes('XX:XX')) {
      console.error(`Cannot send to placeholder MAC address: ${macAddress}`);
      return;
    }

    try {
      spawn('python', [this.bluetoothScript, macAddress, command]);
    } catch (err) {
      console.error(`Failed to spawn Bluetooth bridge: ${err.message}`);
    }
  }

  /**
   * Handle UDP socket error
   */
  handleError(err) {
    console.error('UDP socket error:', err.message);
    process.kill(process.pid, 'SIGINT');
  }

  /**
   * Handle server listening event
   */
  handleListening() {
    console.log(`Haptic Server listening for OSC messages on: ${this.host}:${this.port}`);
    console.log(`Configured ${this.bluetoothDevices.length} Bluetooth device(s)`);
  }

  /**
   * Stop the server
   */
  stop() {
    if (this.udp) {
      this.udp.close(() => {
        console.log('Haptic Server stopped');
      });
    }
  }

  /**
   * Setup process signal handlers for graceful shutdown
   */
  setupSignalHandlers() {
    process.on('SIGINT', () => {
      this.udp.close(() => {
        console.log('SIGINT received - server closed');
        process.exit(0);
      });
    });

    process.on('SIGTERM', () => {
      this.udp.close(() => {
        console.log(`SIGTERM received - server closed (check for bound port: netstat -nlp | grep :${this.port})`);
        process.kill(process.pid, 'SIGINT');
        process.exit(1);
      });
    });
  }
}

module.exports = HapticServer;
