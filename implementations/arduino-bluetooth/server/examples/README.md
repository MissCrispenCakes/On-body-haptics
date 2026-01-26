# Arduino Bluetooth Server Examples

This directory contains example implementations showing different ways to use the On-Body Haptics system.

## Examples Overview

### 1. send-pattern.js - Basic OSC Pattern Sender

**What it does:** Sends a simple haptic pattern every second via OSC protocol

**Use case:** Testing the system, learning the OSC message format

**Usage:**
```bash
node examples/send-pattern.js
```

**Configuration:**
- Update `remoteAddress` to point to your haptic server's IP
- Update `remotePort` to match your haptic server's OSC port (default: 9998)

### 2. websocket-server.js - WebSocket to OSC Bridge

**What it does:** Creates a WebSocket server that receives messages from web clients and forwards them as OSC commands to the haptic server

**Use case:** Web-based applications, browser-based controls, VR web apps

**Usage:**
```bash
node examples/websocket-server.js
```

**Configuration:**
- `WS_PORT`: WebSocket server port (default: 8080)
- `OSC_REMOTE_ADDRESS`: IP of your haptic server
- `OSC_REMOTE_PORT`: OSC port of your haptic server (default: 9998)

**Client Usage:**
Connect to the WebSocket server and send the string `"sendHaptics"` to trigger a pattern

Example client code:
```javascript
const ws = new WebSocket('ws://localhost:8080');
ws.onopen = () => {
    ws.send('sendHaptics');
};
```

### 3. threejs-vr-client.js - VR Head Tracking Integration

**What it does:** Demonstrates how to integrate haptic feedback with Three.js VR applications using head/gaze tracking

**Use case:** WebXR applications, VR experiences, interactive 3D environments

**Usage:**
Include this module in your Three.js VR application and call `intersectHead()` in your render loop

**Integration:**
```javascript
import { intersectHead } from './threejs-vr-client.js';

let raycaster = new THREE.Raycaster();
let websocket = new WebSocket('ws://localhost:8080');

function render() {
    intersectHead(raycaster, camera, userObject, websocket);
    renderer.render(scene, camera);
}
```

## Example Integration Workflow

1. **Start the haptic server:**
   ```bash
   node src/index.js 0.0.0.0 9998
   ```

2. **Start the WebSocket bridge (if needed):**
   ```bash
   node examples/websocket-server.js
   ```

3. **Test with pattern sender:**
   ```bash
   node examples/send-pattern.js
   ```

## Dependencies

All examples require the `osc` package:
```bash
npm install osc
```

The WebSocket example also requires:
```bash
npm install ws
```

The Three.js example requires Three.js in your web application:
```bash
npm install three
```

## Custom Examples

These examples serve as starting points. You can:

- Modify the OSC message format to target different belts/buzzers
- Change pattern parameters (repetitions, frequency)
- Create custom WebSocket message protocols
- Integrate with other 3D libraries or frameworks
- Build custom UIs for haptic control

## OSC Message Format

All examples use the standard OSC format:

**Buzzer control:**
```
/belt_{1-6}/buzzer_{1-5}/frequency
Arguments: [repetitions, frequency]
```

**Pattern control:**
```
/belt_{1-6}/pattern_{1-4}/frequency
Arguments: [repetitions, frequency]
```

**Belt 6 = All belts** (broadcasts to all configured devices)

## Troubleshooting

**"Cannot connect to server"**
- Verify the haptic server is running
- Check IP addresses and ports in your config
- Ensure firewall allows UDP (OSC) and TCP (WebSocket) connections

**"WebSocket connection refused"**
- Ensure websocket-server.js is running
- Check the WebSocket port (default: 8080)
- Verify client is connecting to correct address

**"No haptic feedback"**
- Check Bluetooth connections to Arduino devices
- Verify MAC addresses in `config/default.json`
- Check server console for error messages
- Ensure Arduino firmware is uploaded and running

## Additional Resources

- [OSC Protocol Specification](../../../../docs/api/osc-protocol.md)
- [Arduino API Documentation](../../../../docs/api/arduino-api.md)
- [Integration Guides](../../../../docs/integration/)
