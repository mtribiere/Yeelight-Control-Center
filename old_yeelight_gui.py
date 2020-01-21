# !/usr/bin/python3

import tkinter as tk
import tkinter.colorchooser as tkcd
from yeelight_lib import Bulb

class Application(tk.Frame):

	def __init__(self,master=None):
		super().__init__(master)
		
		#Setup bulb
		self.bulb = Bulb("192.168.43.53",55443)
		print("Connecting to bulb....",end='')
		#self.bulb.connect()
		print("OK !")

		#Setup GUI
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		
		#Left panel
		self.leftPanel = tk.PanedWindow(self)
		self.leftPanel.pack(fill="y",expand=1)

		#Turn on button
		self.ButtonOn = tk.Button(self.leftPanel)
		self.ButtonOn["text"] = "Turn On"
		self.ButtonOn["command"] = self.bulb.turnOn
		self.leftPanel.add(self.ButtonOn)

		#Turn off button
		self.ButtonOff = tk.Button(self.leftPanel)
		self.ButtonOff["text"] = "Turn Off"
		self.ButtonOff["command"] = self.bulb.turnOff
		self.leftPanel.add(self.ButtonOff)

		#Choose color button
		self.ChooseColorButton = tk.Button(self.leftPanel)
		self.ChooseColorButton["text"] = "Choose color"
		self.ChooseColorButton["command"] = self.chooseColor
		self.leftPanel.add(self.ChooseColorButton)

		self.rightPanel = tk.PanedWindow(self.leftPanel,orient="vertical")
		self.leftPanel.add(self.rightPanel)

		#Brightness slider
		self.BrightnessSlider = tk.Scale(self.leftPanel)
		self.BrightnessSlider["from_"] = 100
		self.BrightnessSlider["to"] = 0
		self.BrightnessSlider["orient"] = "vertical"
		self.BrightnessSlider.bind("<ButtonRelease-1>",self.adjustBrightness)
		self.rightPanel.add(self.BrightnessSlider)

		#Current State label
		self.CurrentStateLabel = tk.Label(self)
		self.CurrentStateLabel["text"] = "Current State : On"
		self.CurrentStateLabel.pack(side="left",padx=20)

	def adjustBrightness(self,event):
		self.bulb.adjustBrightness(self.BrightnessSlider.get())
	
	def chooseColor(self):
		color = tkcd.askcolor(title="Choose color")
		print("Selected : "+str(color))

	def disconnect(self):
		print("Disconnecting from bulb....")
		self.bulb.disconnect()
		

root = tk.Tk()
root.title("Yeelight Control Center")  
app = Application(master=root) 
app.mainloop()
app.disconnect()
print("Application Terminated")