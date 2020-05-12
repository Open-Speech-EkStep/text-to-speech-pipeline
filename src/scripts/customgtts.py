from gtts import gTTS
from loader import DataLoader
import time
from tqdm import tqdm

from joblib import Parallel, delayed

class CustomgTTS(object):
    def __init__(self, language, file_format='mp3'):
        self.language = language
        self.save_format = file_format
        

    def __save_file(self, path, obj):
        ## if one sentence per file --> save file as the same name of input file

        try:
            obj.save(path)
            return 1
        except:
            return 0

    def __get_tts_object(self, text, slow):
        
        myobj = gTTS(text = text, lang=self.language, slow=False) 
        return myobj


    def test_text_to_speech(self, mytext , path,  slow = False):
        obj = self.__get_tts_object(mytext, slow)
        return self.__save_file(path, obj)

    def text_to_speech(self, source_directory , save_directory = None,  slow = False, parallel_processing = False, nworkers = -1 ):


        if save_directory is None:
            save_directory = source_directory
        
        loader = DataLoader()

        ## sentences 4000, limit ->> 2000

        ## for batches in retuned

        arr_lines_dict = loader.load_data(path = source_directory, file_type='dir')

        if parallel_processing:
            Parallel(n_jobs=nworkers, prefer='threads', verbose=1)(delayed(self.__parallel_funct)(record, source_directory, save_directory, slow) for record in arr_lines_dict)
            return

        for record in tqdm(arr_lines_dict):
            mytext = record['data']
            filename = record['filename']
            full_save_path = save_directory + '/' + filename.split('/')[-1].split('.')[0] + '.' + self.save_format
            obj = self.__get_tts_object(mytext[0], slow)
            self.__save_file(full_save_path, obj)

    def __parallel_funct(self, record, source_directory, save_directory, slow):
        mytext = record['data']
        filename = record['filename']


        full_save_path = save_directory + '/' + filename.split('/')[-1].split('.')[0] + '.' + self.save_format
        #start = time.time()
        
        obj = self.__get_tts_object(mytext[0], slow)
        #print("TTS time: ", time.time()-start)

        #start = time.time()
        
        self.__save_file(full_save_path, obj)
        #print("Save time: ", time.time()-start)



if __name__ == "__main__":

    start_time = time.time()
    obj = CustomgTTS('hi')
    hindi_text = 'कालिंजर दुर्ग, भारतीय राज्य उत्तर प्रदेश के बांदा जिला स्थित एक दुर्ग है। बुन्देलखण्ड क्षेत्र में विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर स्थल खजुराहो से ९७.७ किमी दूर है'
    save_path = './abc.wav'

    source_directory = '/Users/harveen.chadha/Ekstep Speech Recognition/github/tts/text-to-speech-pipeline/data/raw/transcript'
    save_directory = '/Users/harveen.chadha/Ekstep Speech Recognition/github/tts/text-to-speech-pipeline/data/external/transcript'

    obj.text_to_speech(source_directory, save_directory = save_directory)

    print("Total Time taken for pipeline is ", time.time() - start_time)



    