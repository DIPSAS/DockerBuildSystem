import yaml
import re
import os


def GetYamlData(yamlFiles, ignoreEmptyYamlData = False, infoMsgOnError = None):
    yamlStrings = ""
    for yamlFile in yamlFiles:
        yamlStrings += GetYamlString(yamlFile)
    yamlStrings = ReplaceEnvironmentVariablesMatches(yamlStrings)
    yamlData = yaml.safe_load(yamlStrings)
    if yamlData == None:
        if ignoreEmptyYamlData:
            yamlData = {}
            return yamlData
        errorMsg = "No yml data where discovered!\r\n"
        if not(infoMsgOnError == None):
            errorMsg += infoMsgOnError
        raise Exception(errorMsg)
    return yamlData


def ReplaceEnvironmentVariablesMatches(yamlString):
    pattern = r'\$\{([^}^{]+)\}'
    matches = re.finditer(pattern, yamlString)
    for match in matches:
        envVar = match.group()[2:-1]
        envValue = os.environ.get(envVar)
        if envValue == None:
            envValue = ''
        yamlString = yamlString.replace(match.group(), envValue)
    return yamlString


def GetYamlString(yamlFile):
    with open(yamlFile) as f:
        yamlString = f.read() + "\r\n"
    return yamlString


def DumpYamlDataToFile(yamlData, yamlFile):
    yamlDump = yaml.dump(yamlData)
    with open(yamlFile, 'w') as f:
        f.write(yamlDump)


def TryGetFromDictionary(dictionary, key, defaultValue):
    if key in dictionary:
        return dictionary[key]
    return defaultValue


def GetProperties(propertyType, yamlData):
    properties = {}
    if propertyType in yamlData:
        properties = yamlData[propertyType]
    return properties