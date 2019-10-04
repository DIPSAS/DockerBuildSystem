import unittest
import os
from tests import TestTools
from DockerBuildSystem import YamlTools

class TestYamlTools(unittest.TestCase):

    def test_GetYamlData(self):
        yamlData = YamlTools.GetYamlData([os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'docker-compose.yml')])
        self.assertTrue('my-service' in YamlTools.GetProperties('services', yamlData))


    def test_ReplaceEnvironmentVariablesMatches(self):
        os.environ['TEST_KEY'] = 'test-value'
        yamlString = 'abc ${TEST_KEY} def'
        yamlString = YamlTools.ReplaceEnvironmentVariablesMatches(yamlString)
        self.assertFalse('${TEST_KEY}' in yamlString)
        self.assertTrue('test-value' in yamlString)


if __name__ == '__main__':
    unittest.main()