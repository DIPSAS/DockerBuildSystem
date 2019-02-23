import unittest
import os
from .. import TerminalTools

class TestTerminalTools(unittest.TestCase):

    def test_GetNumbersFromString(self):
        numbers = TerminalTools.GetNumbersFromString('per 123 k')
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0], 123)


if __name__ == '__main__':
    unittest.main()