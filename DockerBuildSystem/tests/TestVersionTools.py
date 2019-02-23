import unittest
import os
from . import TestTools
from .. import VersionTools

class TestVersionTools(unittest.TestCase):

    def test_GetVersionFromChangelog(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        version = VersionTools.GetVersionFromChangelog('CHANGELOG.md')
        self.assertEqual(version, '1.0.0')
        os.chdir(cwd)

    def test_ExportVersionFromChangelogToEnvironment(self):
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        VersionTools.ExportVersionFromChangelogToEnvironment('CHANGELOG.md', 'VERSION')
        self.assertEqual(os.environ['VERSION'], '1.0.0')
        os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()