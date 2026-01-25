// PI@local     'ISP' xxx.xxx.x..... etc

// /etc/bluetooth/rfcomm.conf  // can edit to bind bt

// HC06 0: mac addy xx:xx:xx:xx etc
// HC05 1: mac addy



// ******************************************************* //
// *************************BEGIN************************* //
// ******************************************************* //

const osc = require('osc-min')
const dgram = require('dgram')
//const fs = require('fs')
// const argv = require('minimist')
// const portScanner = require( 'portscanner' );

// const { spawn } = require( 'child_process' );
const { spawn, exec, execFile } = require('child_process')
// const { exec } = require( 'child_process' );
const { spawnSync, execSync, execFileSync } = require( 'child_process' )
// const { execFileSync } = require( 'child_process' )

// const grep = spawnSync( 'grep', [ 'ssh' ] )

// const initput = process.argv.slice(2)
const HOST = process.argv[2]
const PORT = Number(process.argv[3])

var remoteAddress
var remotePort

var regEx = /(\/belt_(?<beltb>[1-6]){1}\/buzzer_(?<buzzer>[1-5]){1}\/((repititions)|(frequency)))|(\/belt_(?<beltp>[1-6]){1}\/pattern_(?<pattern>[1-4]){1}\/((repititions)|(frequency)))/
//var regEx = /(\/belt_(?<belt>[1-6]){1}\/buzzer_(?<buzzer>[1-5]){1}\/((frequency)|(repititions)))|(\/belt_([1-5]){1}\/pattern_(?<pattern>[1-2]){1}\/((repititions)|(frequency)))/
//var regEx = /(\/belt_(?<belt>[1-6]){1})((\/buzzer_(?<buzzer>[1-5]){1}\/((frequency)|(repititions)))|(\/pattern_(?<pattern>[1-2]){1}\/((repititions)|(frequency))))/

var udp = dgram.createSocket('udp4')
udp.on('message', function (msg, rinfo) {
   remoteAddress = rinfo.address
   remotePort = rinfo.port
  try {
    var incoming = osc.fromBuffer(msg)
    if (incoming) {
      //console.log('\n----------------')
      //console.log('I have incoming:\n')
      //console.log(incoming)
      //console.log('\n')
      var incomingOSCPath = incoming.address
      var incomingOSCArgs = incoming.args
      var incomingOSCArgsLength = incomingOSCArgs.length

      //console.log(incoming.address, incoming['address'])
      //console.log('args: '+length, '\n', incoming.args[0]['value'], '\n', incoming.args[1]['type'])
      var match = incomingOSCPath.match( regEx )

      //console.log(incoming.address+'\n', incomingAddress+'\n', regEx000+'\n', incoming.args+'\n', incomingArguments+'\n')//, testReg1, testReg2)
      if(match) {
        var incomingTags = incomingOSCPath.match(regEx).groups;
        //console.log(incomingTags.pattern)      
        console.log('\n---------------')
        console.log('\nI have a RegExp')
        console.log('\n---------------')
        //console.log(incomingOSCPath)
      
        try {
          var buzz = incomingTags.buzzer  
          if(!buzz) {
            console.log("no buzzer")
          } else {
            console.log(buzz)
          }
        } catch (err) {

        }

        try {
          var patt = incomingTags.pattern
          if(!patt) {
            console.log("no pattern")
          } else {
            console.log(patt)
          }
        } catch (err) {
          //console.log("no pattern")
        }
               
        var reps = incomingOSCArgs[0]['value']
        console.log(reps)
        var freq = incomingOSCArgs[1]['value']
        console.log(freq)

        var count =  "";
        console.log(count)
        if(buzz){
          var belt = incomingTags.beltb
          count += 1
          count += buzz
        } else if(patt) {
          var belt = incomingTags.beltp
          count += 2
          count += patt
        }
        count += reps
        count += freq
        //sconsole.log(count)
        console.log(belt)
        if (belt==1) {
          spawn('python', ['./HC05_1.py', count])
          console.log("HC05_1", count)  
        } else if (belt==2) {
          //spawnSync('python', ['./HC05_2.py', count])  
          //console.log("HC05_2", count)
        } else if (belt==3) {
          console.log("HC05_3", count)
          spawn('python', ['./HC05_3.py', count])  
        } else if (belt==4) {
          spawn('python', ['./HC05_4.py', count])  
          console.log("HC05_4", count)
        } else if (belt==5) {
          //spawnSync('python', ['./HC06_1.py', count])  
          //console.log("HC06_1", count)
        } else if (belt==6) {
          console.log("All boards", count)
          spawn('python', ['./HC05_1.py', count])  
          //spawn('python', ['./HC05_2.py', count])  
          spawn('python', ['./HC05_3.py', count])  
          spawn('python', ['./HC05_4.py', count])  
          //spawn('python', ['./HC06_1.py', count])  
        }
        
      } else {
        console.log('I do not have a RegExp')
        console.log('\n----------------------')
      }
    }
  } catch (err) {
    //count = 0
    console.log('Could not decode OSC message')
  }
})

process.on('SIGINT', function () {
  udp.close(() => {
    console.log(' SIGINT exit | server closed')
    process.exit(0)
  })
})

process.on('SIGTERM', function () {
  udp.close(() => {
    console.log(' SIGTERM exit | server closed - check for bound port netstat -nlp | grep :' + PORT)
    process.kill(process.pid, 'SIGINT')
    process.exit(1)
  })
})

udp.on('error', function (err) {
  process.kill(process.pid, 'SIGINT')
  console.log('throw err ... so something wrong..')
  //throw err
})

udp.on('listening', function () {
  console.log('Listening for OSC messages on: ' + HOST + ':' + PORT)
})

udp.bind({
  port: PORT, exclusive: true
})

// function send() {
//   if(! remoteAddress)
//     return
//   var y = osc.toBuffer({
//     oscType: 'message',
//     address: '/print/y',
//     args: [{
//       type: 'string',
//       value: 'testing...'
//     }]
//   })

//   udp.send(y, 0, y.length, remotePort, remoteAddress)
//   console.log('Sent OSC message to %s:%d', remoteAddress, remotePort)
// }

// send message every second
// setInterval(send, 1000);


// ----------------------------
// ----------------------------
// ----------------------------

// var count = 2
//       //count = 7
//       spawnSync('python', ['./HC051.py', count])
//       count++
//       spawnSync('python', ['./HC06.py', incoming])
//       count++
//       spawnSync('python', ['./HC052.py', count])
//       count++
//       if (count > 8) {
//         count = 2
//       }
//          // else {
//    //   count = 0
//    //   spawnSync('python', [ './HC05.py', count])
//    //   spawnSync('python', [ './HC06.py', count])
//    //   spawnSync('python', ['./HC052.py', count])
//    // }
//    //  }
// // });



// var testReg1 = new RegExp("test")
// var testReg2 = /test/
// var testReg3 = /\w\w\w\w/
// // var str = "test"

// var regEx000 = new RegExp("/belt_([1-5]){1}/buzzer_([1-5]){1}/((intensity)|(frequency))")
// var regEx111 = new RegExp("/belt_([1-5]){1}/pattern_([1-2]){1}/((direction)|(intensity))")
// var regEx010 = new RegExp("("+regEx000+ ")|(" +regEx111+")") //.source

// var regEx00 = /(\/belt_([1-5])\d{1}\/buzzer_([1-5])\d{1}\/((frequency ([0-255])\d{1,3})|(intensity ([0-3])\d{1})))|(\/belt_([1-5])\d{1}\/pattern_([1-2])\d{1}\/((intensity ([0-3])\d{1})|(direction ([1-2])\d{1})))\//
// var regEx01 = new RegExp("/belt_[1-5]/buzzer_[1-5]/intensity_[0-3]")
// var regEx02 = new RegExp("/belt_[1-5]/pattern_[1-2]/(intensity_[0-3]|direction[1-2])")
// var regEx03 = new RegExp("/belt_[1-5]/pattern_[1-2]/direction_[1-2]")
// var regEx04 = new RegExp("/belt_[1-5]/pattern_[1-2]/frequency_[0-255]")

// var regEx1 = new RegExp("/belt_([1-5]){1}") //"/belt\w\d" /\/belt\w\d\//
// var regEx2 = new RegExp("/buzzer_([1-5]){1}")
// var regEx3 = new RegExp("/pattern_([1-2]){1}")  // pulse, wave
// var regEx4 = new RegExp("/frequency_([0-255])") // set range
// var regEx5 = new RegExp("/intensity_([0-3])") // off, low, med, high
// var regEx6 = new RegExp("/direction_([1-2])") // CW, CCW

// var combo = new RegExp("("+regEx1+")"+"(("+regEx2+")|("+regEx3+"))")
// var start = 

// var grabShort alert(incoming.match(/\b\d{1}\b/))
// var grabLong alert(incoming.match(/\b\d{1-3}\b/))