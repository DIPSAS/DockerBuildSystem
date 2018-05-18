from DockerBuildSystem import TerminalTools


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


def GetContainerExitCode(containerName):
    terminalCommand = "docker inspect " + containerName + " --format='{{.State.ExitCode}}'"
    output = TerminalTools.ExecuteTerminalCommandAndGetOutput(terminalCommand)
    exitCode = TerminalTools.GetNumbersFromString(output)[0]
    return int(exitCode)
