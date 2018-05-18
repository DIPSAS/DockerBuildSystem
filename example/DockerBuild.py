import sys
import os
import DockerBuildCommon
import DockerBuildBackend
import DockerBuildFrontend
import DockerBuildSystem

AvailableCommands = [
    ["run-dev", "Run frontend and backend services on local docker host in development environment."],
    ["run-prod", "Run frontend and backend services on local docker host in production environment."],
    ["build-dev", "Build service images of frontend and backend in development environment."],
    ["build-prod", "Build service images of frontend and backend in production environment."],
    ["test", "Test frontend and backend services."],
    ["publish", "Publish images, including npm and nuget packages of frontend and backend."],
    ["publish-image", "Publish backend and frontend images."],
    ["publish-npm", "Publish frontend npm packages."],
    ["publish-nuget", "Publish backend nuget packages."],
    ["help", "Print available argument commands."]
]

def BuildDocker(buildSelection):
    print("Executing build selection: " + buildSelection)

    if buildSelection == "run-dev":
        BuildDocker("build-dev")
        composeFiles = [
            'backend/src/docker-compose.generated.dev.yml',
            'frontend/src/docker-compose.generated.dev.yml'
        ]
        mergedComposeFile = "docker-compose.generated.dev.yml"
        DockerBuildSystem.DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerBuildSystem.DockerComposeTools.DockerComposeUp([mergedComposeFile])
        
    elif buildSelection == "run-prod":
        BuildDocker("build-prod")
        composeFiles = [
            'backend/src/docker-compose.generated.prod.yml',
            'frontend/src/docker-compose.generated.prod.yml'
        ]
        mergedComposeFile = "docker-compose.generated.dev.yml"
        DockerBuildSystem.DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
        DockerBuildSystem.DockerComposeTools.DockerComposeUp([mergedComposeFile])

    elif buildSelection == "build-dev":
        DockerBuildBackend.BuildDocker('build-dev')
        DockerBuildFrontend.BuildDocker('build-dev')

    elif buildSelection == "build-prod":
        DockerBuildBackend.BuildDocker('build-prod')
        DockerBuildFrontend.BuildDocker('build-prod')

    elif buildSelection == "test":
        DockerBuildBackend.BuildDocker('test')
        DockerBuildFrontend.BuildDocker('test')

    elif buildSelection == "publish":
        DockerBuildBackend.BuildDocker('publish')
        DockerBuildFrontend.BuildDocker('publish')

    elif buildSelection == "publish-image":
        DockerBuildBackend.BuildDocker('publish-image')
        DockerBuildFrontend.BuildDocker('publish-image')

    elif buildSelection == "publish-npm":
        DockerBuildBackend.BuildDocker('publish-npm')
        DockerBuildFrontend.BuildDocker('publish-npm')

    elif buildSelection == "publish-nuget":
        DockerBuildBackend.BuildDocker('publish-npm')
        DockerBuildFrontend.BuildDocker('publish-npm')

    elif buildSelection == "help":
        DockerBuildSystem.TerminalTools.PrintAvailableCommands(AvailableCommands)

    else:
        print("Please provide a valid build argument: ")
        BuildDocker("help")

if __name__ == "__main__":
    buildSelections = sys.argv[1:]
    if len(buildSelections) == 0:
        buildSelections = ["no_argument"]
    for buildSelection in buildSelections:
        BuildDocker(buildSelection)
