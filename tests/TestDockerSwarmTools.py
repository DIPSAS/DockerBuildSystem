import unittest
import random
import os
from tests import TestTools
from DockerBuildSystem import DockerSwarmTools
from DockerBuildSystem import DockerComposeTools

class TestDockerSwarmTools(unittest.TestCase):

    def test_a_StartSwarm(self):
        print('SWARM START')
        DockerSwarmTools.StartSwarm()
        print('DONE SWARM START')

    def test_b_CreateRemoveNetwork(self):
        print('CREATE NETWORK')
        network = 'my-network-' + str(random.randint(0, 10000))
        DockerSwarmTools.CreateSwarmNetwork(network)
        DockerSwarmTools.RemoveSwarmNetwork(network)

        DockerSwarmTools.CreateSwarmNetwork(network, encrypted=True, driver="overlay", attachable=False, options=['--ipv6'])
        DockerSwarmTools.RemoveSwarmNetwork(network)

        print('DONE CREATE NETWORK')

    def test_c_CreateRemoveConfig(self):
        print('CREATE CONFIG')
        config = 'changelog-config-' + str(random.randint(0, 10000))
        DockerSwarmTools.CreateSwarmConfig(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.md'), config)
        DockerSwarmTools.RemoveSwarmConfig(config)
        print('DONE CREATE CONFIG')

    def test_d_CreateRemoveSecret(self):
        print('CREATE SECRET')
        secret = 'changelog-secret-' + str(random.randint(0, 10000))
        DockerSwarmTools.CreateSwarmSecret(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.md'), secret)
        DockerSwarmTools.RemoveSwarmSecret(secret)
        print('DONE CREATE SECRET')

    def test_e_CreateRemoveVolume(self):
        print('CREATE VOLUME')
        volume = 'test-volume-' + str(random.randint(0, 10000))
        DockerSwarmTools.CreateSwarmVolume(volume)
        DockerSwarmTools.RemoveSwarmVolume(volume)

        DockerSwarmTools.CreateSwarmVolume(volume, driver='local')
        DockerSwarmTools.RemoveSwarmVolume(volume)

        print('DONE CREATE VOLUME')

    def test_f_CreateRemoveStack(self):
        print('CREATE STACK')
        stack = 'test-stack-' + str(random.randint(0, 10000))
        DockerComposeTools.DockerComposeBuild([os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.yml')])
        DockerSwarmTools.DeployStack(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.yml'), stack)
        DockerSwarmTools.RemoveStack(stack)
        print('DONE CREATE STACK')


if __name__ == '__main__':
    unittest.main()