from indicnlp.tokenize import sentence_tokenize
import numpy as np

class DataTokenizer:
    
    def __init__(self, language):
        self.language = language
    
    def __tokenize_data(self, data):
        return sentence_tokenize.sentence_split(data, lang=self.language)


    
    def __tokenize_paragraph(self, paragraph):
        tokenized_paragraph = []
        if paragraph and len(paragraph) > 0:
            tokenized_paragraph = self.__tokenize_data(paragraph)
        return tokenized_paragraph





    def tokenize_data(self, data):
        processed_data = []

        for paragraph in data:
            processed_data.extend(self.__tokenize_paragraph(paragraph))
   
        return processed_data
