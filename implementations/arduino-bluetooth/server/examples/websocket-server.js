/**
 * WebSocket to OSC Bridge Example
 *
 * Creates a WebSocket server that receives messages from web clients
 * and forwards them as OSC messages to the haptic server.
 *
 * Usage:
 *   node examples/websocket-server.js
 *
 * Configuration:
 *   Update the IP addresses and ports below to match your setup.
 *
 * Client Usage:
 *   Send "sendHaptics" via WebSocket to trigger a pattern
 */

const WebSocket = require('ws');
const osc = require('osc');

// Configuration
const WS_PORT = 8080;
const OSC_LOCAL_PORT = 9999;
const OSC_REMOTE_ADDRESS = "127.0.0.1";  // Replace with your haptic server IP
const OSC_REMOTE_PORT = 9998;

// Create WebSocket server
const wss = new WebSocket.Server({ port: WS_PORT });

console.log(`WebSocket server listening on port ${WS_PORT}`);
console.log(`OSC messages will be sent to ${OSC_REMOTE_ADDRESS}:${OSC_REMOTE_PORT}\n`);

// Handle WebSocket connections
wss.on('connection', function connection(ws) {
    console.log('Client connected');

    // Create OSC UDP port for this client
    let udpPort = new osc.UDPPort({
        localAddress: "0.0.0.0",
        localPort: OSC_LOCAL_PORT,
        remoteAddress: OSC_REMOTE_ADDRESS,
        remotePort: OSC_REMOTE_PORT,
        metadata: true
    });

    // Handle messages from WebSocket client
    ws.on('message', function(msg) {
        console.log('Received from client:', msg);

        if (msg == "sendHaptics") {
            udpPort.open();

            // Send haptic pattern to all 8 buzzers on belt 1
            for (let i = 0; i < 8; i++) {
                let belt = 1;
                let buzzer = i;
                let pattern = 52;
                let duration = 0.5;

                sendHapticCommand(belt, buzzer, pattern, duration);
            }
        }
    });

    ws.on('close', function() {
        console.log('Client disconnected');
        if (udpPort) {
            udpPort.close();
        }
    });

    // Helper function to send OSC haptic command
    function sendHapticCommand(belt, buzzer, pattern, duration) {
        let bodyHaptics = {
            address: `/belt_${belt}/buzzer_${buzzer}/frequency`,
            args: [
                {
                    type: "i",
                    value: pattern
                },
                {
                    type: "i",
                    value: duration
                }
            ]
        };

        console.log("Sending OSC:", bodyHaptics.address, bodyHaptics.args);
        udpPort.send(bodyHaptics);
    }
});
