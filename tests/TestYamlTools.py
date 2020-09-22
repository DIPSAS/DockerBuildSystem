import unittest
import os
from tests import TestTools
from DockerBuildSystem import YamlTools, TerminalTools

class TestYamlTools(unittest.TestCase):

    def test_GetYamlData(self):
        TerminalTools.LoadEnvironmentVariables(os.path.join(TestTools.TEST_SAMPLE_FOLDER, '.env'))
        yamlData = YamlTools.GetYamlData([os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.yml')])
        self.assertTrue('my-service' in YamlTools.GetProperties('services', yamlData))
        self.assertTrue('my_repo/my.service:1.0.0' == yamlData['services']['my-service']['image'])
        self.assertTrue('env_value' == yamlData['services']['my-service']['environment']['SOME_VARIABLE'])
        self.assertTrue('default_value' == yamlData['services']['my-service']['environment']['SOME_VARIABLE_2'])


    def test_GetMergedYamlData(self):
        TerminalTools.LoadEnvironmentVariables(os.path.join(TestTools.TEST_SAMPLE_FOLDER, '.env'))
        files = [os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.yml'), os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.override.yml')]
        yamlData = YamlTools.GetYamlData(files)
        self.assertTrue('my-service' in YamlTools.GetProperties('services', yamlData))
        self.assertTrue('my_repo/my.service:1.0.0' == yamlData['services']['my-service']['image'])
        self.assertTrue('new-my-service' == yamlData['services']['my-service']['container_name'])
        self.assertTrue(len(yamlData['services']['my-service']['networks']) == 2)
        self.assertTrue('new_network' in yamlData['services']['my-service']['networks'])
        self.assertTrue('backend_network' in yamlData['services']['my-service']['networks'])
        YamlTools.DumpYamlDataToFile(yamlData, os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'output', 'docker-compose.merged.yml'))


    def test_ReplaceEnvironmentVariablesMatches(self):
        os.environ['TEST_KEY'] = 'test-value'
        yamlString = 'abc ${TEST_KEY} def'
        yamlString = YamlTools.ReplaceEnvironmentVariablesMatches(yamlString)
        self.assertFalse('${TEST_KEY}' in yamlString)
        self.assertTrue('test-value' in yamlString)


if __name__ == '__main__':
    unittest.main()