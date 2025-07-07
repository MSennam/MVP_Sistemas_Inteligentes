from pydantic import BaseModel
from typing import Optional, List
from model.vinho import Vinho
import json
import numpy as np

# Schema de entrada: dados que o usuário envia para classificar o vinho
class VinhoSchema(BaseModel):
    nome: str = "Cabernet Teste"
    fix_acid: float = 7.0
    vol_acid: float = 0.6
    cit_acid: float = 0.25
    res_sugar: float = 2.1
    chlorides: float = 0.08
    free_sulf: float = 15.0
    total_sulf: float = 60.0
    density: float = 0.9968
    ph: float = 3.3
    sulphates: float = 0.6
    alcohol: float = 10.0

# Schema de saída (para exibir um vinho armazenado)
class VinhoViewSchema(BaseModel):
    id: int
    nome: str
    fix_acid: float
    vol_acid: float
    cit_acid: float
    res_sugar: float
    chlorides: float
    free_sulf: float
    total_sulf: float
    density: float
    ph: float
    sulphates: float
    alcohol: float
    quality_pred: int
    class_label: str

# Schema para busca (por nome)
class VinhoBuscaSchema(BaseModel):
    nome: str = "Cabernet Teste"

# Lista de vinhos
class ListaVinhosSchema(BaseModel):
    vinhos: List[VinhoViewSchema]

# Schema para deleção (baseado no nome)
class VinhoDelSchema(BaseModel):
    nome: str = "Cabernet Teste"

def apresenta_vinho(vinho: Vinho):
    """Retorna uma representação do vinho conforme VinhoViewSchema"""
    return {
        "id": vinho.id,
        "nome": vinho.nome,
        "fix_acid": vinho.fix_acid,
        "vol_acid": vinho.vol_acid,
        "cit_acid": vinho.cit_acid,
        "res_sugar": vinho.res_sugar,
        "chlorides": vinho.chlorides,
        "free_sulf": vinho.free_sulf,
        "total_sulf": vinho.total_sulf,
        "density": vinho.density,
        "ph": vinho.ph,
        "sulphates": vinho.sulphates,
        "alcohol": vinho.alcohol,
        "quality_pred": vinho.quality_pred,
        "class_label": vinho.class_label
    }

def apresenta_vinhos(vinhos: List[Vinho]):
    """Retorna uma lista de vinhos no formato ListaVinhosSchema"""
    result = []
    for v in vinhos:
        result.append(apresenta_vinho(v))
    return {"vinhos": result}   