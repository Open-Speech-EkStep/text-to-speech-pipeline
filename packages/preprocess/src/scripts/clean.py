import re
import numpy as np
import string

class DataCleaner(object):
    
 
    def __init__(self, language):
        self.language = language
        if(language == 'hi'):
            self.__set_regular_expressions_for_hindi()
        self.__set_common_regular_expressions()
    
    def __common_replace_dash_with_space(self, data):
        return re.sub(self.re_dash, ' ', data)
    
    def __common_special_character_removal(self, data):
        return re.sub(self.re_special_character, '', self.__common_replace_dash_with_space(data))

    def __common_remove_extra_spaces(self, data):
        return re.sub(self.re_spaces, ' ', data.strip())
   
    def __set_common_regular_expressions(self):
        self.re_dash = re.compile('[-]+')
        self.re_special_character = re.compile('[!-/:-@[-`{-~}]+')
        self.re_spaces = re.compile(r'\s+')

    def __common_remove_spaces(self, data):
        data = re.sub(self.re_spaces, '', str.strip(data))
        return data

    def __common_remove_foreign_language(self, data):
        return re.sub(self.pattern, '', data)



    def __set_regular_expressions_for_hindi(self):
        self.base_pattern = '[^ ँ-नप-रल-ळव-ह़-्ॐॠ-ॡ।-॥०-९]+'
        self.pattern = '[^ ँ-नप-रल-ळव-ह़-्ॐॠ-ॡ।-॥०-९]+'
        self.number_set_hindi = {0 : '०' , '1': '१', '2': '२', '3':'३', '4': '४', '5': '५', '6':'६', '7':'७', '8':'८', '9':'९'}

     
    def __get_updated_regular_expression(self):
        return '[' + self.pattern[2:]

    
    def __get_digit_language(self, digit_language):
        if digit_language is None:
            return self.language
        else:
            if digit_language == self.language:
                return digit_language 
        return 'en'
    
    def __remove_foreign_lines(self, data):
        violation_pattern = re.compile('[' + self.pattern[2:])
        valid_lines = []
        for line in data:
            local_line = line
            violation = re.sub(violation_pattern, '', local_line)
            violation = self.__common_remove_spaces(str.strip(violation))
            
            if len(violation) == 0:
                #line_without_spaces = self.__common_remove_extra_spaces(line)
                valid_lines.append(line)
        return valid_lines

    def __remove_extra_whitespaces(self, data):
        processed_data = []
        whitespace_pattern = re.compile(r"\s+")
        for line in data:
            data_ = re.sub(whitespace_pattern, ' ', line)
            stripped = data_.strip()
            if stripped:
                processed_data.append(stripped)
        return processed_data

    def __remove_foreign_occurences(self, data):
        processed_data = []
        for line in data:
            processed_data.append(self.__common_remove_foreign_language(line))
        return processed_data

    def __replace_digits_for_hindi(self, data, digit_language):
        
        self.pattern = self.base_pattern
        processed_data = []
        if digit_language == 'en':
            # hindi -> english
            
            for line in data:
                local_line = line
                for key, value in self.number_set_hindi.items():
                    local_line = local_line.replace(str(value), str(key))
                processed_data.append(local_line)
            self.pattern = self.pattern[:-5] + '0-9' + ']+'
            return processed_data
        
        #english -> hindi
        for line in data:
            local_line = line
            for key, value in self.number_set_hindi.items():
                local_line = local_line.replace(str(key), str(value))
            processed_data.append(local_line)
        
        return processed_data
               
   
    def __clean_special_characters(self, data):
        processed_data = []
        #dash_regular_expression = re.compile('[-]+')
        chars = re.escape(string.punctuation)
        special_character_regular_expression = re.compile(r'[%s]+' % chars)
        #special_character_regular_expression = re.compile('[!-/:-@[-`{-~}]+')
        for line in data:
            #data_ = re.sub(dash_regular_expression, ' ', line)


            processed_data.append( re.sub(special_character_regular_expression, '', line.replace('-' , ' ')) )

        return processed_data

    def __filter_according_to_minimum_length(self, single_record, min_threshold):
        if len(single_record) > min_threshold:
            return True
        return False

    def __filter_according_to_maximum_length(self, single_record, max_threshold):
        if len(single_record) < max_threshold:
            return True
        return False

    def __filter_sentences__according_to_length(self, data, mode, min_threshold, max_threshold) :
        filtered_lines = []

        if mode == 'min':
            for line in data:
                if self.__filter_according_to_minimum_length(line, min_threshold):
                    filtered_lines.append(line)
        if mode == 'max':
            for line in data:
                if self.__filter_according_to_maximum_length(line, max_threshold):
                    filtered_lines.append(line)
        if mode == 'min-max':
            for line in data:
                if self.__filter_according_to_minimum_length(line, min_threshold) and \
                    self.__filter_according_to_maximum_length(line, max_threshold):
                    filtered_lines.append(line)
        return filtered_lines    




    def clean_data(self, data, 
                    remove_special_character = True, replace_digits = False, digit_language = None,
                    remove_foreign_language_occurences = True, remove_foreign_language_lines = False,
                    remove_extra_whitespace = True,
                    filter_line_by_length_mode = None,
                    max_length_threshold = 99999999,
                    min_length_threshold = -1):
        digit_language = self.__get_digit_language(digit_language)
        
        processed_data = data
        
        if self.language == 'hi':
            if remove_special_character: ### add special characters in regular expression
                print("Removing Special Characters")
                processed_data = self.__clean_special_characters(processed_data)
                

            if replace_digits:
                print("Replacing Digits")
                processed_data = self.__replace_digits_for_hindi(processed_data, digit_language)

            if remove_foreign_language_occurences:
                print("Removing Foreign Language Occurences")
                processed_data = self.__remove_foreign_occurences(processed_data)
            elif remove_foreign_language_lines:
                print("Removing Foreign Language Lines")
                processed_data = self.__remove_foreign_lines(processed_data)
            
            if remove_extra_whitespace:
                print("Removing Whitespace")
                processed_data = self.__remove_extra_whitespaces(processed_data)
                print("Done with whitespace")

            if filter_line_by_length_mode is not None:
                print("Removing Lines with Length Threshold")
                processed_data = self.__filter_sentences__according_to_length(processed_data, filter_line_by_length_mode,
                                                                             min_length_threshold, max_length_threshold)
                
        return processed_data
        
