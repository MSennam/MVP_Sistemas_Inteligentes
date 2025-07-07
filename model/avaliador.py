from sklearn.metrics import accuracy_score

class Avaliador:
    
    def __init__(self):
        
        pass
    """ Fazendo predição e avaliando o modelo. """
    def avaliar(self, model, X_test, Y_test):
        
        predicoes = model.predict(X_test)
        return accuracy_score(Y_test, predicoes)
                
