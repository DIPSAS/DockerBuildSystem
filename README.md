# Docker Build System

[![PyPI version](https://badge.fury.io/py/DockerBuildSystem.svg)](https://badge.fury.io/py/DockerBuildSystem)
[![Build Status](https://travis-ci.com/DIPSAS/DockerBuildSystem.svg?branch=master)](https://travis-ci.com/DIPSAS/DockerBuildSystem)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

A simple library for handling docker commands with python.

## Install Or Upgrade
- pip install --upgrade DockerBuildSystem

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
- Optionally export versionmajor and versionminor based on the top-most version from CHANGELOG.md file as an environment variable:
```python
VersionTools.ExportVersionFromChangelogToEnvironment("path_to/CHANGELOG.md", "version", "versionmajor", "versionminor")
```

Please have a look at an example of use here:
- https://github.com/DIPSAS/DockerBuildSystem/tree/master/example

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker
- Install Dependencies:
    - pip install -r requirements.txt

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/DockerBuildSystem

## Publish New Version.
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*

## Run Unit Tests
- python -m unittest