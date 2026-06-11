from sqlalchemy.orm import Session
from datetime import date

from app.models.pessoa import Pessoa


def criar_pessoa(
    db: Session,
    nome: str,
    cpf: str,
    email: str,
    data_nascimento: date,
    cep: str,
    logradouro: str,
    numero_endereco: str,
    bairro: str,
    cidade: str,
    uf: str,
    complemento: str,
    login: str
):
    pessoa = Pessoa(
        nome=nome,
        cpf=cpf,
        email=email,
        data_nascimento=data_nascimento,
        cep=cep,
        logradouro=logradouro,
        numero_endereco=numero_endereco,
        bairro=bairro,
        cidade=cidade,
        uf=uf,
        complemento=complemento,
        login=login
    )

    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)

    return pessoa

def buscar_por_cpf_ou_email(db: Session, cpf: str, email: str):
    return db.query(Pessoa).filter(
        (Pessoa.cpf == cpf) | (Pessoa.email == email)
    ).first()

def buscar_por_login(db: Session, login: str):
    return db.query(Pessoa).filter(Pessoa.login == login).first()

def listar_logins(db: Session):
    pessoas = db.query(Pessoa.login).all()

    return [pessoa.login for pessoa in pessoas]

def listar_pessoas(db: Session):
    return db.query(Pessoa).all() 

def buscar_pessoa_por_id(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()