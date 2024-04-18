from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from flask_cors import CORS


from model import Session, Correlacao
from logger import logger
from schemas import *


info = Info(title="Correlation Service API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
correlacao_tag = Tag(name="Correlação", description="Adição, visualização e remoção de Correlações à base")
filtros_tag = Tag(name="filtros", description="Adição de filtros a partir de sistemas e grupo")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/correlacao', tags=[correlacao_tag],
          responses={"200": CorrelacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_correlacao(form: CorrelacaoSchema):
    """Adiciona uma nova Correlacao à base de dados

    Retorna uma representação da correlação e o grupo associado.
    """
    
    try:
        # criando conexão com a base
        session = Session()

        # Normaliza o valor do grupo, retirando espaços ou letras maiúsculas
        grupo_normalizado = normaliza_grupo(form.grupo)

        # Verifica se já existe uma correlação com os mesmos valores
        correlacao_existente = session.query(Correlacao).filter(
            Correlacao.sistema_origem == form.sistema_origem,
            Correlacao.entidade_origem == form.entidade_origem,
            Correlacao.id_origem == form.id_origem,
            Correlacao.sistema_destino == form.sistema_destino,
            Correlacao.entidade_destino == form.entidade_destino,
            Correlacao.id_destino == form.id_destino,
            Correlacao.grupo == grupo_normalizado  ## grupo sem espaços ou letras maiúsculas
        ).all()

        if correlacao_existente:
            error_msg = "correlacao com o mesmo conjunto de atributos já salva na base :/"
            logger.warning(f"Erro ao adicionar correlacao, {error_msg}")
            return {"message": error_msg}, 409

        else:
            correlacao = Correlacao(
                sistema_origem=form.sistema_origem,
                entidade_origem=form.entidade_origem,
                id_origem=form.id_origem,
                sistema_destino=form.sistema_destino,
                entidade_destino=form.entidade_destino,
                id_destino=form.id_destino,
                grupo=grupo_normalizado,   ## grupo sem espaços ou letras maiúsculas
            )

            session.add(correlacao)
            session.commit()

            logger.debug(f"Adicionada correlacao de id: '{correlacao.id_correlacao}'")
            return apresenta_correlacao(correlacao), 200

    except IntegrityError:
        error_msg = "correlacao de mesmo id já salvo na base :/"
        logger.warning(f"Erro ao adicionar correlacao '{form.id_origem}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar correlacao '{form.id_origem}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/correlacoes', tags=[correlacao_tag],
         responses={"200": ListagemCorrelacoesSchema, "404": ErrorSchema})
def get_correlacoes():
    """Faz a busca por todas as correlacoes cadastradas

    Retorna uma representação da listagem de correlações.
    """
    logger.debug(f"Coletando correlações ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    correlacoes = session.query(Correlacao).all()

    if not correlacoes:
        # se não há correlações cadastradas
        return {"correlacoes": []}, 200
    else:
        logger.debug(f"%d correlações encontradas" % len(correlacoes))
        # retorna a representação de correlacao
        print(correlacoes)
        return apresenta_correlacoes(correlacoes), 200


@app.get('/correlacao', tags=[correlacao_tag],
         responses={"200": CorrelacaoViewSchema, "404": ErrorSchema})
def get_correlacao(query: CorrelacaoBuscaSchema):
    """Faz a busca por uma correlacao a partir do id da correlacao

    Retorna uma representação das correlacoes e o grupo associado.
    """
    correlacao_id = query.id_correlacao
    logger.debug(f"Coletando dados sobre correlacao #{correlacao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    correlacao = session.query(Correlacao).filter(Correlacao.id_correlacao == correlacao_id).first()

    if not correlacao:
        # se o correlacao não foi encontrada
        error_msg = "correlacao não encontrada na base :/"
        logger.warning(f"Erro ao buscar correlacao '{correlacao_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"correlacao econtrada: '{correlacao.id_correlacao}'")
        # retorna a representação de correlacao
        return apresenta_correlacao(correlacao), 200


@app.delete('/correlacao/', tags=[correlacao_tag],
            responses={"200": CorrelacaoDelSchema, "404": ErrorSchema})
def del_correlacao(query: CorrelacaoBuscaSchema):
    """Deleta uma correlação a partir do id de correlcao informado

    Retorna uma mensagem de confirmação da remoção.
    """
    correlacao_id = query.id_correlacao
    print(correlacao_id)
    logger.debug(f"Deletando dados sobre correlacao #{correlacao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    remover_correlacao = session.query(Correlacao).filter(Correlacao.id_correlacao == correlacao_id).delete()
    session.commit()

    if remover_correlacao:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada correlacao #{correlacao_id}")
        return {"mesage": "correlacao removida", "id": correlacao_id}
    else:
        # se o correlacao não foi encontrado
        error_msg = "correlacao não encontrado na base :/"
        logger.warning(f"Erro ao deletar correlacao #'{correlacao_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/correlacao/del_full', tags=[correlacao_tag],
          responses={"200": CorrelacaoDelFullSchema, "404": ErrorSchema})
def del_correlacao_full(query: CorrelacaoSchema):
    """Deleta uma correlação com base em todos os seus atributos

    Retorna uma mensagem de confirmação da remoção.
    """
    correlacao_data = query.dict()  # Converte o objeto Pydantic para um dicionário
    logger.debug(f"Deletando dados sobre correlacao com atributos: {correlacao_data}")

    # Verifica se todos os campos necessários estão presentes e não são None
    required_fields = ['sistema_origem', 'entidade_origem', 'id_origem', 'sistema_destino', 'entidade_destino', 'id_destino', 'grupo']

    if not all(field in correlacao_data and correlacao_data[field] is not None for field in required_fields):
        error_msg = "Todos os campos são obrigatórios e não podem ser None para deletar uma correlação."
        logger.warning(f"Erro ao deletar correlacao com atributos incompletos ou None: {correlacao_data}, {error_msg}")
        return {"message": error_msg}, 400
    
    # Criando conexão com a base
    session = Session()

    # Fazendo a remoção
    remover_correlacao = (
        session.query(Correlacao)
        .filter_by(**correlacao_data)
        .delete()
    )
    session.commit()

    if remover_correlacao:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada correlacao com atributos: {correlacao_data}")
        return {"message": "correlacao removida", "correlacao": correlacao_data}
    else:
        # Se a correlacao não foi encontrada
        error_msg = "correlacao não encontrado na base :/"
        logger.warning(f"Erro ao deletar correlacao com atributos: {correlacao_data}, {error_msg}")
        return {"message": error_msg}, 404


######## adicionando rotas de busca de correlação a partir de sistema de origem, 
######## sistema de destino e grupo ######

@app.get('/correlacoes/sistema_origem', tags=[correlacao_tag],
         responses={"200": CorrelacaoViewSchema, "404": ErrorSchema})
def get_correlacao_origem(query: CorrelacaoBuscaOrigemSchema):
    """Faz a busca por uma correlacao a partir de um sistema de origem

    Retorna uma representação das correlacoes e o grupo associado.
    """
    origem = query.sistema_origem
    logger.debug(f"Coletando dados sobre correlações com origem = {origem}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    correlacoes_origem = session.query(Correlacao).filter(Correlacao.sistema_origem == origem).all()

    if not correlacoes_origem:
            # se não há correlações cadastradas
            return {"correlacoes": []}, 200
    else:
        logger.debug(f"%d correlações encontradas" % len(correlacoes_origem))
        # retorna a representação de correlacao
        print(correlacoes_origem)
        return apresenta_correlacoes(correlacoes_origem), 200


    
@app.get('/correlacoes/sistema_destino', tags=[correlacao_tag],
         responses={"200": CorrelacaoViewSchema, "404": ErrorSchema})
def get_correlacao_destino(query: CorrelacaoBuscaDestinoSchema):
    """Faz a busca por uma correlacao a partir de um sistema de destino

    Retorna uma representação das correlacoes e o grupo associado.
    """
    destino = query.sistema_destino
    logger.debug(f"Coletando dados sobre correlações com destino = {destino}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    correlacoes_destino = session.query(Correlacao).filter(Correlacao.sistema_destino == destino).all()

    if not correlacoes_destino:
            # se não há correlações cadastradas
            return {"correlacoes": []}, 200
    else:
        logger.debug(f"%d correlações encontradas" % len(correlacoes_destino))
        # retorna a representação de correlacao
        print(correlacoes_destino)
        return apresenta_correlacoes(correlacoes_destino), 200


@app.get('/correlacoes/grupo', tags=[correlacao_tag],
         responses={"200": CorrelacaoViewSchema, "404": ErrorSchema})
def get_correlacao_grupo(query: CorrelacaoBuscaGrupoSchema):
    """Faz a busca por uma correlacao a partir de um grupo

    Retorna uma representação das correlacoes e o grupo associado.
    """
    nome_grupo = query.grupo
    logger.debug(f"Coletando dados sobre correlações com grupo = {nome_grupo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    correlacoes_grupo = session.query(Correlacao).filter(Correlacao.grupo == nome_grupo).all()

    if not correlacoes_grupo:
            # se não há correlações cadastradas
            return {"correlacoes": []}, 200
    else:
        logger.debug(f"%d correlações encontradas" % len(correlacoes_grupo))
        # retorna a representação de correlacao
        print(correlacoes_grupo)
        return apresenta_correlacoes(correlacoes_grupo), 200
    
