#!/usr/bin/env node
/**
 * On-Body Haptics Server
 *
 * Entry point for the OSC-to-Bluetooth haptic feedback server.
 * Receives OSC messages and routes them to Arduino devices via Bluetooth.
 *
 * Usage:
 *   node src/index.js [host] [port]
 *
 * Example:
 *   node src/index.js 0.0.0.0 9999
 *
 * If no arguments provided, uses values from config/default.json
 */

const path = require('path');
const HapticServer = require('./lib/haptic-server');

// Parse command line arguments
const host = process.argv[2];
const port = process.argv[3] ? Number(process.argv[3]) : undefined;

// Create and start server
const server = new HapticServer({
  host: host,
  port: port,
  bluetoothScript: path.join(__dirname, 'bluetooth-bridge.py')
});

try {
  server.start();
} catch (err) {
  console.error('Failed to start Haptic Server:', err.message);
  process.exit(1);
}
