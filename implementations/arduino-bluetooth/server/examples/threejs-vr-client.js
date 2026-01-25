/**
 * Three.js VR Client Example
 *
 * Demonstrates integration of haptic feedback with VR head tracking.
 * When the user's head/gaze intersects with objects in the scene,
 * haptic feedback is triggered via WebSocket.
 *
 * Usage:
 *   Include this in your Three.js VR application
 *   Requires a WebSocket server (see websocket-server.js example)
 *
 * Dependencies:
 *   - three.js
 *   - WebSocket connection to haptic server
 */

/**
 * Check for head/gaze intersection with scene objects
 * Triggers haptic feedback when intersection occurs
 *
 * @param {THREE.Raycaster} raycaster - Three.js raycaster for intersection testing
 * @param {THREE.Camera} camera - VR camera
 * @param {THREE.Object3D} user - User object containing interactive children
 * @param {WebSocket} sock - WebSocket connection to haptic server
 */
function intersectHead(raycaster, camera, user, sock) {
    // Cast ray from center of camera view
    raycaster.setFromCamera({ x: 0, y: 0 }, camera);
    let intersects = raycaster.intersectObjects(user.children);

    if (intersects.length > 0) {
        console.log('Head intersection detected');

        if (intersected != intersects[0].object) {
            // Reset previous intersection highlight
            if (intersected) {
                intersected.material.emissive.setHex(intersected.currentHex);
            }

            // Highlight new intersection
            intersected = intersects[0].object;
            intersected.currentHex = intersected.material.emissive.getHex();
            intersected.material.emissive.setHex(0xff0000);

            // Send haptic feedback
            if (intersected && sock) {
                try {
                    sock.send("sendHaptics");
                } catch (e) {
                    console.error('Failed to send haptic command:', e);
                }
            }
        }
    } else {
        // No intersection - reset highlight
        if (intersected) {
            intersected.material.emissive.setHex(intersected.currentHex);
        }
        intersected = undefined;
    }
}

// Example integration in VR render loop:
//
// let raycaster = new THREE.Raycaster();
// let intersected;
//
// function animate() {
//     renderer.setAnimationLoop(render);
// }
//
// function render() {
//     intersectHead(raycaster, camera, userObject, websocket);
//     renderer.render(scene, camera);
// }
