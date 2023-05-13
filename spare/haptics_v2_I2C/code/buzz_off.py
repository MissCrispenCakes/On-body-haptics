import time
import board
import busio
import adafruit_drv2605
import adafruit_tca9548a

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
print("Initializing I2C Mux")
tca = adafruit_tca9548a.TCA9548A(i2c)

drv = []

for i in range(8):
    print("Initializing driver {}".format(i))
    drv.append(adafruit_drv2605.DRV2605(tca[i]))
    drv[i].use_LRM()

# Main loop runs forever trying each effect (1-123).
# See table 11.2 in the datasheet for a list of all the effect names and IDs.
#   http://www.ti.com/lit/ds/symlink/drv2605.pdf
for i in range(8):
    print('Using channel #{0}'.format(i))
    drv[i].stop()       # and then stop (if it's still running)
