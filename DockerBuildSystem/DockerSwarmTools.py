from DockerBuildSystem import TerminalTools
import os


def DeployStack(composeFile, stackName, environmentVariablesFiles):
    for environmentVariablesFile in environmentVariablesFiles:
        TerminalTools.LoadEnvironmentVariables(environmentVariablesFile)
    print("Deploying stack: " + stackName)
    dockerCommand = "docker stack deploy -c " + composeFile + " " + stackName
    TerminalTools.ExecuteTerminalCommands([dockerCommand], True)


def RemoveStack(stackName):
    print("Removing stack: " + stackName)
    dockerCommand = "docker stack rm " + stackName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def CreateSwarmNetwork(networkName, encrypted = False):
    print("Creating network: " + networkName)
    dockerCommand = "docker network create "
    if encrypted:
        dockerCommand += "--opt encrypted "
    dockerCommand += "--driver bridge "
    dockerCommand += "--attachable "
    dockerCommand += networkName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def RemoveSwarmNetwork(networkName):
    print("Removing network: " + networkName)
    dockerCommand = "docker network rm " + networkName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def CreateSwarmSecret(secretFile, secretName):
    print("Creating secret: " + secretName)
    dockerCommand = "docker secret create " + secretName + " " + secretFile
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def RemoveSwarmSecret(secretName):
    print("Removing secret: " + secretName)
    dockerCommand = "docker secret rm " + secretName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def CreateSwarmConfig(configFile, configName):
    print("Creating config: " + configName)
    dockerCommand = "docker config create " + configName + " " + configFile
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def RemoveSwarmConfig(configName):
    print("Removing config: " + configName)
    dockerCommand = "docker config rm " + configName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def CreateSwarmVolume(volumeName):
    print("Creating volume: " + volumeName)
    dockerCommand = "docker volume create " + volumeName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def RemoveSwarmVolume(volumeName):
    print("Removing volume: " + volumeName)
    dockerCommand = "docker volume rm " + volumeName
    TerminalTools.ExecuteTerminalCommands([dockerCommand])


def StartSwarm():
    print("Starting swarm")
    dockerCommand = "docker swarm init"
    TerminalTools.ExecuteTerminalCommands([dockerCommand])
