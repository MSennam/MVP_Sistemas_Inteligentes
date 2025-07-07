import pickle


class Modelo:

    def __init__(self):
        self.modelo = None

    def carrega_modelo(self, path):
        """Carrega sendo Pickle ou Joblib"""

        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                self.modelo = pickle.load(file)
        else:
            raise Exception(
                'Formato de arquivo não suportado, arquivo precisa ser .pkl')
        return self.modelo

    def prediz_vinho(self, X_input):
        """Prediz a qualidade do vinho, com base nos dados de entrada baseado no treinamento."""
        if self.modelo is None:
            raise Exception(
                'Modelo não foi carregado. Use carrega_modelo() primeiro.')
        diagnosis = self.modelo.predict(X_input)
        return diagnosis
