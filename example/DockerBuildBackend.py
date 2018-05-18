import sys
import os
import DockerBuildCommon
from DockerBuildSystem import TerminalTools, DockerComposeTools, VersionTools

AvailableCommands = [
    ["run-dev", "Run backend services on local docker host in development environment."],
    ["run-prod", "Run backend services on local docker host in production environment."],
    ["build-dev", "Build backend service images in development environment."],
    ["build-prod", "Build backend service images in production environment."],
    ["test", "Test backend services with unit testing and integration testing."],
    ["publish-image", "Publish images."],
    ["publish-npm", "Publish npm package."],
    ["publish-nuget", "Publish nuget package."],
    ["help", "Print available argument commands."]
]

def BuildDocker(buildSelection):
    if buildSelection == "run-dev":
        UseCommonBuildSelection(buildSelection)

    if buildSelection == "run-prod":
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "build-dev":
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "build-prod":
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "test":
        os.chdir("backend/src/")
        DockerComposeTools.ExecuteComposeTests(['docker-compose.tests.yml'], ['lab-backend-tests'])
        os.chdir("..")

    elif buildSelection == "publish-image":
        VersionTools.ExportVersionFromChangelogToEnvironment("backend/CHANGELOG.md", "version")
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "publish-npm":
        print("Backend solution does not publish npm packages.")

    elif buildSelection == "publish-nuget":
        VersionTools.ExportVersionFromChangelogToEnvironment("backend/CHANGELOG.md", "version")
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "help":
        TerminalTools.PrintAvailableCommands(AvailableCommands)

    else:
        print("Please provide a valid build argument: ")
        BuildDocker("help")

def UseCommonBuildSelection(buildSelection):
    os.chdir("backend/src/")
    DockerBuildCommon.BuildDocker(buildSelection)
    os.chdir("../..")

if __name__ == "__main__":
    buildSelections = DockerBuildCommon.GetBuildSelections()
    for buildSelection in buildSelections:
        BuildDocker(buildSelection)
