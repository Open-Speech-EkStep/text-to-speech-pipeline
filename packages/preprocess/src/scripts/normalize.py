from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
import numpy as np

class DataNormalizer(object):
    """
    Replaces '|' with '।'.
    """
    
    def __init__(self, language):
        self.language = language
        self.__set_normalizer_object()
    
    def __set_normalizer_object(self):
        if(self.language == 'hi'):
            factory = IndicNormalizerFactory()
            self.normalizer_obj = factory.get_normalizer(self.language)

    def __normalize_data(self, data):
        return self.normalizer_obj.normalize(data)

    def normalize_data(self, data):
        """
        Normalizes data using indicnlp's IndicNormalizerFactory().
        
        Args:
            data: numpy array of sentences
        """
        processed_data = []
        for paragraph in data:
            processed_data.append(self.__normalize_data(paragraph))
        
        return processed_data
