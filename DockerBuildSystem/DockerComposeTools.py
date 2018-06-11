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


def DockerComposeUp(composeFiles, abortOnContainerExit = True):
    terminalCommand = "docker-compose"
    terminalCommand += MergeComposeFileToTerminalCommand(composeFiles)
    if abortOnContainerExit:
        terminalCommand += " up --abort-on-container-exit"
    else:
        terminalCommand += " up"
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


def ExecuteComposeTests(composeFiles, testContainerNames):
    DockerComposeBuild(composeFiles)
    DockerComposeUp(composeFiles)
    exitCode = 0
    for testContainerName in testContainerNames:
        exitCode = DockerImageTools.GetContainerExitCode(testContainerName)
    DockerComposeDown(composeFiles)
    DockerComposeRemove(composeFiles)
    if exitCode > 0:
        raise Exception("Container test '" + testContainerName + "' FAILED!")
    print(testContainerName + " container test finished with success.")


def MergeComposeFileToTerminalCommand(composeFiles):
    terminalCommand = ""
    for composeFile in composeFiles:
        terminalCommand += " -f " + composeFile
    return terminalCommand
