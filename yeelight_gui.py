# !/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from yeelight_lib import Bulb
from setting_dialog import SettingDialog
import JSONutils as configFile

class Application(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self,title="Yeelight Control Center")

		#Setup bulb
		config = configFile.loadConfig()
		self.createBulb(config["ipAddress"],config["transitionType"])

		#Setup GUI
		self.set_icon_from_file("img/logo.ico")
		self.create_widgets()

		#Connect to bulb
		self.connectToBulb()


	def create_widgets(self):

		########################### Main Box
		self.mainBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_VERTICAL,spacing=2)
		self.add(self.mainBox)
		
		################ Top Box
		self.topBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing=2)
		self.mainBox.add(self.topBox)

		#Turn on button
		self.ButtonOn = Gtk.Button(label="Turn On")
		self.imageOn = Gtk.Image()
		self.imageOn.set_from_file("img/Light_on.png")
		self.ButtonOn.set_property("image",self.imageOn)
		self.ButtonOn.set_property("always-show-image",True)
		self.ButtonOn.connect("clicked",self.turnOnLight)
		
		self.topBox.pack_start(self.ButtonOn,True,True,0)

		#Turn off button
		self.ButtonOff = Gtk.Button(label="Turn Off")
		self.imageOff = Gtk.Image()
		self.imageOff.set_from_file("img/Light_off.png")
		self.ButtonOff.set_property("image",self.imageOff)
		self.ButtonOff.set_property("always-show-image",True)
		self.ButtonOff.connect("clicked",self.turnOffLight)

		self.topBox.pack_start(self.ButtonOff,True,True,0)

		#Choose color button
		self.ChooseColorButton = Gtk.Button(label="Change Color")
		self.ChooseColorButton.connect("clicked",self.chooseColor)

		self.topBox.pack_start(self.ChooseColorButton,True,True,0)

		################## Mid Box
		self.midBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing=2)
		self.mainBox.add(self.midBox)

		#Brightness slider
		self.brightnessAdjustement = Gtk.Adjustment(value=50,lower=0,upper=100,step_increment=5,page_increment=10,page_size=0)
		self.BrightnessSlider = Gtk.Scale(orientation=Gtk.STYLE_CLASS_HORIZONTAL,adjustment=self.brightnessAdjustement)
		self.BrightnessSlider.set_property("value-pos",1)
		self.BrightnessSlider.set_digits(0)
		self.BrightnessSlider.connect("value-changed",self.adjustBrightness)

		self.midBox.pack_start(self.BrightnessSlider,True,True,0)

		#Theme button
		self.ButtonTheme = Gtk.Button(label="Themes")
		self.midBox.pack_start(self.ButtonTheme,False,True,0)

		################# Bottom Box
		self.botBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing=2)
		self.mainBox.add(self.botBox)

		#Temperature slider
		self.temperatureAdjustement = Gtk.Adjustment(value=4000,lower=1700,upper=6500,step_increment=5,page_increment=10,page_size=0)
		self.TemperatureSlider = Gtk.Scale(orientation=Gtk.STYLE_CLASS_HORIZONTAL,adjustment=self.temperatureAdjustement)
		self.TemperatureSlider.set_property("value-pos",1)
		self.TemperatureSlider.set_digits(0)
		self.TemperatureSlider.connect("value-changed",self.adjustTemperature)

		self.botBox.pack_start(self.TemperatureSlider,True,True,0)

		#Setting button
		self.ButtonSetting = Gtk.Button()
		self.imageSetting = Gtk.Image()
		self.imageSetting.set_from_file("img/setting.png")
		self.ButtonSetting.set_property("image",self.imageSetting)
		self.ButtonSetting.set_property("always-show-image",True)
		self.ButtonSetting.connect("clicked",self.openSettings)

		self.botBox.pack_start(self.ButtonSetting,False,True,0)

	def turnOnLight(self,widget):
		if(self.bulb.turnOn() != 0):
			print("Connection Error") 

	def turnOffLight(self,widget):
		if(self.bulb.turnOff() != 0):
			print("Connection Error")

	def adjustBrightness(self,event):
		self.bulb.adjustBrightness(self.BrightnessSlider.get_value())

	def adjustTemperature(self,event):
		self.bulb.adjustTemperature(self.TemperatureSlider.get_value())
	
	def chooseColor(self,widget):

		#Prepare dialogBox
		self.dialog = Gtk.ColorChooserDialog(title="Choose a new color",parent=self)
		self.dialogResponse = self.dialog.run()
		newColor = self.dialog.get_rgba()

		#Handle response
		if(self.dialogResponse == Gtk.ResponseType.OK):
			print("New color : "+str(newColor))
			self.bulb.setColor(int(newColor.red*255),int(newColor.green*255),int(newColor.blue*255))
		else:
			print("Abord")

		#Close the dialog
		self.dialog.destroy()

	def openSettings(self,widget):
		
		#Prepare dialogBox
		settingDialog = SettingDialog(self,self.bulb.getCurrentIp(),self.bulb.getCurrentTransitionType())
		settingDialogResponse = settingDialog.run()
		
		#Handle the response
		if(settingDialogResponse == Gtk.ResponseType.OK):
			print("Interrupting communactions")
			#Get the new transition
			if(settingDialog.getTransitionType() == 0):
				newTransitionType = "sudden"
			else:
				newTransitionType = "smooth"

			#Write the config
			configFile.saveConfig(settingDialog.getIp(),newTransitionType)

			#Create new Bulb
			self.bulb.disconnect()
			self.createBulb(settingDialog.getIp(),newTransitionType)

			#Connect to bulb
			self.connectToBulb()

		else:
			print("Canceled")

		#Destroy the dialog
		settingDialog.destroy()
	
	def createBulb(self,ipAdress,transitionType):
		self.bulb = Bulb(ipAdress,55443,transitionType)
	
	def connectToBulb(self):

		print("Connecting to bulb....",end='')
		#If an error occured
		if(self.bulb.connect() == 1):
			#Create the dialog
			errorDialog = Gtk.MessageDialog(parent=self,
											flags=0,
											message_type=Gtk.MessageType.ERROR,
											buttons=Gtk.ButtonsType.OK)
			errorDialog.set_property("text","Connection error")
			errorDialog.format_secondary_text("A connection error occured when trying to connect to the bulb.\nPlease double-check its IP address and make sure the device is online.")
			errorDialog.run()

			#Destroy the dialog
			errorDialog.destroy()
		else:
			self.updateCursors()
			print("OK !")
	
	def updateCursors(self):
		currentState = self.bulb.getCurrentState()
		self.BrightnessSlider.set_value(int(currentState[1]))
		self.TemperatureSlider.set_value(int(currentState[3]))

	def disconnect(self):
		print("Disconnecting from bulb....")
		self.bulb.disconnect()
		Gtk.main_quit()
		print("Application Terminated")
		

window = Application()
window.connect("destroy",Application.disconnect)
window.show_all()
Gtk.main()
