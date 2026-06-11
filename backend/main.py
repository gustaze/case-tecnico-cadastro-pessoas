from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.models.pessoa import Pessoa
from app.api.pessoa_api import router as pessoa_router

Pessoa.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cadastro de Pessoas API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pessoa_router)

@app.get("/", tags=["Sistema"])
def home():
    return {
        "nome": "Cadastro de Pessoas API",
        "versao": "1.0",
        "message": "Online"
    }