from pythonosc import dispatcher
from pythonosc import osc_server
import re

import time
import board
import busio
import adafruit_drv2605
import adafruit_tca9548a

import threading
import queue

class I2CThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super(I2CThread,self).__init__(group=group, target=target, 
            name=name)
        self._running = True
        self.args = args
        self.kwargs = kwargs
        self.queue = kwargs['queue']        
        
        print("I2CThread: initializing I2C")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        print('I2CThread: Initializing I2C mux')
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        
        self.drv = []
        
        for i in range(8):
            print('I2CThread: Initializing driver {}'.format(i))
            self.drv.append(adafruit_drv2605.DRV2605(self.tca[i]))
            self.drv[i].use_LRM()

        return
        
    def stop(self, *args, **kwargs):
        args[1].put({"start": 0, "belt": 1, "buzz": args[0], "pattern": 0, "duration": 0})
        return
    
    def run(self):
        while self._running:
            if not q.empty():
                item = q.get()
                print(item)
                i = item['buzz']
                if item['start'] == 1:
                    if (i < 8):
                        self.drv[i].sequence[0] = adafruit_drv2605.Effect(item['pattern'])
                        self.drv[i].sequence[1] = adafruit_drv2605.Pause(item['duration'])
                        self.drv[i].play()
                        time.sleep(0.2) #item['duration'])
                        t = threading.Timer(item['duration'], stop_buzzer, [i], {})
                        t.start()
                else:
                    if (i < 8):
                        self.drv[i].stop()
            
        return

def stop_buzzer(*args, **kwargs):
    global q
    q.put({"start": 0, "belt": 1, "buzz": args[0], "pattern": 0, "duration": 0})

def print_handler(address, *args):
    print("{}: {}".format(address, args))

def buzz_handler(address, *args):
    global q
    
    print("Buzzer handler")
    print("{}: {}".format(address, args))
    buzz_args = re.split('\/belt_(\d*)\/buzz_(\d*)(\/?)', address)
    belt = int(buzz_args[1])
    buzz = int(buzz_args[2])
    print("Belt: {}, buzz: {}".format(belt, buzz))
    print(len(args))
    if len(args) == 0:
        duration = 0.5
        pattern = 118
    elif len(args) == 1:
        duration = args[0]
        pattern = 118
    else:
        duration = args[0]
        pattern = args[1]
    
    if duration > 1.27:
        duration = 1.27

    q.put({"start": 1, "belt": belt, "buzz": buzz, "pattern": pattern, "duration":duration})

    print("Duration: {}, pattern: {}".format(duration, pattern))

q = queue.Queue(16)

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/belt_1/*", buzz_handler)
dispatcher.set_default_handler(print_handler)

print("Starting I2C thread")
i_thread = I2CThread(name="I2C", kwargs={'queue': q})
i_thread.start()

print('Waiting')
server = osc_server.ThreadingOSCUDPServer(
    ('192.168.2.221', 9998), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
