import bluetooth
import sys
#import time

#bd_addr = "XX:XX:XX:XX:XX:XX" # HC06 bound to rfcomm1
bd_addr = "98:D3:31:XX:XX:XX" # HC05 bound to rfcomm2

#f= open("05test","w+")
#f.write("This is line")
#f.close()

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect(( bd_addr, port ))

data = sys.argv[1]

sock.send(data)
#sock.send('12345678'.encode())
#print ('Bzzz Bzz 05'))
#time.sleep(.3)
sock.close()
