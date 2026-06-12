from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.viacep_service import buscar_endereco_por_cep
from app.services.login_service import gerar_login
from app.database.session import get_db
from app.repositories.pessoa_repository import (
    criar_pessoa,
    buscar_por_cpf_ou_email,
    listar_logins,
    listar_pessoas,
    buscar_pessoa_por_id,
    buscar_por_login
)
from app.schemas.pessoa_schema import PessoaCreate, PessoaResponse

router = APIRouter(
    prefix="/pessoas",
    tags=["Pessoas"]
)

@router.post("/", status_code=201)
def cadastrar_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    pessoa_existente = buscar_por_cpf_ou_email(
        db=db,
        cpf=pessoa.cpf,
        email=pessoa.email
    )
    if pessoa_existente:
        raise HTTPException(
            status_code=400,
            detail="CPF ou e-mail já cadastrado."
        )
    logins_existentes = listar_logins(db)

    try:
        endereco = buscar_endereco_por_cep(pessoa.cep)
    
    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )
    
    pessoa_salva = criar_pessoa(
        db=db,
        nome=pessoa.nome,
        cpf=pessoa.cpf,
        email=pessoa.email,
        data_nascimento=pessoa.data_nascimento,
        cep=pessoa.cep,
        logradouro=endereco["logradouro"],
        numero_endereco=pessoa.numero_endereco,
        bairro=endereco["bairro"],
        cidade=endereco["cidade"],
        uf=endereco["uf"],
        complemento=pessoa.complemento or endereco["complemento"],
        login=gerar_login(
            pessoa.nome,
            logins_existentes
        )
    )

    return {
        "message": "Pessoa cadastrada com sucesso",
        "id": pessoa_salva.id,
        "nome": pessoa_salva.nome,
        "cpf": pessoa_salva.cpf,
        "email": pessoa_salva.email,
        "data_nascimento": pessoa_salva.data_nascimento,
        "cep": pessoa_salva.cep,
        "logradouro": pessoa_salva.logradouro,
        "numero_endereco": pessoa_salva.numero_endereco,
        "bairro": pessoa_salva.bairro,
        "cidade": pessoa_salva.cidade,
        "uf": pessoa_salva.uf,
        "complemento": pessoa_salva.complemento,
        "login": pessoa_salva.login
    }

@router.get("/", response_model=list[PessoaResponse])
def buscar_pessoas(db: Session = Depends(get_db)):
    pessoas = listar_pessoas(db)

    return pessoas

@router.get("/ID/{pessoa_id}", response_model=PessoaResponse)
def buscar_id(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa = buscar_pessoa_por_id(db, pessoa_id)

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )
    
    return pessoa

@router.get("/Login/{pessoa_login}", response_model=PessoaResponse)
def buscar_login(pessoa_login: str, db: Session = Depends(get_db)):
    login = buscar_por_login(db, pessoa_login)
    
    if not login:
        raise HTTPException(
            status_code=404,
            detail="Login não existe"
        )
    
    return login