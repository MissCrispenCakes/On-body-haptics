var osc = require("osc");

var udpPort = new osc.UDPPort({
    // This is the port we're listening on.
    localAddress: "192.168.1.xxx",  //replace with isp etc
    localPort: 9999,

    // This is where piguy is listening for OSC messages.
    remoteAddress: "xxx.xxx.xxx.xxx", //replace with isp
    remotePort: 9998,
    metadata: true
});

// Open the socket.
udpPort.open();

// test the system
// Every second, send an OSC message to piguy
setInterval(function() {
    var msg = {
        address: "/belt_3/pattern_4/frequency",
        args: [
            {
                type: "i",
                value: 2
            },
            {
                type: "i",
                value: 3
            }
        ]
    };

    console.log("Sending message", msg.address, msg.args, "to", udpPort.options.remoteAddress + ":" + udpPort.options.remotePort);
    udpPort.send(msg);

}, 1000);   

    // var msg = {
    //     address: "/belt_3/pattern_2/frequency",
    //     args: [
    //         {
    //             type: "i",
    //             value: 2
    //         },
    //         {
    //             type: "i",
    //             value: 2
    //         }
    //     ]
    // };

    // console.log("Sending message", msg.address, msg.args, "to", udpPort.options.remoteAddress + ":" + udpPort.options.remotePort);
    // udpPort.send(msg);

    // var msg = {
    //     address: "/belt_1/pattern_3/frequency",
    //     args: [
    //         {
    //             type: "i",
    //             value: 2
    //         },
    //         {
    //             type: "i",
    //             value: 2
    //         }
    //     ]
    // };

    // console.log("Sending message", msg.address, msg.args, "to", udpPort.options.remoteAddress + ":" + udpPort.options.remotePort);
    // udpPort.send(msg);


