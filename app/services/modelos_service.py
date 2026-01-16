from app.repositories import modelos_repository
import math

def listar_codigos():
    return modelos_repository.listar_codigos()

def listar():
    modelos = modelos_repository.listar_modelos()
    return [
        {
            "codigo": m["codigo"],
            "cliente": m["cliente"],
            "setor": m["setor"],
            "meta": float(m["meta"]),
            "fase": m["fase"]
        }
        for m in modelos
    ]

def cadastrar_modelo(dados):
    try:
        modelos_repository.inserir(dados)
        return {"sucesso": True, "mensagem": "Modelo cadastrado"}
    except Exception:
        return {"sucesso": False, "mensagem": "Código já existe"}

def excluir_modelo(dados):
    codigo = dados.get("codigo")

    if not codigo:
        return {
            "sucesso": False,
            "mensagem": "Código não informado"
        }

    try:
        modelos_repository.excluir(codigo)
        return {
            "sucesso": True,
            "mensagem": "Modelo excluído com sucesso"
        }
    except Exception:
        return {
            "sucesso": False,
            "mensagem": "Erro ao excluir modelo"
        }

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

def calcular_perda_producao(meta_hora, producao_real):
    meta_hora = float(meta_hora)
    producao_real = float(producao_real)

    if meta_hora <= 0:
        return {"erro": "Meta inválida"}

    if producao_real >= meta_hora:
        return {
            "tempo_perdido": "0 minutos e 00 segundos",
            "pecas_faltantes": 0
        }

    minutos_por_peca = 60 / meta_hora
    tempo_produzido = producao_real * minutos_por_peca
    tempo_perdido = 60 - tempo_produzido

    minutos = int(tempo_perdido)
    segundos = int(round((tempo_perdido - minutos) * 60))

    if segundos == 60:
        minutos += 1
        segundos = 0

    return {
        "tempo_perdido": f"{minutos} minutos e {segundos:02d} segundos",
        "pecas_faltantes": int(meta_hora - producao_real)
    }

def calcular_meta_smt(tempo_montagem, blank):

    tempo = float(tempo_montagem)
    blank = int(blank)

    if tempo <= 0 or blank <= 0:
        return {"sucesso": False, "erro": "Valores inválidos"}

    # 1) capacidade teórica por placa
    meta_teorica = 3600 / tempo

    # 2) aplica perda de 10%
    meta_com_perda_placa = meta_teorica * 0.9

    # 3) converte para blank
    meta_com_perda_blank = meta_com_perda_placa * blank

    # 4) GARANTE múltiplo exato do blank (NUNCA arredonda pra cima)
    meta_final = math.floor(meta_com_perda_blank / blank) * blank

    return {
        "sucesso": True,
        "dados": {
            "meta_hora": meta_final,
            "meta_teorica": round(meta_teorica, 2),
            "meta_com_perda": round(meta_com_perda_blank, 2)
        }
    }

def calcular_tempo_smt_inverso(meta_hora, blank):
    try:
        meta = float(meta_hora)
        blank = int(blank)

        if meta <= 0 or blank <= 0:
            return {"sucesso": False, "erro": "Valores inválidos"}

        tempo = (3600 * 0.9 * blank) / meta

        return {
            "sucesso": True,
            "dados": {
                "tempo_montagem": round(tempo, 2)
            }
        }

    except Exception:
        return {"sucesso": False, "erro": "Erro no cálculo inverso"}

def calculo_rapido(meta_hora, minutos, blank=None):
    placas = (meta_hora / 60) * minutos

    if not blank or blank <= 1:
        return {
            "placas": round(placas, 2)
        }

    blanks = math.floor(placas / blank)

    return {
        "blanks": blanks,
        "placas_reais": blanks * blank
    }



