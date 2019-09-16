import unittest
import os
from tests import TestTools
from DockerBuildSystem import VersionTools

class TestVersionTools(unittest.TestCase):

    def test_GetVersionFromChangelog(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        
        version = VersionTools.GetVersionFromChangelog('CHANGELOG.md')
        self.assertEqual(version, '1.0.0')
        version = VersionTools.GetVersionFromChangelog('CHANGELOG.v2.md')
        self.assertEqual(version, '1.0.0')
        
        os.chdir(cwd)

    def test_ExportVersionFromChangelogToEnvironment(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        
        os.environ.clear()
        VersionTools.ExportVersionFromChangelogToEnvironment('CHANGELOG.md', 'VERSION')
        self.assertEqual(os.environ['VERSION'], '1.0.0')
        
        os.environ.clear()
        VersionTools.ExportVersionFromChangelogToEnvironment('CHANGELOG.v2.md', 'VERSION')
        self.assertEqual(os.environ['VERSION'], '1.0.0')
        
        os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()