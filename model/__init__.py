from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.vinho import Vinho
from model.modelo import Modelo
from model.pipeline import Pipeline
from model.preprocessador import PreProcessador
from model.avaliador import Avaliador
from model.carregador import Carregador

# Caminho do diretório do banco
db_path = "database/"

# Cria o diretório se não existir
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Caminho e URL do banco SQLite
db_url = f"sqlite:///{db_path}vinhos.sqlite3"

# Criação da engine e da sessão
engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

# Cria o banco e as tabelas se necessário
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)