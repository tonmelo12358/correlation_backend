from pydantic import BaseModel
from typing import List
from model.correlacao import Correlacao

class CorrelacaoSchema(BaseModel):
    """ Define como uma nova Correlação a ser inserida deve ser representada
    """

    sistema_origem: str = "SistemaOrigem"
    entidade_origem: str = "EntidadeOrigem"
    id_origem: str = "IDOrigem"
    sistema_destino: str = "SistemaDestino"
    entidade_destino: str = "EntidadeDestino"
    id_destino: str = "IDDestino"
    grupo: str = "GrupoCorrelacao"


class CorrelacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da Correlacao.
    """
    id_correlacao: int = "1"

##### novas classes #######

class CorrelacaoBuscaOrigemSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca baseada 
        no sistema de origem.
    """
    sistema_origem: str = "IBMS"

class CorrelacaoBuscaDestinoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca baseada 
        no sistema de destino.
    """
    sistema_destino: str = "HCM"

class CorrelacaoBuscaGrupoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca baseada 
        no grupo.
    """
    grupo: str = "OLIMPIADAS"

###### fim das novas classes ######

class ListagemCorrelacoesSchema(BaseModel):
    """ Define como uma listagem de Correlacoes será retornada.
    """
    correlacoes:List[CorrelacaoSchema]


def apresenta_correlacoes(correlacoes: List[Correlacao]):
    """ Retorna uma representação da correlação seguindo o schema definido em
        CorrelacaoViewSchema.
    """
    result = []
    for correlacao in correlacoes:
        result.append({
            "id de correlacao": correlacao.id_correlacao,
            "sistema de origem": correlacao.sistema_origem,
            "entidade de origem": correlacao.entidade_origem,
            "id de origem": correlacao.id_origem,
            "sistema de destino": correlacao.sistema_destino,
            "entidade de destino": correlacao.entidade_destino,
            "id de destino": correlacao.id_destino,
            "grupo": correlacao.grupo,
        })

    return {"correlacoes": result}


class CorrelacaoViewSchema(BaseModel):
    """ Define como uma correlação será retornada: correlação + grupo
    """
    id_correlacao: int = 1
    sistema_origem: str = "IBMS"
    entidade_origem: str = "Media_Id"
    id_origem: str = "SJF2843F"
    sistema_destino: str = "PLAYOUT"
    entidade_destino: str = "Transmission_Id"
    id_destino: str = "45845u3"
    grupo: str = "OLIMPIADAS"


class CorrelacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    correlacao: str


class CorrelacaoDelFullSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de correlacao a partir dos seus atributos.
    """
    mesage: str
    correlacao: str


def apresenta_correlacao(correlacao: Correlacao):
    """ Retorna uma representação da correlação seguindo o schema definido em
        CorrelacaoViewSchema.
    """
    return {
        "id_correlacao": correlacao.id_correlacao,
        "sistema de origem": correlacao.sistema_origem,
        "entidade_origem": correlacao.entidade_origem,
        "id_origem": correlacao.id_origem,
        "sistema de destino": correlacao.sistema_destino,
        "entidade de destino": correlacao.sistema_destino,
        "id de destino": correlacao.sistema_destino,
        "grupo": correlacao.grupo,
    }


###### novas funções #######

def correlacoes_sistema_origem(sistema_origem: str):
    """Retorna uma lista de correlações com base no sistema de origem."""

    correlacoes = []
    return correlacoes


def apresenta_correlacoes_origem(sistema_origem: str):
    """ Retorna uma representação das correlações com base no sistema de origem. """

    correlacoes_origem = correlacoes_sistema_origem(sistema_origem)
    return apresenta_correlacoes(correlacoes_origem)


def correlacoes_sistema_destino(sistema_destino: str):
    """Retorna uma lista de correlações com base no sistema de destino."""

    correlacoes = []
    return correlacoes


def apresenta_correlacoes_destino(sistema_destino: str):
    """ Retorna uma representação das correlações com base no sistema de destino. """

    correlacoes_destino = correlacoes_sistema_destino(sistema_destino)
    return apresenta_correlacoes(correlacoes_destino)


def correlacoes_grupo(grupo: str):
    """Retorna uma lista de correlações com base no grupo."""

    correlacoes = []
    return correlacoes


def apresenta_correlacoes_grupo(grupo: str):
    """ Retorna uma representação das correlações com base no grupo. """

    correlacoes_encontradas_grupo = correlacoes_grupo(grupo)
    return apresenta_correlacoes(correlacoes_encontradas_grupo)


def normaliza_grupo(grupo):
    """Normaliza o valor do grupo para um formato padrão."""

    return grupo.upper().replace(" ", "_")
