import board
import digitalio

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT

while (True):
    if not button.value:
        print("Low")
    else:
        print("High")
