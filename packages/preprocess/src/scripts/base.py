import numpy as np

class BaseClass(object):
    def __init__(self, language):
        self.language = language
    
    def _convert_to_numpy(self, data):
        if type(data) is np.ndarray:
            return
        return np.array(data)
