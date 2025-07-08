from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request # Import 'request' from Flask
from urllib.parse import unquote
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from model import *
from logger import logger
from schemas import *

# API metadata
info = Info(title="API Classificação de Vinhos", version="1.0.0")

# Configuração da aplicação
app = OpenAPI(__name__, info=info, static_folder="front",
              static_url_path="/front")

CORS(app)

# Tags
home_tag = Tag(name="Documentação",
               description="Documentação via Swagger ou Redoc")
vinho_tag = Tag(name="Vinho", description="Predição e gestão de vinhos")

# Rota inicial
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para a interface frontend."""
    return redirect("/front/index.html")


@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para a documentação Swagger."""
    return redirect("/openapi/swagger")


@app.get("/vinhos", tags=[vinho_tag], responses={"200": ListaVinhosSchema, "404": ErrorSchema})
def get_vinhos():
    """Lista todos os vinhos cadastrados."""
    session = Session()
    vinhos = session.query(Vinho).all()

    if not vinhos:
        return {"vinhos": []}, 200
    else:
        return apresenta_vinhos(vinhos), 200



@app.post("/vinho", tags=[vinho_tag], responses={"200": VinhoViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(): 
    
    # 1. Pega os dados JSON brutos diretamente da requisição
    data = request.get_json()
    logger.info(f"Dados recebidos pela API: {data}")

    # 2. Tenta criar o objeto Pydantic manualmente a partir dos dados brutos
    try:
        form = VinhoSchema(**data)
    except ValidationError as e:
        logger.error(f"Erro de validação do Pydantic: {e}")
        return {"message": "Dados de entrada inválidos.", "errors": e.errors()}, 400

    
    
    preprocessador = PreProcessador()
    pipeline_loader = Pipeline()
    X_input = preprocessador.preparar_form(form)
    modelo = pipeline_loader.carrega_pipeline(
        "pipelines/et_wine_classifier_pipeline.pkl")

    quality = int(modelo.predict(X_input)[0])
    if quality <= 3:
        label = "ruim"
    elif quality <= 5:
        label = "médio"
    elif quality <= 7:
        label = "bom"
    else:
        label = "muito bom"

    vinho = Vinho(
        nome=form.nome,
        fix_acid=form.fix_acid,
        vol_acid=form.vol_acid,
        cit_acid=form.cit_acid,
        res_sugar=form.res_sugar,
        chlorides=form.chlorides,
        free_sulf=form.free_sulf,
        total_sulf=form.total_sulf,
        density=form.density,
        ph=form.ph,
        sulphates=form.sulphates,
        alcohol=form.alcohol,
        quality_pred=quality,
        class_label=label
    )

    try:
        session = Session()
        if session.query(Vinho).filter(Vinho.nome == vinho.nome).first():
            return {"message": "Vinho já registrado."}, 409
        session.add(vinho)
        session.commit()
        return apresenta_vinho(vinho), 200
    except Exception as e:
        logger.warning(f"Erro ao adicionar vinho: {e}")
        return {"message": "Erro ao processar o vinho."}, 400


@app.get(
    "/vinho",
    tags=[vinho_tag],
    responses={"200": VinhoViewSchema, "404": ErrorSchema},
)
def get_vinho(query: VinhoBuscaSchema):
    """Busca um vinho cadastrado na base pelo nome."""
    vinho_nome = unquote(query.nome)
    logger.debug(f"Buscando vinho '{vinho_nome}'")
    session = Session()
    vinho = session.query(Vinho).filter(Vinho.nome == vinho_nome).first()
    if not vinho:
        error_msg = f"Vinho '{vinho_nome}' não encontrado."
        logger.warning(error_msg)
        return {"message": error_msg}, 404
    else:
        return apresenta_vinho(vinho), 200


@app.delete(
    "/vinho",
    tags=[vinho_tag],
    responses={"200": {"description": "Mensagem de sucesso"}, "404": ErrorSchema},
)
def delete_vinho(query: VinhoBuscaSchema):
    """Remove um vinho cadastrado na base pelo nome."""
    vinho_nome = unquote(query.nome)
    logger.debug(f"Deletando vinho '{vinho_nome}'")
    session = Session()
    vinho = session.query(Vinho).filter(Vinho.nome == vinho_nome).first()
    if not vinho:
        error_msg = f"Vinho '{vinho_nome}' não encontrado."
        logger.warning(error_msg)
        return {"message": error_msg}, 404
    else:
        session.delete(vinho)
        session.commit()
        logger.debug(f"Vinho '{vinho_nome}' deletado com sucesso.")
        return {
            "message": f"Vinho '{vinho_nome}' removido com sucesso!"
        }, 200


if __name__ == "__main__":
    app.run(debug=True)