import os
import random
from DockerBuildSystem import TerminalTools, DockerImageTools, YamlTools


def MergeComposeFiles(composeFiles, outputComposeFile):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " config > " + outputComposeFile
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def DockerComposeBuild(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " build"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def DockerComposeUp(composeFiles, abortOnContainerExit = True, detached = False):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " up"
    if detached:
        terminalCommand += " -d"
    elif abortOnContainerExit:
        terminalCommand += " --abort-on-container-exit"
    TerminalTools.ExecuteTerminalCommands([terminalCommand], False)


def DockerComposeDown(composeFiles):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " down"
    TerminalTools.ExecuteTerminalCommands([terminalCommand])


def DockerComposeRemove(composeFiles, force = True):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " rm"
    if force:
        terminalCommand += " -f"
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
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        DockerImageTools.TagImage(sourceImage, targetImage)


def SaveImages(composeFile, outputFolder):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    if not(os.path.isdir(outputFolder)):
        os.makedirs(outputFolder)
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        imageName = sourceImage[sourceImage.rfind('/')+1:].replace(':', '-') + '.tar'
        outputPath = os.path.join(outputFolder, imageName)
        DockerImageTools.SaveImage(sourceImage, outputPath)


def PublishDockerImages(composeFile):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        DockerImageTools.PushImage(sourceImage)


def PublishDockerImagesWithNewTag(composeFile, newTag):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        DockerImageTools.TagImage(sourceImage, targetImage)
        DockerImageTools.PushImage(targetImage)


def ExecuteComposeTests(composeFiles, testContainerNames = None, removeTestContainers = True):
    if testContainerNames is None:
        TerminalTools.LoadDefaultEnvironmentVariablesFile()
        yamlData = YamlTools.GetYamlData(composeFiles)
        testContainerNames = GetContainerNames(yamlData)

    DockerComposeBuild(composeFiles)
    DockerComposeUp(composeFiles)
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


def AddDigestsToImageTags(yamlData):
    for service in yamlData.get('services', []):
        if not('image' in yamlData['services'][service]):
            continue

        imageName = yamlData['services'][service]['image']
        imageName = YamlTools.ReplaceEnvironmentVariablesMatches(imageName)
        repoDigests = DockerImageTools.GetImageInfo(imageName)['RepoDigests']
        if len(repoDigests) > 0:
            yamlData['services'][service]['image'] = str(repoDigests[0])
        else:
            yamlData['services'][service]['image'] = imageName


def AddContainerNames(yamlData, prefix = None, subfix = None):
    services = yamlData.get('services', [])
    for service in services:
        if not ('container_name' in yamlData['services'][service]):
            containerName = service
            if not(prefix is None):
                containerName = prefix + containerName
            if not(subfix is None):
                containerName = containerName + subfix
            else:
                random.seed()
                randomId = random.randint(0, 1000)
                containerName = containerName + "_" + str(randomId)

            yamlData['services'][service]['container_name'] = containerName


def GetContainerNames(yamlData):
    services = yamlData.get('services', [])
    containerNames = []
    for service in services:
        if 'container_name' in yamlData['services'][service]:
            containerNames.append(yamlData['services'][service]['container_name'])

    return containerNames
