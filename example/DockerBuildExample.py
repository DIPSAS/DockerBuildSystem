import sys
from DockerBuildSystem import TerminalTools, DockerComposeTools, VersionTools

AvailableCommands = [
    ["run", "Run services."],
    ["build-dev", "Build services."],
    ["test", "Test services."],
    ["publish", "Publish images."],
    ["help", "Print available argument commands."]
]

def BuildDocker(buildSelection):
    VersionTools.ExportVersionFromChangelogToEnvironment('CHANGELOG.md', 'VERSION')
    composeFiles = [
        'docker-compose.yml'
    ]

    if buildSelection == "run":
        DockerComposeTools.DockerComposeUp(composeFiles)

    if buildSelection == "run":
        DockerComposeTools.DockerComposeUp(composeFiles)

    elif buildSelection == "test":
        testContainerNames = ['my-service']
        DockerComposeTools.ExecuteComposeTests(composeFiles, testContainerNames)

    elif buildSelection == "publish":
        BuildDocker("build")
        DockerComposeTools.DockerComposePush(composeFiles)
        DockerComposeTools.PublishDockerImagesWithNewTag(composeFiles, 'latest')

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
