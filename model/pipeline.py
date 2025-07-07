import pickle

class Pipeline:
    
    def __init__(self):
        self.pipeline = None
    
    def carrega_pipeline(self, path):
        """Carregando o pipeline usado no treinamento. StandarScaler """
        
        with open(path, 'rb') as file:
             self.pipeline = pickle.load(file)
        return self.pipeline