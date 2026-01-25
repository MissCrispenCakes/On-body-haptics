import time
import board
import busio
import adafruit_drv2605
import adafruit_tca9548a
from signal import signal, SIGINT
from sys import exit

drv = []

def handler(signal_received, frame):
    for i in range(8):
        drv[i].stop()
    exit(0)

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
print("Initializing I2C Mux")
tca = adafruit_tca9548a.TCA9548A(i2c)

for i in range(8):
    print("Initializing driver {}".format(i))
    drv.append(adafruit_drv2605.DRV2605(tca[i]))
    drv[i].use_LRM()

signal(SIGINT, handler)

# Main loop runs forever trying each effect (1-123).
# See table 11.2 in the datasheet for a list of all the effect names and IDs.
#   http://www.ti.com/lit/ds/symlink/drv2605.pdf
effect_id = 118
while True:
    print('Playing effect #{0}'.format(effect_id))
    for i in range(8):
        print('Using channel #{0}'.format(i))
        drv[i].sequence[0] = adafruit_drv2605.Effect(effect_id)  # Set the effect on slot 0.
        drv[i].sequence[1] = adafruit_drv2605.Pause(1)  # Set the effect on slot 0.
        # You can assign effects to up to 7 different slots to combine
        # them in interesting ways. Index the sequence property with a
        # slot number 0 to 6.
        # Optionally, you can assign a pause to a slot. E.g.
        # drv.sequence[1] = adafruit_drv2605.Pause(0.5)  # Pause for half a second
        drv[i].play()       # play the effect
        time.sleep(1)  # for 0.5 seconds
        drv[i].stop()       # and then stop (if it's still running)
    # Increment effect ID and wrap back around to 1.
    #effect_id += 1
    #if effect_id > 123:
    #    effect_id = 1
