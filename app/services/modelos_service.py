from app.repositories import modelos_repository

def listar_codigos():
    return modelos_repository.listar_codigos()


def listar_modelos():
    return modelos_repository.listar_modelos()


def cadastrar_modelo(dados):
    try:
        modelos_repository.inserir(dados)
        return {"sucesso": True, "mensagem": "Modelo cadastrado"}
    except Exception:
        return {"sucesso": False, "mensagem": "Código já existe"}


def calcular_meta(dados):
    meta = float(dados["meta_padrao"])
    pessoas_atual = int(dados["pessoas_atuais"])
    pessoas_padrao = int(dados["pessoas_padrao"])
    minutos = int(dados["minutos"])

    meta_ajustada = round(
        meta * (pessoas_atual / pessoas_padrao) * 0.85
    )

    qtd = round(meta_ajustada * (minutos / 60))

    return {
        "resultado": f"{minutos} min → {qtd} peças"
    }
