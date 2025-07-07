import pytest
from model import *
from os.path import exists

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Modelo()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./data/X_test.csv"
url_classes = "./data/Y_test.csv"
colunas = [
    'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    'chlorides', 'free sulfur dioxide', 'total sulfur dioxide',
    'density', 'pH', 'sulphates', 'alcohol'
]

# Verificações básicas de existência
def test_arquivos_existem():
    assert exists(url_dados), "Arquivo X_test.csv não encontrado!"
    assert exists(url_classes), "Arquivo Y_test.csv não encontrado!"
    assert exists("./pipelines/et_wine_classifier_pipeline.pkl"), "Pipeline não encontrado!"
    assert exists("./modelos/et_wine_classifier.pkl"), "Modelo .pkl não encontrado!"
    assert exists("./scalers/standard_scaler.pkl"), "Scaler não encontrado!"

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:, 0:]
y = carregador.carregar_dados(url_classes, ['quality']).values.ravel()

# Testa o modelo Extra Trees
def test_modelo_et():
    modelo_et = modelo.carrega_modelo('./modelos/et_wine_classifier.pkl')
    acuracia = avaliador.avaliar(modelo_et, X, y)
    print("Acurácia do modelo Extra Trees:", acuracia)
    assert acuracia >= 0.50  # Ajuste o threshold se necessário

# Testa a pipeline completa
def test_pipeline_et():
    pipeline_et = pipeline.carrega_pipeline('./pipelines/et_wine_classifier_pipeline.pkl')
    acuracia = avaliador.avaliar(pipeline_et, X, y)
    print("Acurácia da pipeline:", acuracia)
    assert acuracia >= 0.55