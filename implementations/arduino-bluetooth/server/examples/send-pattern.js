/**
 * Send Pattern Example
 *
 * Simple example of sending haptic pattern commands via OSC.
 * Sends a test pattern every second to demonstrate the protocol.
 *
 * Usage:
 *   node examples/send-pattern.js
 *
 * Configuration:
 *   Update the IP addresses below to match your setup:
 *   - localAddress: This computer's IP address
 *   - remoteAddress: IP address of the haptic server
 */

var osc = require("osc");

// Configuration - Update these values for your setup
var udpPort = new osc.UDPPort({
    localAddress: "0.0.0.0",
    localPort: 9999,
    remoteAddress: "127.0.0.1",  // Replace with your haptic server IP
    remotePort: 9998,
    metadata: true
});

udpPort.open();

console.log("Starting OSC pattern test...");
console.log("Sending to: " + udpPort.options.remoteAddress + ":" + udpPort.options.remotePort);
console.log("Press Ctrl+C to stop\n");

// Send a test pattern every second
setInterval(function() {
    var msg = {
        address: "/belt_3/pattern_4/frequency",
        args: [
            {
                type: "i",
                value: 2  // Repetitions
            },
            {
                type: "i",
                value: 3  // Frequency
            }
        ]
    };

    console.log("Sending:", msg.address, "args:", msg.args);
    udpPort.send(msg);

}, 1000);


