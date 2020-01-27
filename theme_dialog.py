import gi
import os
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import JSONutils as themeFile

class ThemeDialog(Gtk.Dialog):

	def __init__(self,parent):
		Gtk.Dialog.__init__(self,"Themes",
								 parent,
								 0)

		#Setup GUI
		self.createWidget()
		self.createButtons()

		self.show_all()

	def createWidget(self):

		#Main grid	
		self.contentArea = self.get_content_area()
		
		self.mainGrid = Gtk.Grid() 
		self.mainGrid.set_property("row-spacing",4)
		self.mainGrid.set_property("column-spacing",10)

		self.contentArea.add(self.mainGrid)

		#Setup grid 3xN
		themes = themeFile.loadTheme()
		
		i = 0
		j = 0
		for filename in os.listdir("img/themes"):
			
			#Create template
			tmpBox = Gtk.Box(orientation=Gtk.STYLE_CLASS_VERTICAL,spacing = 2)

			#Load the image
			tmpImage = Gtk.Image()
			tmpImage.set_from_file("img/themes/"+filename)

			tmpBox.add(tmpImage)

			#Load the label
			tmpButton = Gtk.Button(label=themes[filename[:-4]]["name"])
			
			tmpBox.add(tmpButton)

			#Add to the grid
			self.mainGrid.attach(tmpBox,i,j,1,1)

			#Continue to the next cell
			j += 1

			if(j == 2):
				i += 1
				j = 0

		# Seperator
		self.seperator = Gtk.Separator(orientation=Gtk.STYLE_CLASS_HORIZONTAL)
		self.contentArea.add(self.seperator)


	def createButtons(self):

		#Cancel button
		self.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL)

