import requests


def buscar_endereco_por_cep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"

    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()

    dados = resposta.json()

    if dados.get("erro"):
        raise ValueError("CEP não encontrado.")

    return {
        "cep": dados.get("cep"),
        "logradouro": dados.get("logradouro"),
        "complemento": dados.get("complemento"),
        "bairro": dados.get("bairro"),
        "cidade": dados.get("localidade"),
        "uf": dados.get("uf")
    }