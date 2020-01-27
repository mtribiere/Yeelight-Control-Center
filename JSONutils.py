import json

def saveConfig(ipAddress,transitionType,transitionTime):
	
	#Create the obect to store
	dictionnary = {
		"ipAddress" : ipAddress,
		"transitionType" : transitionType,
		"transitionTime" : transitionTime
	}

	jsonParsed = json.dumps(dictionnary,indent=4)

	#Write the config to text
	with open("config/config.cfg",'w') as configFile:
		configFile.write(jsonParsed)

def loadConfig():

	#Read the file
	with open("config/config.cfg",'r') as configFile:
		dictionnary = json.load(configFile)
	
	return dictionnary


def loadTheme():

	#Read the file
	with open("config/themes.cfg",'r') as themeFile:
		dictionnary = json.load(themeFile)
	
	return dictionnary