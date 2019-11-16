// Haptics
let bodyHaptics;
let udpPort = new osc.UDPPort({
		// This is where Clyde is listening on
		localAddress: "ISP goes here"
		localPort: 8080, //9999

		// This is where pi is listening for OSC messages.
		remoteAddress: "ISP goes here"
		remotePort: 3030,
		metadata: true
});


	// respond to any messages from the client:
	ws.on('message', function(msg) {

		if (msg == "sendHaptics") {

				// Open the socket.
				udpPort.open();
	
				function send(b,z,p,d) {
	
					bodyHaptics = {
								address: `/belt_${b}/buzz_${z}/`,
								args: [
										{
												type: "i",
												value: p
										},
										{
												type: "i",
												value: d
										}
								]
						};
	
						console.log("Sending message", bodyHaptics.address, bodyHaptics.args, "to", udpPort.options.remoteAddress + ":" + udpPort.options.remotePort);
						udpPort.send(bodyHaptics);
	
				};
	
				for ( let i = 0; i < 8; i++ ){
					let b = 1; //belt
					let z = i; //buzzer
					let p = 52; //pattern
					let d = 0.5; //duration
					
					send(b,z,p,d);
				};

			} else {
				console.log("received message from client:", id, msg);
			}
		};
