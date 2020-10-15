import yaml
import re
import os


def GetYamlData(yamlFiles, ignoreEmptyYamlData = False, infoMsgOnError = None, replaceEnvironmentVariablesMatches = True):
    yamlData = {}
    for yamlFile in yamlFiles:
        newYamlData = GetSingleYamlData(yamlFile, ignoreEmptyYamlData, infoMsgOnError, replaceEnvironmentVariablesMatches)
        yamlData = MergeYamlData(yamlData, newYamlData)
    return yamlData


def GetSingleYamlData(yamlFile, ignoreEmptyYamlData = False, infoMsgOnError = None, replaceEnvironmentVariablesMatches = True):
    yamlStrings = GetYamlString(yamlFile)
    if replaceEnvironmentVariablesMatches:
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


def MergeYamlData(yamlData1, yamlData2):
    for key in yamlData2:
        if key in yamlData1:
            if isinstance(yamlData1[key], dict) and isinstance(yamlData2[key], dict):
                MergeYamlData(yamlData1[key], yamlData2[key])
            elif isinstance(yamlData1[key], list) and isinstance(yamlData2[key], list):
                for listValue in yamlData2[key]:
                    if not(listValue in yamlData1[key]):
                        yamlData1[key].append(listValue)
            else:
                yamlData1[key] = yamlData2[key]
        else:
            yamlData1[key] = yamlData2[key]
    return yamlData1


def ReplaceEnvironmentVariablesMatches(yamlString):
    pattern = r'\$\{([^}^{]+)\}'
    matches = re.finditer(pattern, yamlString)
    for match in matches:
        envVar = match.group()[2:-1]
        defaultValue = ''
        defaultValuePatternMatch = ':-'
        if envVar.find(defaultValuePatternMatch) >= 0:
            defaultValue = envVar[envVar.find(defaultValuePatternMatch)+len(defaultValuePatternMatch):]
            envVar = envVar[:envVar.find(defaultValuePatternMatch)]
        envValue = os.environ.get(envVar)
        if envValue == None:
            envValue = defaultValue
        yamlString = yamlString.replace(match.group(), envValue)
    return yamlString


def GetYamlString(yamlFile):
    with open(yamlFile) as f:
        yamlString = f.read() + "\r\n"
    return yamlString


def DumpYamlDataToFile(yamlData, yamlFile):
    yamlDump = yaml.dump(yamlData)
    CreateFoldersInPath(yamlFile)
    with open(yamlFile, 'w') as f:
        f.write(yamlDump)


def CreateFoldersInPath(filename):
    basename = os.path.basename(filename)
    dirs = filename[:filename.find(basename)]
    if len(dirs) > 0 and not(os.path.exists(dirs)):
        os.makedirs(dirs)


def TryGetFromDictionary(dictionary, key, defaultValue):
    if key in dictionary:
        return dictionary[key]
    return defaultValue


def GetProperties(propertyType, yamlData):
    properties = {}
    if propertyType in yamlData:
        properties = yamlData[propertyType]
    return properties