import unittest
import os
from tests import TestTools
from DockerBuildSystem import VersionTools

class TestVersionTools(unittest.TestCase):

    def test_GetVersionFromChangelog(self):
        
        version = VersionTools.GetVersionFromChangelog(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.md'))
        self.assertEqual(version, '1.0.0')
        version = VersionTools.GetVersionFromChangelog(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.v2.md'))
        self.assertEqual(version, '1.0.0')


    def test_ExportVersionFromChangelogToEnvironment(self):
        
        os.environ.clear()
        VersionTools.ExportVersionFromChangelogToEnvironment(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.md'), 'VERSION')
        self.assertEqual(os.environ['VERSION'], '1.0.0')
        
        os.environ.clear()
        VersionTools.ExportVersionFromChangelogToEnvironment(os.path.join(TestTools.TEST_SAMPLE_FOLDER, 'CHANGELOG.v2.md'), 'VERSION')
        self.assertEqual(os.environ['VERSION'], '1.0.0')


if __name__ == '__main__':
    unittest.main()