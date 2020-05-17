import glob
import os
import shutil

import numpy as np
import pandas as pd

import uuid


class DataSaver(object):

    def __init__(self):
        pass

    def __remove_duplicate_sentences(self, data, delimiter_text_file, mode, existing_directory):
        """Removes duplciate sentences in data as compared to file(s) in an existing_directory.
        
        Returns: array with unique sentences as compared to file(s) in an existing_directory.
        """
        if existing_directory:
            if not os.path.isdir(existing_directory):
                raise NotADirectoryError(existing_directory + "is not a directory!")

        if mode == 'local':
            unique_data = list(set(data))
            return unique_data

        search_string_csv = existing_directory + '/*.csv'
        search_string_txt = existing_directory + '/*.txt'

        paths_to_csv_files = glob.glob(search_string_csv)
        paths_to_txt_files = glob.glob(search_string_txt)

        existing_sentences = []

        if paths_to_csv_files:
            for path in paths_to_csv_files:
                df = pd.read_csv(path)
                columns = df.columns
                column_name = columns[0]
                # handling the condition where df.to_csv() is run with index=True to save the file.
                if len(columns) == 2 and columns[0] == 'Unnamed: 0':
                    column_name = columns[1]
                if len(columns) > 2:
                    raise ValueError("Number of columns cannot be greater than 2 (if the first column is index)")

                sentences = df[column_name].values
                existing_sentences.extend(sentences)

        if paths_to_txt_files:
            for path in paths_to_txt_files:
                with open(path) as file:
                    content = file.read()
                sentences = content.split(delimiter_text_file)
                existing_sentences.extend(sentences)

        unique_existing_sentences = len(np.unique(existing_sentences))
        unique_sentence_pos = []

        for i, sentence in enumerate(data):
            new_sentence = [sentence]
            total_unique_after_new_sentence = len(np.unique(existing_sentences + new_sentence))
            if total_unique_after_new_sentence > unique_existing_sentences:
                unique_sentence_pos.append(i)
        unique_data = []
        for pos in unique_sentence_pos:
            unique_data.append(data[pos])
        if len(unique_data) == unique_existing_sentences:
            unique_data = []

        return unique_data

    def __save_csv_to_disc(self, data, target_directory, file_name_or_prefix, one_sentence_per_file):

        file_type = 'csv'

        # saving one csv file with all the data
        if not one_sentence_per_file:
            file_name = file_name_or_prefix + '.' + file_type
            file_path = target_directory + '/' + file_name
            data = pd.DataFrame(data)
            data.to_csv(file_path, index=False)
            return

        # saving each sentence as a csv file 
        for i, sentence in enumerate(data):
            file_name = file_name_or_prefix + '_' + str(i + 1) + '.' + file_type
            file_path = target_directory + '/' + file_name
            content = pd.DataFrame([sentence])
            content.to_csv(file_path, index=False)
        return

    def __save_txt_to_disc(self, data, target_directory, file_name_or_prefix, one_sentence_per_file):

        file_type = 'txt'

        # saving one txt file with all the data
        if not one_sentence_per_file:
            file_name = file_name_or_prefix + '.' + file_type
            file_path = target_directory + '/' + file_name
            with open(file_path, 'w+') as file:
                content = '\n'.join(data)
                file.write(content)
            return

        # saving each sentence as a csv file 
        for i, sentence in enumerate(data):
            file_name = file_name_or_prefix + '_' + str(i + 1) + '.' + file_type
            file_path = target_directory + '/' + file_name
            with open(file_path, 'w+') as file:
                file.write(sentence)
        return

    def save_data(self, data, delimiter_text_file='\n', target_directory_for_saving='../../data/external',
                  file_type_for_saving='txt', directory_for_duplication_check=None, check_for_duplicacy=False,
                  file_name_for_saving=None,
                  one_sentence_per_file=False):
        """Finds unique sentences in data as compared to file(s) in an existing_directory and saves them. 
        
        Assumptions:
            1. if check for duplicacy is True and an existing directory is not given by user, the data is locally checked
               for unique sentences in itself.

        Files are saved only when:
            1. number of unique sentences > 0 (if duplicacy check is True).
        
        Args:
            data: numpy array of sentences.
            directory_for_duplication_check: (string) path to the directory against which the data is being checked for duplicacy.
            target_directory_for_saving: (string) path to the dir where files have to be saved
            delimiter_text_file: (string) delimiter to separate text file's content into sentences.  
            one_sentence_per_file: (Boolean) whether to save one sentence in each file or not 
            file_name_for_saving: (string) if the data is being stored in one file, this will be the file_name
                                 but if it is being stored as one sentence per file, this will be the prefix.
            file_type_for_saving: (string) can be 'txt' (default) or 'csv'.
            check_for_duplicacy: (Boolean) whether the data ti be saved has to be checked for duplicacy in sentences.
            mode : 'local' possible values [local, dir]

        Raises:
            NotADirectoryError: If existing_directory is not a directory.
            ValueError: If file other than 'txt' or 'csv' is entered.
            ValueError: If number of columns in csv file is > 1.
            
        Sample usage:
            sample_data = ['मन की बात उसमें में कई विषयों को लेकर के आता हूं।',
                            'कोरोनावायरस का मुकाबला कर रहे हैं जो हमारे फ्रंटलाइन सोल्जर्स है खास करके हमारी नर्सेज बहने हैं।',
                            'मुझसे नाराज भी होंगे कैसे-कैसे सब को घर में बंद कर रहे हो मैं आपकी दिक्कत है।']

            saveit = DataSaver()
            saveit.save_data(sample_data,
                             target_directory_for_saving='/Users/neerajchhimwal/Desktop',
                             file_type_for_saving='csv', check_for_duplicacy=False,
                             one_sentence_per_file=True)
        """

        if check_for_duplicacy:
            mode = 'local'
            if not directory_for_duplication_check:
                mode = 'local'
            else:
                mode = 'dir'
            data = self.__remove_duplicate_sentences(data=data, existing_directory=directory_for_duplication_check,
                                                     delimiter_text_file=delimiter_text_file, mode=mode)

        file_types = ['csv', 'txt']

        # throwing exceptions for invalid file type or directory name
        if not os.path.isdir(target_directory_for_saving):
            raise NotADirectoryError(target_directory_for_saving + " is not a directory!")

        if file_type_for_saving not in file_types:
            raise ValueError('File type not supported. csv or txt files only.')

        # using uuid to create a file name, if not given by user
        if not file_name_for_saving:
            file_name_for_saving = str(uuid.uuid4())

        if file_type_for_saving == 'csv':
            self.__save_csv_to_disc(data=data, target_directory=target_directory_for_saving,
                                    file_name_or_prefix=file_name_for_saving,
                                    one_sentence_per_file=one_sentence_per_file)

        if file_type_for_saving == 'txt':
            self.__save_txt_to_disc(data=data, target_directory=target_directory_for_saving,
                                    file_name_or_prefix=file_name_for_saving,
                                    one_sentence_per_file=one_sentence_per_file)

        return
