import yaml
from DockerBuildSystem import TerminalTools, DockerImageTools


def MergeComposeFiles(composeFiles, outputComposeFile):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " config>" + outputComposeFile
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def DockerComposeBuild(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " build"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def DockerComposeUp(composeFiles, abortOnContainerExit = True, detached = False):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    if abortOnContainerExit:
        terminalCommand += " up --abort-on-container-exit"
    else:
        terminalCommand += " up"
        if detached:
            terminalCommand += " -d"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], False)


def DockerComposeDown(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " down"
    TerminalTools.ExecuteTerminalCommands([terminalCommand])


def DockerComposeRemove(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " rm"
    TerminalTools.ExecuteTerminalCommands([terminalCommand])


def DockerComposePush(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " push"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def DockerComposePull(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " pull"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def TagImages(composeFile, newTag):
    dockerComposeStream = open(composeFile, 'r')
    dockerComposeMap = yaml.safe_load(dockerComposeStream)
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        DockerImageTools.TagImage(sourceImage, targetImage)


def PublishDockerImages(composeFile):
    dockerComposeStream = open(composeFile, 'r')
    dockerComposeMap = yaml.safe_load(dockerComposeStream)
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        DockerImageTools.PushImage(sourceImage)


def PublishDockerImagesWithNewTag(composeFile, newTag):
    dockerComposeStream = open(composeFile, 'r')
    dockerComposeMap = yaml.safe_load(dockerComposeStream)
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        DockerImageTools.TagImage(sourceImage, targetImage)
        DockerImageTools.PushImage(targetImage)


def ExecuteComposeTests(composeFiles, testContainerNames, removeTestContainers = True):
    DockerComposeBuild(composeFiles)
    DockerComposeUp(composeFiles)
    exitCode = 0
    sumExitCodes = 0
    sumErrorMsgs = ""
    for testContainerName in testContainerNames:
        exitCode = DockerImageTools.GetContainerExitCode(testContainerName)
        sumExitCodes += exitCode
        if exitCode > 0:
            errorMsg = "Container test '" + testContainerName + "' FAILED!\r\n"
            sumErrorMsgs += errorMsg
            print(errorMsg)
        else:
            print(testContainerName + " container test finished with success.\r\n")
    DockerComposeDown(composeFiles)
    if removeTestContainers:
        DockerComposeRemove(composeFiles)
    if sumExitCodes > 0:
        raise Exception(sumErrorMsgs)


def CreateLocalNetwork(networkName):
    print("Creating local network: " + networkName)
    dockerCommand = "docker network create --attachable --driver=bridge "
    dockerCommand += networkName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def MergeComposeFileToTerminalCommand(composeFiles):
    terminalCommand = ""
    for composeFile in composeFiles:
        terminalCommand += " -f " + composeFile
    return terminalCommand
