import unittest
import sys
sys.path.append("../../src")
from scripts.save import DataSaver
import os
import pandas as pd


class DeduplicateSaveTest(unittest.TestCase):

    def test_raise_error_when_wrong_path_is_entered(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        ds = DataSaver()

        with self.assertRaises(NotADirectoryError) as context:
            ds.save_data(input_data, target_directory_for_saving='../../data/proc/')
        self.assertTrue('../../data/proc/ is not a directory!' in str(context.exception))

    def test_raise_value_error_for_files_other_than_txt_or_csv(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        ds = DataSaver()

        with self.assertRaises(ValueError) as context:
            ds.save_data(input_data, target_directory_for_saving='../../data/processed/', file_type_for_saving='doc')
        self.assertTrue('File type not supported. csv or txt files only.' in str(context.exception))

    def test_file_is_saved_even_if_directory_name_is_given_without_terminal_slash(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        ds = DataSaver()

        ds.save_data(input_data, target_directory_for_saving='../../data/external',
                     file_type_for_saving='txt', file_name_for_saving='test_file')
        with open('../../data/external/test_file.txt') as f:
            content = f.read()

        os.remove('../../data/external/test_file.txt')
        self.assertEqual(input_data[0], content)

    def test_file_name_is_the_same_as_that_provided_by_user(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        ds = DataSaver()

        ds.save_data(input_data, target_directory_for_saving='../../data/external',
                     file_type_for_saving='txt', file_name_for_saving='test_file')

        all_files = ' '.join(os.listdir('../../data/external'))
        os.remove('../../data/external/test_file.txt')
        self.assertTrue('test_file.txt' in all_files)


    def test_only_unique_lines_are_saved(self):
        # '../../data/external' has test.txt and our input data has one duplicate line from test.txt
        # second line is a duplicate. it should be removed during duplicacy check

        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।',
                      'मन की बात उसमें में कई विषयों को लेकर के आता हूं।',
                      'कोरोनावायरस वीक महामारी']
        ds = DataSaver()
        ds.save_data(input_data, target_directory_for_saving='../../data/external', directory_for_duplication_check='../../data/external',
                     file_type_for_saving='txt', file_name_for_saving='test_file', check_for_duplicacy=True)

        with open('../../data/external/test_file.txt') as f:
            content = f.read()
        expected = "कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।\nमन की बात उसमें में कई विषयों को लेकर के आता हूं।\nकोरोनावायरस वीक महामारी"
        self.assertEqual(expected, content)
        os.remove('../../data/external/test_file.txt')

    def test_csv_file_is_saved(self):
        input_data = ['कैसे-कैसे Innovative ideas के साथ food waste को बचाने के लिये क्या-क्या प्रयोग किये हैं।',
                      'कोरोनावायरस वीक महामारी']
        ds = DataSaver()

        ds.save_data(input_data, target_directory_for_saving='../../data/external',
                     file_type_for_saving='csv', file_name_for_saving='test_file')
        content = pd.read_csv('../../data/external/test_file.csv')
        sentences = content[content.columns[0]].values
        expected = ''.join(input_data)
        received = ''.join(sentences)
        os.remove('../../data/external/test_file.csv')
        self.assertEqual(expected, received)

    def test_unique_lines_from_data_are_saved(self):
        input_data = ['कैसे-कैसे बचाने के लिये क्या-क्या प्रयोग किये हैं।',
                      'कोरोनावायरस वीक महामारी',
                      'कैसे-कैसे बचाने के लिये क्या-क्या प्रयोग किये हैं।']
        ds = DataSaver()

        ds.save_data(input_data, target_directory_for_saving='../../data/external',
                     file_type_for_saving='csv', file_name_for_saving='test_file', check_for_duplicacy=True)
        content = pd.read_csv('../../data/external/test_file.csv')
        strings = content[content.columns[0]].values
        sentences = []
        for i in strings:
            sentences.append(i)
        expected = ['कैसे-कैसे बचाने के लिये क्या-क्या प्रयोग किये हैं।', 'कोरोनावायरस वीक महामारी']
        # received = ' '.join(sentences)
        os.remove('../../data/external/test_file.csv')
        self.assertTrue(all([i in sentences for i in expected]))


if __name__ == '__main__':
    unittest.main()
