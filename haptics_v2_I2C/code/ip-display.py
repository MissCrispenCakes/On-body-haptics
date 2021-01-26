import board
import digitalio
import busio
import netifaces
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

i2c = busio.I2C(board.SCL, board.SDA)
button = digitalio.DigitalInOut(board.D26)
button.direction = digitalio.Direction.INPUT
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)

while (True):
	if not button.value:
		# write IP info to display
		display.fill(0)

		for ifacename in netifaces.interfaces():
			if not ifacename.startswith('wl'):
				continue

			addrs = netifaces.ifaddresses(ifacename)
			wl_ip = ''
			wl_mac = ''

			if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
				ips = [addr['addr'] for addr in addrs[netifaces.AF_INET]]

				for ip in ips:
					if ip.startswith('127.'):
						break
					else:
						wl_ip = ip
						wl_mac = addrs[netifaces.AF_LINK][0]['addr']

		image = Image.new("1", (display.width, display.height))
		draw = ImageDraw.Draw(image)
		draw.text((0, 0), "OctoPulse", font=font, fill=255)
		draw.text((0, 11), "IP: {}".format(wl_ip), font=font, fill=255)
		draw.text((0, 22), "MAC: {}".format(wl_mac), font=font2, fill=255)

		display.image(image)
		display.show()

		time.sleep(10)

		display.fill(0)
		display.show()
