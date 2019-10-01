import unittest
import random
import os
from tests import TestTools
from DockerBuildSystem import DockerComposeTools, YamlTools, DockerImageTools

TEST_IMAGE = 'test.image'
TEST_CONTAINER_NAME = 'test-container-' + str(random.randint(0, 100000))

class TestDockerComposeTools(unittest.TestCase):

    def test_a_ComposeBuild(self):
        print('COMPOSE BUILD')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.DockerComposeBuild(['docker-compose.yml'])
        os.chdir(cwd)
        print('DONE COMPOSE BUILD')

    def test_b_ComposeUp(self):
        print('COMPOSE RUN')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.DockerComposeUp(['docker-compose.yml'])
        os.chdir(cwd)
        print('DONE COMPOSE RUN')

    def test_c_ComposeRemove(self):
        print('COMPOSE REMOVE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.DockerComposeRemove(['docker-compose.yml'])
        os.chdir(cwd)
        print('DONE COMPOSE REMOVE')

    def test_d_TagImages(self):
        print('COMPOSE TAG')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.TagImages('docker-compose.yml', '1.0.0')
        os.chdir(cwd)
        print('DONE COMPOSE TAG')

    def test_e_SaveImages(self):
        print('COMPOSE SAVE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        folder = os.path.join(os.getcwd(), 'output')
        print(folder)
        DockerComposeTools.SaveImages('docker-compose.yml', folder)
        self.assertTrue(os.path.isfile(os.path.join(folder, 'my.service-tag.tar')))
        os.chdir(cwd)
        print('DONE COMPOSE SAVE')

    def test_f_ComposeTest(self):
        print('COMPOSE TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerComposeTools.ExecuteComposeTests(['docker-compose.yml'], ['my-service'])
        os.chdir(cwd)
        print('DONE COMPOSE TEST')

    def test_f_AddDigestsToImageTags(self):
        print('COMPOSE ADD DIGESTS')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerImageTools.PullImage('nginx')
        os.makedirs('output', exist_ok=True)
        DockerComposeTools.AddDigestsToImageTags(['docker-compose.yml'], 'output/docker-compose.digests.yml')
        yamlData = YamlTools.GetYamlData(['output/docker-compose.digests.yml'])
        for service in yamlData['services']:
            if 'my.service' in yamlData['services'][service]['image']:
                self.assertEqual('my_repo/my.service:tag', yamlData['services'][service]['image'])
            else:
                self.assertTrue('nginx@sha256:' in yamlData['services'][service]['image'])
        os.chdir(cwd)
        print('DONE COMPOSE ADD DIGESTS')


if __name__ == '__main__':
    unittest.main()