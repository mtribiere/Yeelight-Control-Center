# !/usr/bin/python3

import socket
import json
import sys

class Bulb:

	def __init__(self,ip,port,transitionType):
		#Get the parameters
		self.ipAddress = (ip,port);
		self.transitionType = transitionType
		
		#Configure the client
		self.bulb = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.bulb.settimeout(2)

		#Setup variable
		self.isConnected = 0

	def connect(self):
		toReturn = 0
		
		try:
			self.bulb.connect(self.ipAddress)
			self.isConnected = 1
		except:
			print("Connection Error")
			toReturn = 1
			self.isConnected = 0

		return toReturn

	def disconnect(self):
		self.bulb.close()
		self.isConnected = 0

	def createCommand(self,id,method,params):

		#Concatenate id and method
		toReturn = "{\"id\":"+id+",\"method\":\""+method+"\",\"params\":["

		#Add the params
		for param in params:
			# If this is an str
			if(isinstance(param,str)):
				
				toReturn += "\""
				toReturn += param
				toReturn += "\""

			else: #if this is an int
				toReturn += str(param)
			
			toReturn += ","

		#Finish the command
		toReturn = toReturn[:-1]
		toReturn += "]}\r\n"

		return toReturn

	def sendCommandToBulb(self,id,method,params):

		#Check the bulb is connected
		if(self.isConnected == 0):
			return "fail"
		
		#Create the command
		toSend = self.createCommand(id,method,params)
		toSend = str.encode(toSend)

		#Send the command
		self.bulb.sendall(toSend)

		#Listen the response
		maxSize = 50000;
		chunks = ""
		bytes_recd = 0
		needStop = 0
		chunk = b''
		while not(needStop):
			
			chunk = self.bulb.recv(1)
			chunks += (str(chunk,'utf-8'))
			bytes_recd = bytes_recd+len(chunk)

			if (chunk == b''):
				raise RuntimeError("Connection Error")
			
			if ('\n' in chunks):

				#Ignore notification messages
				if not("props" in chunks):
					needStop = 1
				else:
					chunk = b''
					chunks = ""
					bytes_recd = 0	
		

		# Return the command result
		#print(chunks)
		result = json.loads(chunks)["result"]
		return result

	def getCurrentState(self):
		result = self.sendCommandToBulb("1","get_prop",["power","bright","rgb","ct"])
		return result

	def turnOff(self):
		toReturn = 1
		if(self.sendCommandToBulb("1","set_power",["off",self.transitionType,500])[0] == "ok"):
			toReturn = 0
		
		return toReturn

	def turnOn(self):
		toReturn = 1
		if(self.sendCommandToBulb("1","set_power",["on",self.transitionType,500])[0] == "ok"):
			toReturn = 0

		return toReturn

	def adjustBrightness(self,brightness):
		self.sendCommandToBulb("1","set_bright",[int(brightness),self.transitionType,500])
	
	def adjustTemperature(self,temperature):
		self.sendCommandToBulb("1","set_ct_abx",[int(temperature),self.transitionType,500])
	
	def setColor(self,r,g,b):
		colorToSend = (65536*r) + (256*g) + b
		print(colorToSend)
		self.sendCommandToBulb("1","set_rgb",[colorToSend,self.transitionType,500])

	def getCurrentIp(self):
		return self.ipAddress[0]
	
	def getCurrentTransitionType(self):
		return self.transitionType;
