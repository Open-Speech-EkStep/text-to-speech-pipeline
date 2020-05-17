import unittest
import sys
sys.path.append("../../src")
from scripts.tokenizer import DataTokenizer


class TokenizeTest(unittest.TestCase):

    def test_a_string_with_one_sentence_stays_unchanged(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']

        tok = DataTokenizer(language='hi')
        self.assertEqual(['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।'],
                         tok.tokenize_data(input_data))

    def test_a_string_with_two_sentences_is_tokenized_to_two_sentences(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं। स्वतंत्रता']

        tok = DataTokenizer(language='hi')
        self.assertEqual(
            ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।', 'स्वतंत्रता'],
            tok.tokenize_data(input_data))

    def test_a_string_with_one_sentence_and_trailing_spaces_is_tokenized(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।    ']
        tok = DataTokenizer(language='hi')
        self.assertEqual(['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।'],
                         tok.tokenize_data(input_data))

    def test_a_string_with_one_sentence_and_initial_spaces_is_tokenized(self):
        input_data = ['          कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        tok = DataTokenizer(language='hi')
        self.assertEqual(['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।'],
                         tok.tokenize_data(input_data))

    def test_tokenizer_with_strings_with_multiple_lines(self):
        input_data = ['कैसे-कैसे Innovative ideas। food waste को बचाने के लिये।', 'क्या-क्या प्रयोग किये हैं।']
        tok = DataTokenizer(language='hi')
        expected = ['कैसे-कैसे Innovative ideas।', 'food waste को बचाने के लिये।', 'क्या-क्या प्रयोग किये हैं।']
        self.assertEqual(expected, tok.tokenize_data(input_data))


if __name__ == '__main__':
    unittest.main()
