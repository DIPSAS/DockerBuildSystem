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
        DockerImageTools.CopyFromContainerToHost(TEST_IMAGE, 'src/', 'output/')
        os.chdir(cwd)
        print('DONE COPY FROM CONTAINER TO HOST')


if __name__ == '__main__':
    unittest.main()