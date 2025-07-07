from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Vinho(Base):
    __tablename__ = 'vinhos'

    id = Column(Integer, primary_key=True)
    nome = Column("Nome", String(100))
    fix_acid = Column("FixedAcidity", Float)
    vol_acid = Column("VolatileAcidity", Float)
    cit_acid = Column("CitricAcid", Float)
    res_sugar = Column("ResidualSugar", Float)
    chlorides = Column("Chlorides", Float)
    free_sulf = Column("FreeSulfurDioxide", Float)
    total_sulf = Column("TotalSulfurDioxide", Float)
    density = Column("Density", Float)
    ph = Column("pH", Float)
    sulphates = Column("Sulphates", Float)
    alcohol = Column("Alcohol", Float)
    quality_pred = Column("QualityPrediction", Integer)
    class_label = Column("Classificacao", String(20))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self, nome: str, fix_acid: float, vol_acid: float, cit_acid: float,
        res_sugar: float, chlorides: float, free_sulf: float,
        total_sulf: float, density: float, ph: float,
        sulphates: float, alcohol: float, quality_pred: int,
        class_label: str, data_insercao: Union[datetime, None] = None
    ):
        """
        Cria um registro de vinho.

        Arguments:
            nome: nome do vinho
            fix_acid: Acidez fixa
            vol_acid: Acidez volátil
            cit_acid: Ácido cítrico
            res_sugar: Açúcar residual
            chlorides: Cloretos
            free_sulf: Dióxido de enxofre livre
            total_sulf: Dióxido de enxofre total
            density: Densidade
            ph: pH
            sulphates: Sulfatos
            alcohol: Teor alcoólico
            quality_pred: Nota prevista (modelo)
            class_label: Classificação textual (ruim, médio, bom, muito bom)
            data_insercao: Data de inserção no banco (opcional)
        """
        self.nome = nome
        self.fix_acid = fix_acid
        self.vol_acid = vol_acid
        self.cit_acid = cit_acid
        self.res_sugar = res_sugar
        self.chlorides = chlorides
        self.free_sulf = free_sulf
        self.total_sulf = total_sulf
        self.density = density
        self.ph = ph
        self.sulphates = sulphates
        self.alcohol = alcohol
        self.quality_pred = quality_pred
        self.class_label = class_label
        self.data_insercao = data_insercao or datetime.now()
