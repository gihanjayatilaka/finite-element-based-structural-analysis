import json

def readFile(fileName):
    '''

    :param fileName: The json file name
    :return: Return a dictionary of the file content
    '''
	with open(fileName) as json_file:
		json_data = json.load(json_file)
		return json_data

def writeFile(data, fileName):
    '''

    :param data: disctionary to be written to file
    :param fileName: The json file name
    '''
	with open(fileName, 'w') as file:
		json.dump(data, file, indent=4)




