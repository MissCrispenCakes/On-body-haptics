*******************
*******************
 
@misscrispencakes GITHUB for:
code, documentation, questions, alternative customisatons (bluetooth, custom PCB files etc.)
>> further [requests,comments,questions] accepted indefinitely from DisPerSion Lab

*******************
*******************

general info:

user name is pi
password is raspberry

(this is the default)
update these as required

*******************

when/if DRV code is updated remember that:
- bit masks or bit specific hardware code is required
- binary/hex format is required
- The OR [ | ] operator forces a 1 in a column where a 1 exists in either the first argument or the second argument.
- The AND [ & ] operator forces a 0 in a column where a 0 exists in either the first argument or the second argument. 
- many examples are provided in the customised adafruit_drv2605_LOG.py file (standard drv file also included)

IT IS ADVISABLE TO NOT PROGRAM THE CONTROL4 REGISTER AND OTP MEMORY: this is a permanent action and will force the
drv to be 'set' to the current LRAs attached.. effectively preventing future customisation

*******************

ANYTIME a new wifi connection is encountered:

connect a screen and keyboard to PI - will need an HMDI to mini-HDMI and USB to micro-USB or comparable 
wait for system to initialize then type the following at prompt:

nano /etc/wpa_supplicant/wpa_supplicant.conf 

then enter the network id and password as indicated by the sample format in the wpa_supplicant.conf file

save, exit and reboot the pi using:
sudo reboot

*******************

once wifi is setup there is a custom button on the PI 
that will show the PIs IP and MAC address on the OLED display

*******************

OSC format:
/belt_#/buzz_# [#, #]

where pattern and duration arguments are contained within [#, #]

it is possible to extend these commands by working with the server code
that runs on the PIs

*******************

files of interest:
octopulse-client.py	- this is a sample code to test sending to haptic belts
octopulse-server.py	- this is running on the PIs (auto starts after wifi is configured)
				- you can run a testing version of this if you change port access in the code and rerun
				- both are located: ~/On-body-haptics/haptics_v2_I2C/code/
adafruit_drv2605.py &| adafruit_drv2605_LOG.py 	- default and customised versions of the DRV code used to control characteristics
						- located: ~/.local/lib/python3.7/site-packages/
octopulse-server.service & ip-display.service  	- these files are run during PI startup and activate the auto-run

other files in /code/ are either simple default versions of above code samples, testing versions or basic setup


*******************
*******************
*******************

MOTORS

*******************
*******************
*******************

currently there are LRAs attached to all motor board PCBs - these can be easily desoldered and swapped for alternative LRAs or ERMs 

if swapping between ERM and LRA adjust DRV code accordingly
