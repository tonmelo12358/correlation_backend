from sqlalchemy import Column, String, Integer

from  model import Base

class Correlacao(Base):
    __tablename__ = 'correlacao'

    id_correlacao = Column("pk_correlacao", Integer, primary_key=True, autoincrement=True)
    sistema_origem = Column(String(140), nullable=False)
    entidade_origem = Column(String(140), nullable=False)
    id_origem = Column(String(140), nullable=False)
    sistema_destino = Column(String(140), nullable=False)
    entidade_destino = Column(String(140), nullable=False)
    id_destino = Column(String(140), nullable=False)
    grupo = Column(String(140), nullable=False)


    def __init__(self, sistema_origem:str, entidade_origem:str, id_origem:str,
                sistema_destino:str, entidade_destino:str, id_destino:str, grupo:str):
        """
        Cria uma Correlação

        Arguments:
            sistema_origem: nome do sistema de origem.
            entidade_origem: nome da entidade de origem.
            id de origem: id do sistema de origem.
            sistema_destino: nome do sistema de destino.
            entidade_destino: nome da entidade de destino.
            id de destino: id do sistema de destino.
            grupo: grupo a qual a correlação pertence (opcional)
        """
        self.sistema_origem = sistema_origem
        self.entidade_origem = entidade_origem
        self.id_origem = id_origem
        self.sistema_destino = sistema_destino
        self.entidade_destino = entidade_destino
        self.id_destino = id_destino
        self.grupo = grupo
