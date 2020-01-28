import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class SettingDialog(Gtk.Dialog):

	def __init__(self,parent,currentIp,currentTransitionType,currentTransitionTime):
		Gtk.Dialog.__init__(self,"Settings",
								parent,
								0)
		
		#Setup GUI
		self.createWidget()
		self.createButtons()

		#Fill informations
		self.ipEntery.set_text(currentIp)

		if(currentTransitionType == "sudden"):
			self.transitionTypeCombo.set_active(0)
		else:
			self.transitionTypeCombo.set_active(1)
		
		self.transitionTimeSpin.set_value(currentTransitionTime)

		self.show_all()

	def createWidget(self):

		# Main box
		self.contentArea = self.get_content_area()
		self.mainBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_VERTICAL,spacing=2) 
		self.contentArea.add(self.mainBox)

		# IP Box
		self.ipBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing = 2)
		self.mainBox.add(self.ipBox)

		self.ipLabel = Gtk.Label("Bulb IP address :")
		self.ipBox.pack_start(self.ipLabel,False,True,0)

		self.ipEntery = Gtk.Entry()
		self.ipBox.pack_start(self.ipEntery,True,True,0)

		#Transition Type Box
		self.transitionTypeBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing = 2)
		self.mainBox.add(self.transitionTypeBox)

		self.transitionTypeLabel = Gtk.Label("Transition type : ")
		self.transitionTypeBox.pack_start(self.transitionTypeLabel,False,True,0)

		transitionTypes = [["Sudden"],["Smooth"]]
		transitionsModel = Gtk.ListStore(str)
		for i in range(0,len(transitionTypes)):
			transitionsModel.append(transitionTypes[i])

		self.transitionTypeCombo = Gtk.ComboBox(model=transitionsModel)
		cell = Gtk.CellRendererText()

		self.transitionTypeCombo.connect("changed",self.onTransitionTypeChanged)
		self.transitionTypeCombo.pack_start(cell,False)
		self.transitionTypeCombo.add_attribute(cell,"text",0)

		self.transitionTypeBox.pack_start(self.transitionTypeCombo,True,True,0)

		#Transition Time Box
		self.transitionTimeBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_HORIZONTAL,spacing=2)
		self.mainBox.add(self.transitionTimeBox)

		self.transitionTimeLabel = Gtk.Label("Transition time : ")
		
		self.transitionTimeBox.pack_start(self.transitionTimeLabel,False,True,0)

		self.spinAdjustment = Gtk.Adjustment(value = 500,lower=30,upper=10000,step_increment=100,page_increment=0,page_size=0)
		self.transitionTimeSpin = Gtk.SpinButton(adjustment=self.spinAdjustment,climb_rate=100,digits=0)
		
		self.transitionTimeBox.pack_start(self.transitionTimeSpin,True,True,0)

		# Seperator
		self.seperator = Gtk.Separator(orientation=Gtk.STYLE_CLASS_HORIZONTAL)
		self.mainBox.add(self.seperator)
	
	
	def createButtons(self):

		#Cancel button
		self.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL)

		#Ok button
		self.add_buttons(Gtk.STOCK_OK,Gtk.ResponseType.OK)

	def onTransitionTypeChanged(self,widget):

		#If the selected transition type is sudden
		if(self.transitionTypeCombo.get_active() == 0):
			self.transitionTimeSpin.set_sensitive(False)
		else:
			self.transitionTimeSpin.set_sensitive(True)
	
	def getIp(self):
		return self.ipEntery.get_text()
	
	def getTransitionType(self):
		return self.transitionTypeCombo.get_active()
	
	def getTransitionTime(self):
		return int(self.transitionTimeSpin.get_value()) 