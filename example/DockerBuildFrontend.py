import sys
import os
import DockerBuildCommon
from DockerBuildSystem import TerminalTools, DockerComposeTools, VersionTools

AvailableCommands = [
    ["run-dev", "Run frontend services on local docker host in development environmnent."],
    ["run-prod", "Run frontend services on local docker host in production environmnent."],
    ["build-dev", "Build frontend service images in development environmnent."],
    ["build-prod", "Build frontend service images in production environmnent."],
    ["test", "Test frontend services."],
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
        os.chdir("frontend/src/")
        DockerComposeTools.ExecuteComposeTests(['docker-compose.tests.yml'], ['lab-frontend-tests'])
        os.chdir("..")

    elif buildSelection == "publish-image":
        VersionTools.ExportVersionFromChangelogToEnvironment("frontend/CHANGELOG.md", "version")
        UseCommonBuildSelection(buildSelection)

    elif buildSelection == "publish-npm":
        VersionTools.ExportVersionFromChangelogToEnvironment("frontend/CHANGELOG.md", "version")
        UseCommonBuildSelection(buildSelection)
    
    elif buildSelection == "publish-nuget":
        print("Frontend solution does not publish nuget packages.")

    elif buildSelection == "help":
        TerminalTools.PrintAvailableCommands(AvailableCommands)

    else:
        print("Please provide a valid build argument: ")
        BuildDocker("help")


def UseCommonBuildSelection(buildSelection):
    os.chdir("frontend/src/")
    DockerBuildCommon.BuildDocker(buildSelection)
    os.chdir("../..")


if __name__ == "__main__":
    buildSelections = DockerBuildCommon.GetBuildSelections()
    for buildSelection in buildSelections:
        BuildDocker(buildSelection)
