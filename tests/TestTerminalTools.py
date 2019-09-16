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
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        cmd = 'python ./pythonSnippet.py'
        TerminalTools.ExecuteTerminalCommands([cmd], True)
        os.chdir(cwd)


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
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        TerminalTools.LoadEnvironmentVariables('.env')
        self.assertTrue('REPO' in os.environ)
        os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()