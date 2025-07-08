import pytest
from os.path import exists
from model import Carregador, Modelo, Avaliador, Pipeline


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

# Carga dos dados de teste a partir dos arquivos CSV
try:
    dataset = carregador.carregar_dados(url_dados, colunas)
    X = dataset.values
    y = carregador.carregar_dados(url_classes, ['quality']).values.ravel()
except FileNotFoundError:
    pytest.fail(
        "Arquivos X_test.csv ou Y_test.csv não encontrados. "
        "Certifique-se de gerá-los a partir do notebook no ambiente local."
    )

# Testes
def test_arquivos_existem():
    """Verifica se todos os arquivos necessários (dados e modelos) existem."""
    assert exists(url_dados), "Arquivo X_test.csv não encontrado!"
    assert exists(url_classes), "Arquivo Y_test.csv não encontrado!"
    assert exists("./pipelines/et_wine_classifier_pipeline.pkl"), "Pipeline não encontrado!"
    assert exists("./modelos/et_wine_classifier.pkl"), "Modelo .pkl não encontrado!"
    assert exists("./scalers/standard_scaler.pkl"), "Scaler não encontrado!"

def test_modelo_et():
    """Testa a acurácia do modelo .pkl, aplicando o scaler."""
    # Carrega o modelo e o scaler
    modelo_et = modelo.carrega_modelo('./modelos/et_wine_classifier.pkl')
    scaler = modelo.carrega_modelo('./scalers/standard_scaler.pkl')

    # Transforma os dados de teste com o scaler antes da avaliação
    X_test_scaled = scaler.transform(X)
    
    acuracia = avaliador.avaliar(modelo_et, X_test_scaled, y)
    print(f"\nAcurácia do modelo Extra Trees (com dados dimensionados): {acuracia}")
    
    assert acuracia >= 0.70

def test_pipeline_et():
    """Testa a acurácia da pipeline completa, que deve dimensionar os dados internamente."""
    pipeline_et = pipeline.carrega_pipeline('./pipelines/et_wine_classifier_pipeline.pkl')
    
    # A pipeline deve receber os dados brutos e fazer a transformação
    acuracia = avaliador.avaliar(pipeline_et, X, y)
    print(f"\nAcurácia da pipeline (dados brutos): {acuracia}")
    
    assert acuracia >= 0.70