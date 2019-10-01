from DockerBuildSystem import TerminalTools
import re
import json

def BuildImage(imageName, dockerfile = 'Dockerfile', context = '.'):
    dockerCommand = "docker build -f " + dockerfile + " -t " + imageName + " " + context
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def RunImage(imageName, properties = ""):
    dockerCommand = "docker run " + properties + " " + imageName
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def PullImage(imageName):
    dockerCommand = "docker pull " + imageName
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def PushImage(imageName):
    dockerCommand = "docker push " + imageName
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def TagImage(sourceImage, targetImage):
    dockerCommand = "docker tag " + sourceImage + " " + targetImage
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def SaveImage(imageName, outputPath):
    dockerCommand = "docker save -o " + outputPath + " " + imageName
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def GetContainerExitCode(containerName):
    terminalCommand = "docker inspect " + containerName + " --format='{{.State.ExitCode}}'"
    output = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand)
    exitCode = TerminalTools.GetNumbersFromString(output)[0]
    return int(exitCode)


def GetContainerRunningCode(containerName):
    terminalCommand = "docker inspect " + \
        containerName + " --format='{{.State.Running}}'"
    output = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand)
    running = bool(re.search('true', str(output).lower()))
    return running


def CopyFromContainerToHost(containerName, containerSrc, hostDest):
    terminalCommand = "docker cp " + \
        containerName + ":" + containerSrc + " " + hostDest
    TerminalTools.ExecuteTerminalCommands([terminalCommand])


def GetImageRepoDigest(imageName):
    terminalCommand = "docker inspect --format=\"{{index .RepoDigests 0}}\" " + imageName
    repoDigest = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8").replace('\n', '')
    return repoDigest


def GetImageLabel(imageName, labelKey):
    terminalCommand = "docker inspect --format=\"{{.Config.Labels." + labelKey + "}}\" " + imageName
    labelValue = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8")
    if len(labelValue) > 0 and labelValue[-1] == '\n':
        labelValue = labelValue[:-1]
    return labelValue


def CheckImageLabelExists(imageName, labelKey):
    labelValue = GetImageLabel(imageName, labelKey)
    return not(labelValue == '<no value>')


def GetImageId(imageName):
    terminalCommand = "docker inspect --format=\"{{.Id}}\" " + imageName
    imageId = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8").replace('\n', '')
    return imageId


def GetImageInfo(imageName):
    terminalCommand = "docker inspect " + imageName
    info = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8")
    jsonInfo = json.loads(info)[0]
    return jsonInfo


def GetContainerInfo(containerName):
    return GetImageInfo(containerName)