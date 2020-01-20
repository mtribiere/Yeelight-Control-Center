# !/usr/bin/python3

import socket
import sys

class Bulb:

	def __init__(self,ip,port):
		self.ipAddress = (ip,port);
		self.bulb = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	def connect(self):
		self.bulb.connect(self.ipAddress)
	
	def disconnect(self):
		self.bulb.close()

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
		
		#Create the command
		toSend = self.createCommand(id,method,params)
		toSend = str.encode(toSend)

		#Send the command
		self.bulb.sendall(toSend)

		#Listen the response
		maxSize = 50000;
		chunks = []
		bytes_recd = 0
		needStop = 0
		while not(needStop):
			chunk = self.bulb.recv(2048)
			if chunk == b'':
				raise RuntimeError("Connection Error")
			if b'\n' in chunk:
				needStop = 1
			chunks.append(chunk)
			bytes_recd = bytes_recd+len(chunk)
		
		print(str(chunks))

	def turnOff(self):
		self.sendCommandToBulb("1","set_power",["off","smooth",500])


	def turnOn(self):
		self.sendCommandToBulb("1","set_power",["on","smooth",500])

	def adjustBrightness(self,brightness):
		self.sendCommandToBulb("1","set_bright",[int(brightness),"smooth",500])
