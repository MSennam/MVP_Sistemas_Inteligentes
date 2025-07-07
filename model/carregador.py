import pandas as pd

class Carregador:

    def __init__(self):
        pass

    def carregar_dados(self, url: str, atributos: list):
        """Carregando os dados do csv através de uma URL"""
        if atributos:
            return pd.read_csv(url, names=atributos, header=0, delimiter=',')
        else:
            return pd.read_csv(url, delimiter=',') 