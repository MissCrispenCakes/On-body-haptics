from pythonosc.udp_client import SimpleUDPClient
import time
import sys
#from signal import signal, SIGINT #could include kill signal handling
from sys import exit

######
# THIS IS SAMPLE CODE TO TEST THE HAPTIC SYSTEM
# CLIENT IS SET UP TO SEND OSC ACTIVATION VIA COMMAND LINE ARGUMENT INPUT
# USE: "python3 octopulse-client.py 0 1 2 3"
# where the cmd line arguments indicate the LRA/buzzers
# i.e., 0 1 2 3 4 5 4 4 4 4 4 3 7 5 6 0 ... etc 
# edit the IP, PORT, and pattern variables below
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
# BELT: 	belt_0	|		belt_1	|		 belt_2	 |	 belt_3		|		belt_4	
# IP  :	10.0.0.30 | 10.0.0.55 | 10.0.0.101 | 10.0.0.110 | 10.0.0.140
#
#####

ip = "10.0.0.140" #change to my new IP
port = 9994 #change to my new PORT
client = SimpleUDPClient(ip, port)  # Create client

args = []
pattern = 12
duration = 1 #0.5 # 0.1, 0.5, 1, 1.5
#modifier = 0 # can include additional variables if desired - update server code accordingly to handle

belt = 4 #belt number used here to identify associated RaspPi
#buzz = 0

print(sys.argv[1:]) #toggle my comments
print(len(sys.argv)) #toggle my comments
arg = sys.argv[1]
for i in range(1,len(sys.argv)):
	#print(arg) #toggle my comments
	print(sys.argv[i])
	args.append(sys.argv[i])

print(args)

for i in range(len(args)):
		#print(i) #toggle my comments
		print("Buzzing on #{0}".format(args[i]))
		client.send_message("/belt_4/buzz_{0}".format(args[i]), [duration, pattern])
		#client.send_message("/belt_{0}/buzz_{0}".format(belt, buzz, [duration, pattern, modifier])
		print("/belt_4/buzz_{0}".format(args[i]), [duration, pattern])
		time.sleep(2) # adjust me or 'duration' variable here and/or adjust server 
										# variable 'pause' on RaspPI depending on signal response and 
										# desired timing effects
		# time.sleep(0) can mimic driving multiple LRAs simultaneously
print("done") #toggle my comments
