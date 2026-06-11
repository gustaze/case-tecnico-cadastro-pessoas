import unicodedata


def normalizar_nome(texto: str) -> str:
    texto = texto.strip().lower()

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))

    return texto

def intercalar_partes(primeira_parte: str, segunda_parte: str) -> str:
    login = ""

    tamanho_maximo = max(len(primeira_parte), len(segunda_parte))

    for i in range(tamanho_maximo):
        if i < len(primeira_parte):
            login += primeira_parte[i]

        if i < len(segunda_parte):
            login += segunda_parte[i]

        if len(login) >= 7:
            break

    return login[:7]

"""
Gera possíveis logins de 7 caracteres a partir do nome informado.
Tenta diferentes combinações para garantir unicidade.
"""
def gerar_candidatos_login(nome: str) -> list[str]:
    
    nome_normalizado = normalizar_nome(nome)

    partes = [
        parte for parte in nome_normalizado.split()
        if parte.isalpha()
    ]

    candidatos = []

    for i in range(len(partes)):
        for j in range(i + 1, len(partes)):
            primeira_parte = partes[i]
            segunda_parte = partes[j]

            combinacoes = [
                primeira_parte[:5] + segunda_parte[:2],
                primeira_parte[:4] + segunda_parte[:3],
                primeira_parte[:3] + segunda_parte[:4],
                primeira_parte[:2] + segunda_parte[:5],
                segunda_parte[:5] + primeira_parte[:2],
                segunda_parte[:4] + primeira_parte[:3],
                segunda_parte[:3] + primeira_parte[:4],
                segunda_parte[:2] + primeira_parte[:5],
                intercalar_partes(primeira_parte, segunda_parte),
                intercalar_partes(segunda_parte, primeira_parte),
            ]

            for login in combinacoes:
                if len(login) == 7 and login not in candidatos:
                    candidatos.append(login)
                    
    nome_completo = "".join(partes)
    
    for i in range(len(nome_completo) - 6):
        login = nome_completo[i:i + 7]
    
        if len(login) == 7 and login not in candidatos:
            candidatos.append(login)
    
    return candidatos


def gerar_login(nome: str, logins_existentes: list[str]) -> str:
    candidatos = gerar_candidatos_login(nome)

    for candidato in candidatos:
        if candidato not in logins_existentes:
            return candidato

    raise ValueError("Não foi possível gerar um login único para o nome informado.")