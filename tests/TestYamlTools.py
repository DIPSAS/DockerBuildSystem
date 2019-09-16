import unittest
import os
from tests import TestTools
from DockerBuildSystem import YamlTools

class TestYamlTools(unittest.TestCase):

    def test_GetYamlData(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()

        yamlData = YamlTools.GetYamlData(['docker-compose.yml'])
        self.assertTrue('my-service' in YamlTools.GetProperties('services', yamlData))
        
        os.chdir(cwd)

    def test_ReplaceEnvironmentVariablesMatches(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()

        os.environ['TEST_KEY'] = 'test-value'
        yamlString = 'abc ${TEST_KEY} def'
        yamlString = YamlTools.ReplaceEnvironmentVariablesMatches(yamlString)
        self.assertFalse('${TEST_KEY}' in yamlString)
        self.assertTrue('test-value' in yamlString)
        
        os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()