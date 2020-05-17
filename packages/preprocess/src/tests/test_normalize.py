import unittest
import sys
sys.path.append("../../src")
from scripts.normalize import DataNormalizer


class NormalizeTest(unittest.TestCase):
    def test_a_single_line_is_normalized(self):
        norm = DataNormalizer('hi')
        input_data = ['क्या-क्या प्रयोग किये हैं|']
        expected = ['क्या-क्या प्रयोग किये हैं।']
        self.assertEqual(expected, norm.normalize_data(input_data))

    def test_multiple_lines_are_normalized(self):
        norm = DataNormalizer('hi')
        input_data = ['क्या प्रयोग किये हैं|', 'मन की बात | उसमें में कई विषयों को लेकर के आता हूं।']
        expected = ['क्या प्रयोग किये हैं।', 'मन की बात । उसमें में कई विषयों को लेकर के आता हूं।']
        self.assertEqual(expected, norm.normalize_data(input_data))


if __name__ == '__main__':
    unittest.main()
