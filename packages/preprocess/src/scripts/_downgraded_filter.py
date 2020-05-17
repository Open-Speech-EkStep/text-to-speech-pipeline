
import re
import numpy as np

class DataFilter(object):
    def __init__(self, language, pattern):
        self.language = language
        self.pattern = pattern
        self.base_pattern = re.compile(pattern)
        self.re_spaces = re.compile('\s+')
    
    def __common_remove_extra_spaces(self, data):
        data = re.sub(self.re_spaces, ' ', str.strip(data))
        return data

    def __common_remove_spaces(self, data):
        data = re.sub(self.re_spaces, '', str.strip(data))
        return data

    def __common_remove_foreign_language(self, data):
        return re.sub(self.pattern, '', data)

    def __update_regular_expression(self):
        self.pattern = re.compile('[' + self.pattern[2:])

    def __remove_lines(self, data):
        self.__update_regular_expression()
        valid_lines = []
        for line in data:
            violation = self.__common_remove_foreign_language(line)
            violation = self.__common_remove_spaces(str.strip(violation))
            
            if len(violation) == 0:
                line_without_spaces = self.__common_remove_extra_spaces(line)
                valid_lines.append(line_without_spaces)
        return valid_lines


    def filter_data(self, data, remove_occurence = True, remove_lines = False):
        filtered_data = []
        if remove_lines:
            filtered_data = self.__remove_lines(data)
            return np.array(filtered_data)
        
        
        for line in data:
            filtered_line = self.__common_remove_foreign_language(line)
            filtered_data.append(self.__common_remove_extra_spaces(filtered_line))

        return np.array(filtered_data)

