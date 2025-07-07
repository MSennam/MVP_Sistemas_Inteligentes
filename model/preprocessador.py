from sklearn.model_selection import train_test_split
import numpy as np
import pickle

class PreProcessador:
    def __init__(self):
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=5):
        """ Cuidando do pré-processamento"""
                
        # limpeza e seleção de atributos buscando eliminar outliers

        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(
            dataset, percentual_teste, seed
        )

        return X_train, X_test, Y_train, Y_test

    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """
        Faz divisão dos dados dados em treino e teste.

        Argumentoss:
            dataset: DataFrame Pandas contendo o dataset completo
            percentual_teste: fração do conjunto de dados para teste (ex: 0.2)
            seed: semente para reprodutibilidade

        Returns:
            X, y separados com stratify
        """
        dados = dataset.values
        X = dados[:, 0:11]   # 11 atributos do vinho
        Y = dados[:, 11]     # qualidade do vinho (quality no dataset)
        return train_test_split(X, Y, test_size=percentual_teste,
                                random_state=seed, stratify=Y)

    def preparar_form(self, form):
        """
        Prepara os dados recebidos do formulário HTML para envio ao modelo.

        Args:
            form: objeto com atributos do vinho

        Returns:
            np.ndarray com shape (1, 11)
        """
        X_input = np.array([
            form.fix_acid,
            form.vol_acid,
            form.cit_acid,
            form.res_sugar,
            form.chlorides,
            form.free_sulf,
            form.total_sulf,
            form.density,
            form.ph,
            form.sulphates,
            form.alcohol
        ])

        return X_input.reshape(1, -1)

    def aplicar_scaler(self, X_input, path_scaler):
        """
        Aplica um scaler salvo via pickle nos dados.

        Args:
            X_input: dados de entrada (np.ndarray)
            path_scaler: caminho do arquivo .pkl do scaler

        Returns:
            Dados transformados
        """
        scaler = pickle.load(open(path_scaler, 'rb'))
        return scaler.transform(X_input)