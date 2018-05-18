import sys
from DockerBuildSystem import TerminalTools, DockerComposeTools, VersionTools

AvailableCommands = [
    ["run-dev", "Run services on local docker host in development environmnent."],
    ["run-prod", "Run services on local docker host in production environmnent."],
    ["build-dev", "Build service images in development environmnent."],
    ["build-prod", "Build service images in production environmnent."],
    ["test", "Test services."],
    ["publish-image", "Publish images."],
    ["publish-npm", "Publish npm package."],
    ["publish-nuget", "Publish nuget package."],
    ["help", "Print available argument commands."]
]

def BuildDocker(buildSelection):
    if buildSelection == "run-dev":
        BuildDocker("build-dev")
        composeFiles = [
            'docker-compose.generated.dev.yml'
        ]
        DockerComposeTools.DockerComposeUp(composeFiles)

    if buildSelection == "run-prod":
        BuildDocker("build-prod")
        composeFiles = [
            'docker-compose.generated.prod.yml'
        ]
        DockerComposeTools.DockerComposeUp(composeFiles)

    elif buildSelection == "build-dev":
        composeFiles = [
            'docker-compose.yml',
            'docker-compose.build.yml',
            'docker-compose.override.yml'
        ]
        mergedComposeFile = "docker-compose.generated.dev.yml"
        DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerComposeTools.DockerComposeBuild([mergedComposeFile])

    elif buildSelection == "build-prod":
        composeFiles = [
            'docker-compose.yml',
            'docker-compose.build.yml'
        ]
        mergedComposeFile = "docker-compose.generated.prod.yml"
        DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerComposeTools.DockerComposeBuild([mergedComposeFile])

    elif buildSelection == "test":
        composeFiles = [
            'docker-compose.tests.yml'
        ]
        testContainerNames = [
            'lab-services-tests'
        ]
        DockerComposeTools.ExecuteComposeTests(composeFiles, testContainerNames)

    elif buildSelection == "publish-image":
        BuildDocker("build-prod")
        composeFiles = [
            'docker-compose.generated.prod.yml'
        ]
        DockerComposeTools.DockerComposePush(composeFiles)
        DockerComposeTools.PublishDockerImagesWithNewTag(composeFiles, 'latest')

    elif buildSelection == "publish-npm":
        composeFiles = [
            'docker-compose.publish.npm.yml'
        ]
        mergedComposeFile = "docker-compose.generated.npm.yml"
        DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerComposeTools.DockerComposeBuild([mergedComposeFile])

    elif buildSelection == "publish-nuget":
        composeFiles = [
            'docker-compose.publish.nuget.yml'
        ]
        mergedComposeFile = "docker-compose.generated.nuget.yml"
        DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerComposeTools.DockerComposeBuild([mergedComposeFile])

    elif buildSelection == "help":
        TerminalTools.PrintAvailableCommands(AvailableCommands)

    else:
        print("Please provide a valid build argument: ")
        BuildDocker("help")

def GetBuildSelections():
    buildSelections = sys.argv[1:]
    if len(buildSelections) == 0:
        buildSelections = ["no_argument"]
    return buildSelections

if __name__ == "__main__":
    buildSelections = GetBuildSelections()
    for buildSelection in buildSelections:
        BuildDocker(buildSelection)
