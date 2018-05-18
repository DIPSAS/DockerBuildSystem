# Docker Build System

A simple library for handling docker commands with python.

## Example
- Include DockerBuildSystem tools:
```python
from DockerBuildSystem import DockerComposeTools, DockerImageTools, DockerSwarmTools, TerminalTools, VersionTools
```

- Merge, build and run docker-compose.*.yml files:
```python
composeFiles = [
    'docker-compose.yml',
    'docker-compose.build.yml',
    'docker-compose.override.yml'
]
mergedComposeFile = "docker-compose.generated.dev.yml"
DockerComposeTools.MergeComposeFiles(composeFiles, mergedComposeFile)
DockerComposeTools.DockerComposeBuild([mergedComposeFile])
DockerComposeTools.DockerComposeUp([mergedComposeFile])
```

- Push and pull images in docker-compose.*.yml files, including additional `latest` tag:
```python
composeFiles = [
    'docker-compose.yml'
]
DockerComposeTools.DockerComposePush(composeFiles)
DockerComposeTools.PublishDockerImagesWithNewTag(composeFiles, 'latest')
DockerComposeTools.DockerComposePull(composeFiles)
```

- Execute test projects in Docker containers and raise exception if container exits with error code due to failing tests:
```python
composeFiles = [
    'docker-compose.tests.yml'
]
testContainerNames = [
    'lab-services-tests'
]
DockerComposeTools.ExecuteComposeTests(composeFiles, testContainerNames)
```

- Load set of specific environment variables from a `*.env` file:
```python
TerminalTools.LoadEnvironmentVariables('path_to/variables.env')
```

- Export top-most version from CHANGELOG.md file (see the example folder) as an environment variable:
```python
VersionTools.ExportVersionFromChangelogToEnvironment("path_to/CHANGELOG.md", "version")
```

Please have a look at an example of use here:
- https://github.com/DIPSAS/DockerBuildSystem/tree/master/example

## Install And/Or Upgrade
- pip install --no-cache-dir --upgrade DockerBuildSystem

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/DockerBuildSystem

## Publish New Version.
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*