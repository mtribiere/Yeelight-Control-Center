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
		self.bulb.connect()
		print("OK !")

		#Setup GUI
		self.create_widgets()

	def create_widgets(self):

		#Main Box
		self.mainBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_VERTICAL,spacing=0)
		self.add(self.mainBox)
		
		#Top Box
		self.topBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing=2)
		self.mainBox.add(self.topBox)

		#Turn on button
		self.ButtonOn = Gtk.Button(label="Turn On")
		self.ButtonOn.connect("clicked",self.turnOnLight)
		self.topBox.pack_start(self.ButtonOn,True,True,0)

		#Turn off button
		self.ButtonOff = Gtk.Button(label="Turn Off")
		self.ButtonOff.connect("clicked",self.turnOffLight)
		self.topBox.pack_start(self.ButtonOff,True,True,0)

		#Choose color button
		self.ChooseColorButton = Gtk.Button(label="Change Color")
		self.ChooseColorButton.connect("clicked",self.chooseColor)
		self.topBox.pack_start(self.ChooseColorButton,True,True,0)

		#Brightness slider
		self.brightnessAdjustement = Gtk.Adjustment(50,0,100,5,10,0)
		self.BrightnessSlider = Gtk.Scale(orientation=Gtk.STYLE_CLASS_HORIZONTAL,adjustment=self.brightnessAdjustement)
		self.BrightnessSlider.set_property("value-pos",1)
		self.BrightnessSlider.set_digits(0)
		self.BrightnessSlider.connect("value-changed",self.adjustBrightness)
		self.mainBox.pack_start(self.BrightnessSlider,False,True,0)
		

		# #Current State label
		# self.CurrentStateLabel = tk.Label(self)
		# self.CurrentStateLabel["text"] = "Current State : On"
		# self.CurrentStateLabel.pack(side="left",padx=20)

	def turnOnLight(self,widget):
		self.bulb.turnOn()

	def turnOffLight(self,widget):
		self.bulb.turnOff()

	def adjustBrightness(self,event):
		self.bulb.adjustBrightness(self.BrightnessSlider.get_value())
	
	def chooseColor(self,widget):

		# Préparer la boite de dialogue
		self.dialog = Gtk.ColorChooserDialog(title="Choose a new color",parent=self)
		#self.dialog.set_property("show-editor",True)
		self.dialogResponse = self.dialog.run()
		self.color = self.dialog.get_rgba()

		# Traiter la réponse
		if(self.dialogResponse == Gtk.ResponseType.OK):
			print("New color : "+str(self.color))
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
