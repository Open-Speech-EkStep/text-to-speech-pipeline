import pandas as pd
import glob
import numpy as np

class DataLoader(object):
    def __init__(self):
        pass

    def __read_data_from_csv(self, file_path, column_name, header, nrows):
        df = []
        
        if header is None:
            if nrows is None:
                df = pd.read_csv(file_path)
            else:
                df = pd.read_csv(file_path, nrows = nrows)
        else:
            if nrows is None:
                df = pd.read_csv(file_path, header = header)
            else:
                df = pd.read_csv(file_path, header = header, nrows= nrows)
        
        array_lines = np.array([])
        if column_name is not None:
            array_lines = df.loc[:, column_name].values
        else:
            array_lines = df.iloc[:, 0].values
            
        return array_lines
    
    def __read_data_from_txt(self, file_path, delimiter):
        array_lines = []
#        file_contents = []
        
        with open(file_path , "r", encoding='utf-8') as file:
            array_lines = file.readlines()
            
        #array_lines = file_contents.split(delimiter)
        return array_lines
    
    def __read_data_from_dir(self, file_path, column_name, 
                             header, delimiter, nrows):
        array_lines = []
        
        
        search_string_txt = file_path + "/*.txt"
        search_string_csv = file_path + "/*.csv"
        
        list_paths_txt = glob.glob(search_string_txt)
        list_paths_csv = glob.glob(search_string_csv)
        
        print("Total Number of files to found: ", len(list_paths_csv) + len(list_paths_txt))
        if list_paths_txt:
            for path_txt in list_paths_txt:
                array_lines.extend(self.__read_data_from_txt(path_txt, delimiter))
            
        if list_paths_csv:
            for path_csv in list_paths_csv:
                array_lines.extend(self.__read_data_from_csv(path_csv, column_name, header, nrows))
        
        return array_lines
            
    
    def load_data(self, path, file_type = 'txt', delimiter ='\n',
                             column_name = None, header = None, nrows = None):
        file_types = ['txt', 'csv', 'dir']
        
        if file_type not in file_types:
            return
        
        arr_lines = []
        
        if file_type == 'csv':
            arr_lines = self.__read_data_from_csv(path, column_name, header, nrows)
        
        if file_type == 'txt':
            arr_lines = self.__read_data_from_txt(path, delimiter)
            
        if(file_type == 'dir'):
            arr_lines = self.__read_data_from_dir(path, column_name, header, delimiter, nrows)
        
        #arr_lines = np.array(arr_lines)
        print("Return type is ", type(arr_lines))
        return arr_lines

