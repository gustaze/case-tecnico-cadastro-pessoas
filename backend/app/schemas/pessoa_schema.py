from pydantic import BaseModel, EmailStr, field_validator
import re
from datetime import date


class PessoaCreate(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    data_nascimento: date
    cep: str
    complemento: str | None = None
    numero_endereco: str | None = None

    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        
        if not re.fullmatch(r"[A-Za-zÀ-ÿ ]+", valor):
            raise ValueError("Nome deve conter apenas letras e espaços.")

        return valor.strip()

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, valor):
        if not re.fullmatch(r"\d{11}", valor):
            raise ValueError("CPF deve conter exatamente 11 números.")

        return valor

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, valor):
        if valor > date.today():
            raise ValueError("Data de nascimento não pode ser futura.")

        return valor

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, valor):
        if not re.fullmatch(r"\d{8}", valor):
            raise ValueError("CEP deve conter exatamente 8 números.")

        return valor
    
class PessoaResponse(BaseModel):
    id: int
    login: str
    nome: str
    cpf: str
    email: EmailStr
    data_nascimento: date
    cep: str
    logradouro: str | None
    numero_endereco: str | None
    complemento: str | None
    bairro: str | None
    cidade: str
    uf: str

    model_config = {
        "from_attributes": True
    }