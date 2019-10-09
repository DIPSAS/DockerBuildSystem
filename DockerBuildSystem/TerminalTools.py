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


def ExecuteTerminalCommands(terminalCommands, raiseExceptionWithErrorCode=False):
    for terminalCommand in terminalCommands:
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
            errorMsg = "Terminal command: '" + terminalCommand + \
                "' executed with error return code: " + str(returnCode)
            if raiseExceptionWithErrorCode:
                raise Exception(errorMsg)
            print(errorMsg)


def ExecuteTerminalCommandAndGetOutput(terminalCommand):
    print("Executing: " + terminalCommand)
    output = subprocess.Popen(terminalCommand, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return output


def GetNumbersFromString(string):
    strNumbers = re.findall(r'\d+', str(string))
    numbers = [int(i) for i in strNumbers]
    return numbers


def ExportVariableToEnvironment(variable, variableName):
    os.environ[variableName] = str(variable)
