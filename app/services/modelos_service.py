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


# 🔴 NOVA FUNÇÃO – PERDA DE PRODUÇÃO
def calcular_perda_producao(meta_hora, producao_real):
    """
    Ex:
    meta_hora = 200
    producao_real = 100
    """

    if producao_real >= meta_hora:
        return "Sem perda de produção"

    proporcao = producao_real / meta_hora
    minutos_perdidos = int((1 - proporcao) * 60)
    segundos = 0

    return f" Perda de Produção: {minutos_perdidos} minutos e {segundos:02d} segundos"

