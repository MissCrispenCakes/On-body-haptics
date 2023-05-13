from pythonosc.udp_client import SimpleUDPClient
import time
import sys
from signal import signal, SIGINT
from sys import exit

ip = "192.168.2.221"
port = 9998

client = SimpleUDPClient(ip, port)  # Create client

args = []

print(sys.argv[1:])
print(len(sys.argv))
arg = sys.argv[1]
for i in range(1,len(sys.argv)):
	#print(arg)
	#args. = sys.argv[i]
	print(sys.argv[i])
	args.append(sys.argv[i])

print(args)

for i in range(len(args)):
		print(i)
		print("Buzzing on #{0}".format(args[i]))
		client.send_message("/belt_1/buzz_{0}".format(args[i]), [0.5, 95])
		time.sleep(0.2)

def handler(signal_received, frame):
    for i in range(8):
        client.send_message("/belt_1/buzz_{0}".format(i), [0, 0])
    exit(0)

signal(SIGINT, handler)

#client.send_message("/belt_1/buzz_0", [1, 14])
#lient.send_message("/belt_1/buzz_1", [1, 14])
# time.sleep(5)
# client.send_message("/belt_1/buzz_2", [1, 12])
# time.sleep(5)
# client.send_message("/belt_1/buzz_3", [1, 12])
# time.sleep(5)
# client.send_message("/belt_1/buzz_4", [1, 12])
# time.sleep(5)
# client.send_message("/belt_1/buzz_5", [1, 12])
# time.sleep(5)
# client.send_message("/belt_1/buzz_6", [1, 12])
# time.sleep(5)
# client.send_message("/belt_1/buzz_7", [1, 12])
# #//client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string
print("round done")