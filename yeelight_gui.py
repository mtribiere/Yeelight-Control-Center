# !/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from yeelight_lib import Bulb

class Application(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self,title="Yeelight Control Center")

		#Setup bulb
		self.bulb = Bulb("192.168.43.53",55443)
		print("Connecting to bulb....",end='')
		#self.bulb.connect()
		print("OK !")
		#self.bulb.getCurrentState()

		#Setup GUI
		self.set_icon_from_file("img/logo.ico")
		self.create_widgets()

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

		# Préparer la boite de dialogue
		self.dialog = Gtk.ColorChooserDialog(title="Choose a new color",parent=self)
		#self.dialog.set_property("show-editor",True)
		self.dialogResponse = self.dialog.run()
		newColor = self.dialog.get_rgba()

		# Traiter la réponse
		if(self.dialogResponse == Gtk.ResponseType.OK):
			print("New color : "+str(newColor))
			self.bulb.setColor(int(newColor.red*255),int(newColor.green*255),int(newColor.blue*255))
		else:
			print("Abord")

		#Détruire la boite de dialogue
		self.dialog.destroy()

	def disconnect(self):
		print("Disconnecting from bulb....")
		self.bulb.disconnect()
		Gtk.main_quit()
		print("Application Terminated")
		

window = Application()
window.connect("destroy",Application.disconnect)
window.show_all()
Gtk.main()
