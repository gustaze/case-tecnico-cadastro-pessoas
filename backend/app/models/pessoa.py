from sqlalchemy import Column, Integer, String, Date

from app.database.database import Base


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    cpf = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    data_nascimento = Column(Date, nullable=False)

    cep = Column(String, nullable=False)

    logradouro = Column(String, nullable=True)

    numero_endereco = Column(String, nullable=True)

    bairro = Column(String, nullable=True)

    cidade = Column(String, nullable=False)

    uf = Column(String, nullable=False)

    complemento = Column(String, nullable=True)

    login = Column(String, unique=True, nullable=False)