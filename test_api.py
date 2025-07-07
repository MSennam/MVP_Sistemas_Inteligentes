import pytest
import json
from app import app
from model import Session, Vinho
import uuid

# Comando para rodar: pytest -v test_api.py

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_vinho_data():
    return {
        "nome": f"Vinho Teste {uuid.uuid4()}",
        "fix_acid": 7.5,
        "vol_acid": 0.5,
        "cit_acid": 0.3,
        "res_sugar": 6.1,
        "chlorides": 0.04,
        "free_sulf": 30.0,
        "total_sulf": 100.0,
        "density": 0.995,
        "ph": 3.3,
        "sulphates": 0.6,
        "alcohol": 11.0
    }

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_vinhos_empty(client):
    response = client.get('/vinhos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vinhos' in data
    assert isinstance(data['vinhos'], list)

def test_add_vinho(client, sample_vinho_data):
    # remove se já existir
    session = Session()
    existente = session.query(Vinho).filter(Vinho.nome == sample_vinho_data["nome"]).first()
    if existente:
        session.delete(existente)
        session.commit()
    session.close()

    response = client.post(
        '/vinho',
        data=json.dumps(sample_vinho_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["nome"] == sample_vinho_data["nome"]
    assert "quality_pred" in data
    assert "class_label" in data

def test_add_duplicated_vinho(client, sample_vinho_data):
    client.post('/vinho', data=json.dumps(sample_vinho_data), content_type='application/json')
    response = client.post('/vinho', data=json.dumps(sample_vinho_data), content_type='application/json')
    assert response.status_code == 409
    data = json.loads(response.data)
    assert "message" in data

def test_get_vinho_by_nome(client, sample_vinho_data):
    client.post('/vinho', data=json.dumps(sample_vinho_data), content_type='application/json')
    response = client.get(f'/vinho?nome={sample_vinho_data["nome"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["nome"] == sample_vinho_data["nome"]

def test_get_vinho_inexistente(client):
    response = client.get('/vinho?nome=VINHO_INEXISTENTE_123')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "message" in data

def test_delete_vinho(client, sample_vinho_data):
    client.post('/vinho', data=json.dumps(sample_vinho_data), content_type='application/json')
    response = client.delete(f'/vinho?nome={sample_vinho_data["nome"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "removido com sucesso" in data["message"]

def test_delete_vinho_inexistente(client):
    response = client.delete('/vinho?nome=VINHO_NAO_EXISTENTE_456')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "message" in data

# Teste de extremos (opcional)
def test_predicao_extremos(client):
    extremos = [
        {
            "nome": "Vinho Ruim",
            "fix_acid": 12.0,
            "vol_acid": 1.5,
            "cit_acid": 0.0,
            "res_sugar": 15.0,
            "chlorides": 0.2,
            "free_sulf": 5.0,
            "total_sulf": 10.0,
            "density": 1.005,
            "ph": 2.5,
            "sulphates": 0.3,
            "alcohol": 8.0
        },
        {
            "nome": "Vinho Bom",
            "fix_acid": 6.0,
            "vol_acid": 0.25,
            "cit_acid": 0.4,
            "res_sugar": 3.0,
            "chlorides": 0.03,
            "free_sulf": 40.0,
            "total_sulf": 120.0,
            "density": 0.990,
            "ph": 3.4,
            "sulphates": 0.8,
            "alcohol": 13.0
        }
    ]

    for vinho in extremos:
        response = client.post('/vinho', data=json.dumps(vinho), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "quality_pred" in data
        assert "class_label" in data