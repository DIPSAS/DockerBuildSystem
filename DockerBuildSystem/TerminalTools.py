import subprocess
import os
import re
from dotenv import load_dotenv


def LoadEnvironmentVariables(environmentVariablesFile):
    load_dotenv(environmentVariablesFile)


def LoadDefaultEnvironmentVariablesFile(defaultEnvFile = '.env'):
    if os.path.isfile(defaultEnvFile):
        LoadEnvironmentVariables(defaultEnvFile)


def PrintAvailableCommands(availableCommands):
    for availableCommand in availableCommands:
        print(availableCommand)


def ExecuteTerminalCommands(terminalCommands, raiseExceptionWithErrorCode=False, printCommand=False):
    for terminalCommand in terminalCommands:
        if printCommand:
            print("Executing: " + terminalCommand)
            
        keyboardInterrupt = False
        returnCode = 0
        try:
            returnCode = subprocess.Popen(terminalCommand, shell=True).wait()
        except KeyboardInterrupt:
            keyboardInterrupt = True
        if keyboardInterrupt and raiseExceptionWithErrorCode:
            raise Exception("Exception thrown due to keyboardinterrupt")
        if returnCode > 0:
            errorMsg = "Terminal command"
            if printCommand:
                errorMsg += " '" + terminalCommand + "'"
            else:
                errorMsg += " executed with error return code: " + str(returnCode)
            if raiseExceptionWithErrorCode:
                raise Exception(errorMsg)
            print(errorMsg)


def ExecuteTerminalCommandAndGetOutput(terminalCommand, includeErrorOutput = False, printCommand=False):
    if printCommand:
        print("Executing: " + terminalCommand)
    stderr = None
    if includeErrorOutput:
        stderr = subprocess.PIPE
    outputList = subprocess.Popen(terminalCommand, stdout=subprocess.PIPE, stderr=stderr, shell=True).communicate()
    output = b""
    for outputLine in outputList:
        if not(outputLine is None):
            output += outputLine
    return output


def GetNumbersFromString(string):
    strNumbers = re.findall(r'\d+', str(string))
    numbers = [int(i) for i in strNumbers]
    return numbers


def ExportVariableToEnvironment(variable, variableName):
    os.environ[variableName] = str(variable)
