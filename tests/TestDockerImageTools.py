import unittest
import random
import os
from tests import TestTools
from DockerBuildSystem import DockerImageTools

TEST_IMAGE = 'test.image'
TEST_CONTAINER_NAME = 'test-container-' + str(random.randint(0, 100000))

class TestDockerImageTools(unittest.TestCase): 

    def test_a_BuildImage(self):
        print('BUILD IMAGE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerImageTools.BuildImage(TEST_IMAGE)
        os.chdir(cwd)
        print('DONE BUILD IMAGE')

    def test_b_RunImage(self):
        print('RUN IMAGE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerImageTools.RunImage(TEST_IMAGE, '--name ' + TEST_CONTAINER_NAME)
        os.chdir(cwd)
        print('DONE RUN IMAGE')

    def test_c_GetContainerExitCode(self):
        print('CONTAINER EXIT CODE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        exitCode = DockerImageTools.GetContainerExitCode(TEST_CONTAINER_NAME)
        self.assertEqual(exitCode, 0)
        os.chdir(cwd)
        print('DONE CONTAINER EXIT CODE')

    def test_d_GetContainerRunningCode(self):
        print('CONTAINER RUNNING CODE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        running = DockerImageTools.GetContainerRunningCode(TEST_CONTAINER_NAME)
        self.assertEqual(running, False)
        os.chdir(cwd)
        print('DONE CONTAINER RUNNING CODE')

    def test_e_TagImage(self):
        print('TAG IMAGE')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerImageTools.TagImage(TEST_IMAGE, TEST_IMAGE + ':1.0.0')
        os.chdir(cwd)
        print('DONE TAG IMAGE')

    def test_f_CopyFromContainerToHost(self):
        print('COPY FROM CONTAINER TO HOST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        DockerImageTools.CopyFromContainerToHost(TEST_CONTAINER_NAME, 'src/', 'output/')
        self.assertTrue(os.path.isfile('output/src/pythonSnippet.py'))
        os.chdir(cwd)
        print('DONE COPY FROM CONTAINER TO HOST')

    def test_g_GetImageRepoDigest(self):
        print('GET IMAGE REPO DIGEST')
        DockerImageTools.PullImage('nginx')
        repoDigest = DockerImageTools.GetImageRepoDigest('nginx')
        self.assertTrue('nginx@sha256:' in repoDigest)
        self.assertFalse('\n' in repoDigest)
        print('DONE GET IMAGE REPO DIGEST')

    def test_h_GetImageLabel(self):
        print('GET IMAGE LABEL')
        labelValue = DockerImageTools.GetImageLabel(TEST_IMAGE, 'owner')
        self.assertEqual('example owner', labelValue)

        labelValue = DockerImageTools.GetImageLabel(TEST_IMAGE, 'none_existent')
        self.assertEqual('<no value>', labelValue)
        print('DONE GET IMAGE LABEL')

    def test_i_CheckImageLabelExists(self):
        print('CHECK IMAGE LABEL EXISTS')
        exists = DockerImageTools.CheckImageLabelExists(TEST_IMAGE, 'owner')
        self.assertTrue(exists)

        exists = DockerImageTools.CheckImageLabelExists(TEST_IMAGE, 'none_existent')
        self.assertFalse(exists)
        print('DONE CHECK IMAGE LABEL EXISTS')

    def test_j_GetImageId(self):
        print('GET IMAGE ID')
        imageId = DockerImageTools.GetImageId(TEST_IMAGE)
        self.assertTrue('sha256:' in imageId)
        print('DONE GET IMAGE ID')

    def test_k_GetImageInfo(self):
        print('GET IMAGE INFO')
        jsonInfo = DockerImageTools.GetImageInfo(TEST_IMAGE)
        self.assertTrue('sha256:' in jsonInfo['Id'])
        print('DONE GET IMAGE INFO')

    def test_l_GetContainerInfo(self):
        print('GET CONTAINER INFO')
        jsonInfo = DockerImageTools.GetContainerInfo(TEST_CONTAINER_NAME)
        self.assertTrue(len(jsonInfo['Id']) > 0)
        print('DONE GET CONTAINER INFO')

if __name__ == '__main__':
    unittest.main()