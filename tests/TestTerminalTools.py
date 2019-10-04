import unittest
import os
from tests import TestTools
from DockerBuildSystem import TerminalTools

class TestTerminalTools(unittest.TestCase):

    def test_GetNumbersFromString(self):
        numbers = TerminalTools.GetNumbersFromString('per 123 k')
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0], 123)


    def test_ExecuteTerminalCommands(self):
        pyFile = os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'pythonSnippet.py')
        cmd = 'python ./{0}'.format(pyFile)
        TerminalTools.ExecuteTerminalCommands([cmd], True)


    def test_ExecuteTerminalCommandAndGetOutput(self):
        cmd = 'docker --version'
        version = TerminalTools.ExecuteTerminalCommandAndGetOutput(cmd)
        print(version)
        self.assertTrue('version' in str(version).lower())


    def test_ExportVariableToEnvironment(self):
        variable = 'variable'
        variableName = 'variableName'
        TerminalTools.ExportVariableToEnvironment(variable, variableName)
        self.assertTrue(variableName in os.environ)

    
    def test_LoadEnvironmentVariables(self):
        TerminalTools.LoadEnvironmentVariables(os.path.join(TestTools.TEST_SAMPLE_FOLDER, '.env'))
        self.assertTrue('REPO' in os.environ)


if __name__ == '__main__':
    unittest.main()