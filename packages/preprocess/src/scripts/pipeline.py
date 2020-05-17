from loader import DataLoader
from normalize import DataNormalizer
from tokenizer import DataTokenizer
from clean import DataCleaner
from save import DataSaver
from gcs_operations import CloudStorageOperations
from datetime import datetime
import os
import yaml
import time
import sys




class Pipeline(object):
    def __init__(self, language):
        self.language = language

    def _common_pipeline(self, path, file_type, delimiter, column_name, header, nrows):
        loader = DataLoader()
        data =  loader.load_data(path, file_type=file_type, delimiter=delimiter,
                                column_name=column_name, header=header, nrows=nrows)
        del loader
        return data

    def _run_saver(self, data, delimiter_text_file, file_type_for_saving,
                   target_directory_for_saving, file_name_for_saving, one_sentence_per_file,
                   check_for_duplicacy, directory_for_duplication_check):
        saver = DataSaver()
        saver.save_data(data, directory_for_duplication_check=directory_for_duplication_check,
                        delimiter_text_file=delimiter_text_file,
                        file_type_for_saving=file_type_for_saving,
                        target_directory_for_saving=target_directory_for_saving,
                        file_name_for_saving=file_name_for_saving,
                        one_sentence_per_file=one_sentence_per_file, check_for_duplicacy=check_for_duplicacy)


class HindiPipeline(Pipeline):
    def __init__(self):
        Pipeline.__init__(self, "hi")

    def __run_normalizer(self, data):
        normalizer = DataNormalizer(self.language)
        processed_data = normalizer.normalize_data(data)
        del normalizer
        return processed_data

    def __run_tokenizer(self, data):
        tokenizer = DataTokenizer(self.language)
        processed_data = tokenizer.tokenize_data(data)
        del tokenizer
        return processed_data

    def __run_cleaner(self, data, remove_special_character,
                      replace_digits, digit_language,
                      remove_foreign_language_occurences,
                      remove_foreign_language_lines,
                      remove_extra_whitespace,
                      filter_line_by_length_mode,
                      max_length_threshold,
                      min_length_threshold):

        cleaner = DataCleaner(self.language)
        cleaned_lines = cleaner.clean_data(data, remove_special_character=remove_special_character,
                                           replace_digits=replace_digits,
                                           digit_language=digit_language,
                                           remove_foreign_language_occurences=remove_foreign_language_occurences,
                                           remove_foreign_language_lines=remove_foreign_language_lines,
                                           remove_extra_whitespace=remove_extra_whitespace,
                                           filter_line_by_length_mode=filter_line_by_length_mode,
                                           max_length_threshold=max_length_threshold,
                                           min_length_threshold=min_length_threshold)

        del cleaner
        return cleaned_lines

    def __load_yaml_file(self, path):
        read_dict = {}
        with open(path, 'r') as file:
            read_dict = yaml.load(file)
        return read_dict

    def log(self, data, filename, msg):
        with open(filename, "a+", encoding='utf-8') as file:
            file.writelines(msg)
            file.write(";".join(data))
            file.write("\n------------------------------\n")    

    def generate_batchid(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def fit(self, yaml_file_path,bucket_name,current_work_dir):
        ## specify default arguments
        print("Starting")

        pipeline_start_time = time.time()
        read_dict = self.__load_yaml_file(yaml_file_path)

        args_loader = read_dict['loader']
        args_normalizer  = read_dict['normalizer']
        args_tokenizer = read_dict['tokenizer']
        args_cleaner = read_dict['cleaner']
        args_saver = read_dict['saver']
        start_time_loader = time.time()

        obj_gcsops = CloudStorageOperations()
        #Create local directory if not exists
        obj_gcsops.make_directories(path=os.path.join(current_work_dir,args_saver['target_directory_for_saving']))

        # Download raw data from GCS to local
        if(args_loader['file_type'] == "dir"):
            obj_gcsops.download_to_local(bucket_name=bucket_name, source_blob_name=args_loader['raw_tobeprocessed_path'],
                                        destination=os.path.join(current_work_dir,args_loader['raw_tobeprocessed_path']),
                                        is_directory=True,exclude_extn=args_loader['exclude_extn'])
        else:
            obj_gcsops.download_to_local(bucket_name=bucket_name,
                                         source_blob_name=args_loader['raw_tobeprocessed_path'],
                                         destination=os.path.join(current_work_dir, args_loader['raw_tobeprocessed_path']),
                                         is_directory=False)

        arr_lines = self._common_pipeline(path = args_loader['raw_tobeprocessed_path'],
                                        file_type = args_loader['file_type'], 
                                        delimiter = args_loader['delimiter'],
                                        column_name = args_loader['column_name'],
                                        header = args_loader['header'], nrows=args_loader['nrows'])
        end_time_loader = time.time()

        print("Loader took ", end_time_loader - start_time_loader, " to load  ", len(arr_lines))
        
        ### divide arrray into 10 equal blocks

        #for i in range(10):
        print("Number of lines", len(arr_lines))

        if args_normalizer['enabled']:
            print("Starting Normalization")
            
            arr_lines = self.__run_normalizer(arr_lines)
            
            
            
        if(args_tokenizer['enabled']):
            print("Starting Tokenization")
          
            arr_lines = self.__run_tokenizer(arr_lines)
                                                              
                                                               
        if(args_cleaner['enabled']):
            print("Starting Cleaning")
          
            arr_lines = self.__run_cleaner(arr_lines,
                                                            remove_special_character = args_cleaner['remove_special_character'], 
                                                            replace_digits = args_cleaner['replace_digits'], 
                                                            digit_language = args_cleaner['digit_language'],
                                                            remove_foreign_language_occurences = args_cleaner['remove_foreign_language_occurences'],
                                                            remove_foreign_language_lines = args_cleaner['remove_foreign_language_lines'],
                                                            remove_extra_whitespace = args_cleaner['remove_extra_whitespace'],
                                                            filter_line_by_length_mode = args_cleaner['filter_line_by_length_mode'],
                                                            max_length_threshold = args_cleaner['max_length_threshold'],
                                                            min_length_threshold = args_cleaner['min_length_threshold']
                                                            )
            print("Number of lines after Cleaning: ", len(arr_lines))
           

        if (args_saver['enabled']):
            print("Starting Saving to Local")
            self._run_saver(arr_lines,
                            directory_for_duplication_check=args_saver['directory_for_duplication_check'],
                            delimiter_text_file=args_saver['delimiter_text_file'],
                            file_type_for_saving=args_saver['file_type_for_saving'],
                            target_directory_for_saving=args_saver['target_directory_for_saving'],
                            file_name_for_saving=args_saver['file_name_for_saving'],
                            one_sentence_per_file=args_saver['one_sentence_per_file'],
                            check_for_duplicacy=args_saver['check_for_duplicacy'])
  
            del arr_lines
            print("Save to Local Completed")

            #Upload the processed data to GCS
            print("Initiating processed data upload to cloud storage")
            batch_id=self.generate_batchid()
            print("BatchId for Current run: {}".format(batch_id))
            if (args_saver['one_sentence_per_file'] == True):
                obj_gcsops.upload_to_gcs(bucket_name=gcs_bucket_name,
                                         source=os.path.join(current_work_dir,args_saver['target_directory_for_saving']),
                                         destination_blob_name=os.path.join(args_saver['target_directory_for_saving'],batch_id),
                                         is_directory=True)
            else:
                obj_gcsops.upload_to_gcs(bucket_name=gcs_bucket_name,
                                         source=os.path.join(current_work_dir,args_saver['target_directory_for_saving'],
                                                                            args_saver['file_name_for_saving'] +
                                                                            "." + args_saver['file_type_for_saving']),
                                         destination_blob_name=os.path.join(args_saver['target_directory_for_saving'],
                                                                             batch_id,
                                                                             args_saver['file_name_for_saving'] +
                                                                             "." + args_saver['file_type_for_saving']),
                                         is_directory=False)

            print("Upload to cloud storage completed")
            print('Total Time for Pipeline to run:', time.time() - pipeline_start_time )
            

        else:
            return arr_lines





if __name__ == "__main__":
    #Get Arguments
    job_mode=sys.argv[1] # local,cluster
    gcs_bucket_name = sys.argv[2]  # remote_gcs bucket name
    config_path=sys.argv[3] # remote gcs path, for local it will be src/resources/local/config.yaml

    current_working_directory = os.getcwd()
    config_local_path = os.path.join(current_working_directory,"src/resources/"+job_mode+"/config.yaml")

    if(job_mode=="cluster"):
        # Download config file from GCS
        print("Downloading config file from cloud storage to local")
        obj_gcs = CloudStorageOperations()
        obj_gcs.download_to_local(bucket_name=gcs_bucket_name,
                                  source_blob_name=config_path,
                                  destination=config_local_path,
                                  is_directory=False)

    obj = HindiPipeline()
    obj.fit(yaml_file_path=config_local_path,
            bucket_name=gcs_bucket_name,
            current_work_dir=current_working_directory)
