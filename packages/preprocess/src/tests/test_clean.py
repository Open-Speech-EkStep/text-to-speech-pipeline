import unittest
import sys
sys.path.append("../../src")
from scripts.clean import DataCleaner


class CleanTest(unittest.TestCase):

    def test_dashes_are_replaced_by_spaces(self):
        input_data = ['कैसे-कैसे', 'क्या-क्या', 'Innovative ideas के साथ 1234']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=True, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=False,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['कैसे कैसे', 'क्या क्या', 'Innovative ideas के साथ 1234']
        self.assertEqual(expected, received)

    def test_all_special_characters_and_extra_spaces_are_removed(self):
        input_data = ['! Innovative, ideas, के साथ 1234: food waste को बचाने के लिये प्रयोग किये हैं']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=True, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=False,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['Innovative ideas के साथ 1234 food waste को बचाने के लिये प्रयोग किये हैं']
        self.assertEqual(expected, received)

    # TODO:
    # in the test below, with replace_digits=False and digit_language=None, 1234 got removed as well.
    # it works when replace_digits=True and digit_language='en'
    def test_occurences_of_english_characters_are_removed(self):
        input_data = ['Innovative ideas के साथ 1234 food waste को बचाने के लिये प्रयोग किये हैं']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=True, remove_foreign_language_lines=False,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['के साथ को बचाने के लिये प्रयोग किये हैं']
        self.assertEqual(expected, received)

    def test_english_digits_are_not_removed_with_replace_digits_true(self):
        input_data = ['Innovative ideas के साथ 1234 food waste को बचाने के लिये प्रयोग किये हैं']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=True,
                                    digit_language='en',
                                    remove_foreign_language_occurences=True, remove_foreign_language_lines=False,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['के साथ 1234 को बचाने के लिये प्रयोग किये हैं']
        self.assertEqual(expected, received)

    def test_english_digits_are_converted_to_hindi(self):
        input_data = ['Innovative ideas के साथ 1234 food waste को बचाने के लिये प्रयोग किये हैं']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=True,
                                    digit_language='hi',
                                    remove_foreign_language_occurences=True, remove_foreign_language_lines=False,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['के साथ १२३४ को बचाने के लिये प्रयोग किये हैं']
        self.assertEqual(expected, received)

    # TODO:
    # remove_foreign_language_occurences = True is given priority over remove_foreign_language_lines=True
    # SO when these both are true, only occurences are removed
    def test_lines_with_foreign_characters_are_removed(self):
        input_data = ['Innovative ideas के साथ 1234 food waste को बचाने के लिये प्रयोग किये हैं',
                      'बचाने के लिये प्रयोग']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=True,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode=None,
                                    max_length_threshold=99999999,
                                    min_length_threshold=-1)
        expected = ['बचाने के लिये प्रयोग']
        self.assertEqual(expected, received)

    def test_filter_line_by_min_length_mode(self):
        # बचाने has a length == 5
        input_data = ['मन की बात उसमें में कई विषयों को लेकर के आता हूं', 'बचाने ']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=True,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode='min',
                                    max_length_threshold=99999999,
                                    min_length_threshold=5)
        expected = ['मन की बात उसमें में कई विषयों को लेकर के आता हूं']
        self.assertEqual(expected, received)

    def test_filter_line_by_max_length_mode(self):
        # बचाने has a length == 5
        input_data = ['मन की बात उसमें में कई विषयों को लेकर के आता हूं', 'बचाने ']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=True,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode='max',
                                    max_length_threshold=10,
                                    min_length_threshold=-1)
        expected = ['बचाने']
        self.assertEqual(expected, received)

    def test_filter_line_by_min_max_length_mode(self):
        # बचाने has a length == 5
        input_data = ['मन की बात उसमें में कई विषयों को लेकर के आता हूं', 'बचाने ']
        clean = DataCleaner('hi')
        received = clean.clean_data(input_data, remove_special_character=False, replace_digits=False,
                                    digit_language=None,
                                    remove_foreign_language_occurences=False, remove_foreign_language_lines=True,
                                    remove_extra_whitespace=True,
                                    filter_line_by_length_mode='min-max',
                                    max_length_threshold=10,
                                    min_length_threshold=4)
        expected = ['बचाने']
        self.assertEqual(expected, received)


if __name__ == '__main__':
    unittest.main()
