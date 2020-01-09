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
    repoDigest = str(TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8")).replace('\n', '')
    return repoDigest


def GetImageLabels(imageName):
    jsonInfo = GetImageInfo(imageName)
    labels = jsonInfo['ContainerConfig']['Labels']
    return labels


def GetImageLabel(imageName, labelKey):
    labels = GetImageLabels(imageName)
    if labelKey in labels:
        return labels[labelKey]
    return '<no value>'


def CheckImageLabelExists(imageName, labelKey):
    labelValue = GetImageLabel(imageName, labelKey)
    return not(labelValue == '<no value>')


def GetImageId(imageName):
    terminalCommand = "docker inspect --format=\"{{.Id}}\" " + imageName
    imageId = str(TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8")).replace('\n', '')
    return imageId


def GetImageInfo(imageName):
    terminalCommand = "docker inspect " + imageName
    info = str(TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand).decode("utf-8"))
    jsonInfo = json.loads(info)[0]
    return jsonInfo


def GetContainerInfo(containerName):
    return GetImageInfo(containerName)


def GetLogsFromContainer(containerName):
    terminalCommand = 'docker logs {0}'.format(containerName)
    logs = str(TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand, includeErrorOutput=True).decode("utf-8"))
    return logs

def DockerLogin(server, userName, password):
    terminalCommand = 'docker login {0} -u {1} -p {2}'.format(server, userName, password)
    TerminalTools.ExecuteTerminalCommands(
        terminalCommands=[terminalCommand], 
        raiseExceptionWithErrorCode=True, 
        printCommand=False)

def DockerLogout(server):
    terminalCommand = 'docker logout {0}'.format(server)
    TerminalTools.ExecuteTerminalCommands(
        terminalCommands=[terminalCommand], 
        raiseExceptionWithErrorCode=True, 
        printCommand=False)