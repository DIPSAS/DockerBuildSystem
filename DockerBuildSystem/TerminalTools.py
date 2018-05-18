import subprocess
import sys
import os
import re
import yaml
from dotenv import load_dotenv


def LoadEnvironmentVariables(environmentVariablesFile):
    load_dotenv(environmentVariablesFile)


def PrintAvailableCommands(availableCommands):
    for availableCommand in availableCommands:
        print(availableCommand)


def ExecuteTerminalCommands(terminalCommands, raiseExceptionWithErrorCode=False):
    for terminalCommand in terminalCommands:
        print("Executing: " + terminalCommand)
        returnCode = subprocess.Popen(terminalCommand, shell=True).wait()
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


def GetContainerExitCode(containerName):
    terminalCommand = "docker inspect " + containerName + " --format='{{.State.ExitCode}}'"
    output = ExecuteTerminalCommandAndGetOutput(terminalCommand)
    exitCode = GetNumbersFromString(output)[0]
    return int(exitCode)


def GetNumbersFromString(string):
    strNumbers = re.findall(r'\d+', str(string))
    numbers = [int(i) for i in strNumbers]
    return numbers


def ExecuteComposeTest(composeFile, testContainerName):
    terminalCommands = [
        "docker-compose -f " + composeFile + " build",
        "docker-compose -f " + composeFile + " up --abort-on-container-exit",
    ]
    ExecuteTerminalCommands(terminalCommands)
    exitCode = GetContainerExitCode(testContainerName)
    if exitCode > 0:
        raise Exception("Test FAILED!")
    print(testContainerName + " container test finished with success.")
    terminalCommands = [
        "docker-compose -f " + composeFile + " down",
        "docker-compose -f " + composeFile + " rm",
    ]
    ExecuteTerminalCommands(terminalCommands)


def ExportVariableToEnvironment(variable, variableName):
    os.environ[variableName] = str(variable)
