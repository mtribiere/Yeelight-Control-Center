import json

def saveConfig(ipAddress,transitionType):
	
	#Create the obect to store
	dictionnary = {
		"ipAddress" : ipAddress,
		"transitionType" : transitionType
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