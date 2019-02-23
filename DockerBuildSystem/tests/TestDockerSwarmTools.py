import unittest
import random
import os
from . import TestTools
from .. import DockerSwarmTools
from .. import DockerComposeTools

class TestDockerSwarmTools(unittest.TestCase):

    def test_a_StartSwarm(self):
        print('SWARM START')
        DockerSwarmTools.StartSwarm()
        print('DONE SWARM START')

    def test_b_CreateRemoveNetwork(self):
        print('CREATE NETWORK')
        network = 'my-network-' + str(random.randint(0, 10000))
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerSwarmTools.CreateSwarmNetwork(network)
        DockerSwarmTools.RemoveSwarmNetwork(network)
        os.chdir(cwd)
        print('DONE CREATE NETWORK')

    def test_c_CreateRemoveConfig(self):
        print('CREATE CONFIG')
        config = 'changelog-config-' + str(random.randint(0, 10000))
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerSwarmTools.CreateSwarmConfig('CHANGELOG.md', config)
        DockerSwarmTools.RemoveSwarmConfig(config)
        os.chdir(cwd)
        print('DONE CREATE CONFIG')

    def test_d_CreateRemoveSecret(self):
        print('CREATE SECRET')
        secret = 'changelog-secret-' + str(random.randint(0, 10000))
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerSwarmTools.CreateSwarmSecret('CHANGELOG.md', secret)
        DockerSwarmTools.RemoveSwarmSecret(secret)
        os.chdir(cwd)
        print('DONE CREATE SECRET')

    def test_e_CreateRemoveVolume(self):
        print('CREATE VOLUME')
        volume = 'test-volume-' + str(random.randint(0, 10000))
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerSwarmTools.CreateSwarmVolume(volume)
        DockerSwarmTools.RemoveSwarmVolume(volume)
        os.chdir(cwd)
        print('DONE CREATE VOLUME')

    def test_f_CreateRemoveStack(self):
        print('CREATE STACK')
        stack = 'test-stack-' + str(random.randint(0, 10000))
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.DockerComposeBuild(['docker-compose.yml'])
        DockerSwarmTools.DeployStack('docker-compose.yml', stack, [])
        DockerSwarmTools.RemoveStack(stack)
        os.chdir(cwd)
        print('DONE CREATE STACK')


if __name__ == '__main__':
    unittest.main()