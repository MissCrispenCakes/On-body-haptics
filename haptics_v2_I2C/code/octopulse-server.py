from pythonosc import dispatcher #threading queue
from pythonosc import osc_server
import re

import time
import board #hardware access
import busio #hardware access
import adafruit_drv2605 # this library is a circuit-python dev to directly access hardware of DRV
                        # you can edit this file but make sure you know what you are doing!!!!! 
                        # commands in server code here that access this hardware set are indicated 
                        # with the tag: adafruit-DRV
import adafruit_tca9548a    # this library handles the real-time I2C whereTCA9548A is an I2C Multiplexer 
                            # that allows multiple (1-8) address to access the same SDA/SCL pins
                            # SDA: SERIAL DATA LINE
                            # SCL: SERIAL CLOCK LINE

import threading
import queue

######
# THIS IS SAMPLE CODE TO TEST THE HAPTIC SYSTEM
# SERVER IS SET UP AUTOMATICALLY ON START UP
# but you can start a second session to test/see comments printed to screen
# NAVIGATE TO: /home/pi/On-body-haptics/haptics_v2_I2C/code/ 
# USE: "python3 octopulse-server.py"
# usually requires selecting new PORT (in both client and server code) 
# as auto-start will occupy default port in code
#
# in general, edit the IP, PORT, and pattern variables below
#
######
#
#####
#
# sample patterns from DRV2605 motor driver library are provided 
# alternatively you can access motor driver bits individually 
# but this requires hardware programming and is left up to the 
# experienced user instead of included here
#
#####
#
# pattern [47-51] buzz [100%-20%]
# pattern [118] long buzz for programmatic stopping
# pattern [15-16] 750ms-1000ms Alert buzz
# pattern [10] double click
# pattern [12] triple click
#
#####
# 
# Store IP-Belt combos for easy reference:
#
# BELT:   belt_0  |   belt_1       belt_2  |   belt_3   |   belt_4  
# IP  : 10.0.0.30 | 10.0.0.55 | 10.0.0.101 | 10.0.0.110 | 10.0.0.140
#
#####
#####
# buzzer number and location around belt
# RaspberryPi sits between buzzer 0 and 7
#####
#
# example layout with raspberryPi front and centre / stomach area 
#      front  [L]eft[F]ront || [R]ight[F]ront 
#       [PI]
#      LF  RF 
#       0  7
#  LMF 1    6  RMF  [L|R][M]iddle[F]ront
#  LMR 2    5  RMR  [L|R][M]iddle[R]ear
#       3  4
#      LR  RR  [L]eft[R]ear || [R]ight[R]ear
#       rear
#
#####
#
# OSC namespace 
# /belt_{#}/buzz_{#} [#, #] ;where [#, #] is [duration, pattern] 
# /belt_0/buzz_0 [0.5, 118]
#
#####


class I2CThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
        args=(), kwargs=None):
        super(I2CThread,self).__init__(group=group, target=target,
            name=name)

        self._running = True

        self.args = args
        self.kwargs = kwargs
        self.queue = kwargs['queue']        
        print("I2CThread: initializing I2C") # communicating to DRV2605

        self.i2c = busio.I2C(board.SCL, board.SDA) # access to hardware
        print('I2CThread: Initializing I2C mux') # enabling multiple motor control
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)

        self.drv = [] # drive multiple motors and link Queue protocol to DRV
        for i in range(8):
            print('I2CThread: Initializing driver {}'.format(i))
            self.drv.append(adafruit_drv2605.DRV2605(self.tca[i]))
            #self.drv[i].use_LRM() #adafruit-DRV
            print('DRV2605: Auto-Calibrating driver {}'.format(i))
            #self.drv[i].mode = 7 #MODE_AUTOCAL
            self.drv[i].autocal()
            print('DRV2605: Auto-Calibrating driver {}'.format(i))
            self.drv[i].autocal()
            print('DRV2605: driver {} ready for use'.format(i))
            #self.drv[i].mode = 1 #MODE_INTTRIG
            #self.drv[i].library = 6 #LIBRARY_LRA
        
        return
        
    def stop(self, *args, **kwargs):
        # belt number used to identify associated RaspPi
        args[2].put({"start": 0, "belt": 4, "buzz": args[0], "pattern": 0, "duration": 0})
        # args[2].put({"start": 0, "belt": args[0], "buzz": args[1], "pattern": 0, "duration": 0})
        return
    
    def run(self):
        while self._running:
            if not q.empty():
                item = q.get()
                print(item)
                #l = item['belt']
                b = item['buzz']
                if item['start'] == 1:
                    if (b < 8):
                        self.drv[b].sequence[0] = adafruit_drv2605.Effect(item['pattern']) #adafruit-DRV
                        #self.drv[b].sequence[1] = adafruit_drv2605.Effect(47) #adafruit-DRV
                        #self.drv[b].sequence[2] = adafruit_drv2605.Effect(48) #adafruit-DRV
                        #self.drv[b].sequence[3] = adafruit_drv2605.Effect(49) #adafruit-DRV
                        #self.drv[b].sequence[4] = adafruit_drv2605.Effect(50) #adafruit-DRV
                        #self.drv[b].sequence[5] = adafruit_drv2605.Effect(51) #adafruit-DRV
                        self.drv[b].sequence[6] = adafruit_drv2605.Pause(item['duration']) #adafruit-DRV
                        self.drv[b].play() #adafruit-DRV
                        # time.sleep(0.2) # item['duration']) # variable to adjust timing if required
                        t = threading.Timer(6*item['duration'], stop_buzzer, [b], {})
                        #t = threading.Timer(item['duration'], stop_buzzer, [l], [b], {})
                        t.start()
                else:
                    if (b < 8):
                        self.drv[b].stop()  #adafruit-DRV
        return

def stop_buzzer(*args, **kwargs):
    global q
    q.put({"start": 0, "belt": 4, "buzz": args[0], "pattern": 0, "duration": 0})
    #q.put({"start": 0, "belt": args[0], "buzz": args[1], "pattern": 0, "duration": 0})

def print_handler(address, *args):
    print("{}: {}".format(address, args))

def buzz_handler(address, *args):
    global q

    # print("Buzzer handler") # toggle my comment
    # print("{}: {}".format(address, args)) # toggle my comment
    buzz_args = re.split('\/belt_(\d*)\/buzz_(\d*)(\/?)', address)
    belt = int(buzz_args[1])
    buzz = int(buzz_args[2])
    print("Belt: {}, buzz: {}".format(belt, buzz))

    # print(len(args))
    if len(args) == 0:
        duration = 0.5
        pattern = 118
    elif len(args) == 1:
        duration = args[0]
        pattern = 118
    else:
        if (args[0] == 0 and args[1] == 0):
            stop_buzzer(buzz)
            #stop_buzzer(belt, buzz)
        else:
            duration = args[0]
            pattern = args[1]
    
    if duration > 1.27:
        duration = 1.27

    q.put({"start": 1, "belt": belt, "buzz": buzz, "pattern": pattern, "duration": duration})

    # print("Duration: {}, pattern: {}".format(duration, pattern)) #toggle my comment

q = queue.Queue(16)

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/belt_4/*", buzz_handler) # belt_0/* number used here only as identifier for associated RaspPi
dispatcher.set_default_handler(print_handler)

print("Starting I2C thread")
i_thread = I2CThread(name="I2C", kwargs={'queue': q})
i_thread.start()

print('Waiting')
server = osc_server.ThreadingOSCUDPServer(
    ('10.0.0.140', 9994), dispatcher) # change to my new IP, edit port location if required
print("Serving on {}".format(server.server_address))
server.serve_forever()