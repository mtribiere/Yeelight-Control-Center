# !/usr/bin/python3

from yeelight_lib import Bulb

#Print banner
print("===Yeelight console starting===")

#Define IP
bulb = Bulb("192.168.43.53",55443)

#Connect to Bulb
print("Connection to bulb...",end='')
bulb.connect()
print("OK !")

#Main loop
keepLoop = 1
while(keepLoop):
	#Print Menu
	print("Yeelight commands :")
	print("0: Get Infos")
	print("1: Turn Off")
	print("2: Turn On")

	print("\n98: Discover bulbs")
	print("99 : Quit")

	cmd = int(input("> "))

	#Craft the message
	if(cmd == 0):
		print("Requesting infos...")

	if(cmd == 1):
		print("Turning Off")
		bulb.turnOff()

	if(cmd == 2):
		print("Turning On")
		bulb.turnOn()

	if(cmd == 98):
		print("Starting bulb discovery...")

	if(cmd == 99):
		print("Quitting console...")
		keepLoop = 0

	#Padding
	print("\n\n")


#Disconnect from the bulb
print("Disconnecting from bulb...")
bulb.disconnect();