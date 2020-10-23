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


def DockerComposePull(composeFiles, dryRun=False):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    terminalCommand += " pull"
    if(dryRun):
        print("would have called {}".format(terminalCommand))
    else:
        TerminalTools.ExecuteTerminalCommands([terminalCommand], True)


def TagImages(composeFile, newTag, dryRun = False):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        if(not dryRun):
            DockerImageTools.TagImage(sourceImage, targetImage)
        else:
            print('Would have tagged image {} as {}'.format(sourceImage, targetImage))


def SaveImages(composeFile, outputFolder):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    if not(os.path.isdir(outputFolder)):
        os.makedirs(outputFolder)
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        imageName = sourceImage[sourceImage.rfind('/')+1:].replace(':', '-') + '.tar'
        outputPath = os.path.join(outputFolder, imageName)
        DockerImageTools.SaveImage(sourceImage, outputPath)


def PublishDockerImages(composeFile, dryRun = False):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        if(not dryRun):
            DockerImageTools.PushImage(sourceImage)
        else:
            print('Would have pushed {}'.format(sourceImage))


def PromoteDockerImages(composeFile, targetTags, sourceFeed = None, targetFeed = None, user = None, password = None, logoutFromFeeds = False, dryRun = False):
    userAndPasswordIsGiven = not(user is None or password is None)
    if userAndPasswordIsGiven and not(sourceFeed is None):
        DockerImageTools.DockerLogin(sourceFeed, user, password, dryRun)
    DockerComposePull([composeFile], dryRun)
    if userAndPasswordIsGiven and logoutFromFeeds and not(sourceFeed is None):
        DockerImageTools.DockerLogout(sourceFeed, dryRun)

    if userAndPasswordIsGiven and not(targetFeed is None):
        DockerImageTools.DockerLogin(targetFeed, user, password, dryRun)
    for tag in targetTags:
        PublishDockerImagesWithNewTag(composeFile, tag, sourceFeed, targetFeed, dryRun)
    if userAndPasswordIsGiven and logoutFromFeeds and not(targetFeed is None):
        DockerImageTools.DockerLogout(targetFeed, dryRun)


def PublishDockerImagesWithNewTag(composeFile, newTag, sourceRepository = None, targetRepository = None, dryRun = False):
    dockerComposeMap = YamlTools.GetYamlData([composeFile])
    for service in dockerComposeMap['services']:
        sourceImage = dockerComposeMap['services'][service]['image']
        tagIndex = sourceImage.rfind(':')
        targetImage = sourceImage[:tagIndex+1] + str(newTag)
        if not(sourceRepository is None or targetRepository is None):
            targetImage = targetImage.replace(sourceRepository, targetRepository, 1)
        if dryRun:
            print("Would have tagged image {} as {}".format(sourceImage, targetImage))
            print("Would have pushed image {}".format(targetImage))
        else:
            DockerImageTools.TagImage(sourceImage, targetImage)
            DockerImageTools.PushImage(targetImage)


def ExecuteComposeTests(composeFiles, testContainerNames = None, removeTestContainers = True, buildCompose = True, downCompose = True):
    if testContainerNames is None:
        TerminalTools.LoadDefaultEnvironmentVariablesFile()
        yamlData = YamlTools.GetYamlData(composeFiles)
        testContainerNames = GetContainerNames(yamlData)

    if buildCompose:
        DockerComposeBuild(composeFiles)
    DockerComposeUp(composeFiles)
    sumExitCodes, sumErrorMsgs = DockerImageTools.VerifyContainerExitCode(testContainerNames)
    if downCompose:
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
