import board
import digitalio
import busio
import threading
import netifaces
import adafruit_ssd1306
import queue

class I2CThread(threading.Thread):
	IP_STATE_IDLE = 0
	IP_STATE_SHOW = 1

	def __init__(self, group=None, target=None, name=None, queue=None, verbose=None):
		super(I2CThread,self).__init__(group=group, target=target, name=name)
		self.setDaemon(True)
		button = digitalio.DigitalInOut(board.D26)
		button.direction = digitalio.Direction.INPUT
		self.ipState = self.IP_STATE_IDLE
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
		self._running = True
		self.clearEvent = threading.event()
		self.queue = queue
		return

	def showIP(self):
		#write IP info to the display
		self.display.fill(0)
		self.display.text("OctoPulse", 0, 2)
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
						wl_mac = addrs[netifaces.AF_LINK].addr[0]['addr']

		print("Found IP {} and MAC {}".format(wl_ip, wl_mac))
		self.display.text("IP: {}".format(wl_ip), 0, 12)
		self.display.text("MAC: {}".format(wl_mac), 0, 22)
		return

	def clearDisplay(self):
		#clear the display
		self.display.fill(0)
		self.display.show()
		return

	def setClear(self):
		self.clearEvent.set()
		return

	def run(self):
		while self._running:
			if (self.ipState == self.IP_STATE_IDLE):
				# check for GPIO4 == 0
				if not button.value:
					# button is pushed, show IP for 10 seconds
					self.ipState = self.IP_STATE_SHOW
					self.showIP()
					t = threading.Timer(10.0, self.setClear)
					t.start()
			if (self.clearEvent.is_set()):
				self.clearDisplay()
				self.clearEvent.clear()
				self.ipState = IP_STATE_IDLE
			if not self.queue.empty():
				buzzEvent = self.queue.get()
				print(buzzEvent)

buzzQueue = queue.Queue(10)

myI2CThread = I2CThread(buzzQueue)

myI2CThread.start()

myI2CThread.join()

print("Terminating...")
