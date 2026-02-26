from app.repositories import modelos_repository
from app.repositories.modelos_repository import buscar_ultimo_modelo
import math


LINHAS_VALIDAS = {
    "SMD-01", "SMD-02", "SMD-03", "SMD-04", "SMD-05",
    "SMD-06", "SMD-07", "SMD-08", "SMD-09"
}


def resumo_dashboard():
    modelos = modelos_repository.listar_modelos()

    total = len(modelos)

    por_setor = {}
    por_fase = {}

    for m in modelos:
        setor = m.get("setor")
        fase = m.get("fase")

        if setor:
            por_setor[setor] = por_setor.get(setor, 0) + 1

        if fase:
            por_fase[fase] = por_fase.get(fase, 0) + 1

    ultimo_modelo = buscar_ultimo_modelo()

    return {
        "total_modelos": total,
        "por_setor": por_setor,
        "por_fase": por_fase,
        "ultimo_modelo": ultimo_modelo
    }


def listar_codigos():
    return modelos_repository.listar_codigos()


def listar():
    modelos = modelos_repository.listar_modelos()
    return [
        {
            "codigo": m["codigo"],
            "cliente": m["cliente"],
            "setor": m["setor"],
            "linha": m["linha"],
            "meta": float(m["meta_padrao"]) if m["meta_padrao"] is not None else 0,
            "tempo_montagem": m["tempo_montagem"],
            "blank": m["blank"],
            "fase": m["fase"]
        }
        for m in modelos
    ]


def cadastrar_modelo(dados):
    linha = (dados.get("linha") or "").strip()
    if not linha:
        return {"sucesso": False, "mensagem": "Linha não informada"}
    if linha not in LINHAS_VALIDAS:
        return {"sucesso": False, "mensagem": "Linha inválida"}

    try:
        modelos_repository.inserir(dados)
        return {"sucesso": True, "mensagem": "Modelo cadastrado"}
    except Exception as e:
        print("ERRO AO CADASTRAR:", e)
        # Ex.: violação do unique (codigo,fase,linha)
        return {"sucesso": False, "mensagem": str(e)}


def excluir_modelo(dados):
    codigo = (dados.get("codigo") or "").strip()
    fase = (dados.get("fase") or "").strip()
    linha = (dados.get("linha") or "").strip()

    if not codigo or not fase or not linha:
        return {"sucesso": False, "mensagem": "Código, fase e linha são obrigatórios"}

    try:
        modelos_repository.excluir(codigo, fase, linha)
        return {"sucesso": True, "mensagem": "Modelo excluído com sucesso"}
    except Exception as e:
        print("ERRO AO EXCLUIR:", e)
        return {"sucesso": False, "mensagem": "Erro ao excluir modelo"}


def atualizar_modelo(dados):
    codigo = (dados.get("codigo") or "").strip()
    fase = (dados.get("fase") or "").strip()
    linha = (dados.get("linha") or "").strip()

    if not codigo or not fase or not linha:
        return {"sucesso": False, "mensagem": "Código, fase e linha são obrigatórios"}

    campos = {}

    if dados.get("meta_padrao"):
        campos["meta_padrao"] = float(dados["meta_padrao"])

    if dados.get("tempo_montagem"):
        campos["tempo_montagem"] = float(dados["tempo_montagem"])

    if dados.get("blank"):
        campos["blank"] = str(dados["blank"]).strip()

    if dados.get("novo_codigo"):
        campos["codigo"] = str(dados["novo_codigo"]).strip()

    if not campos:
        return {"sucesso": False, "mensagem": "Nada para atualizar"}

    modelos_repository.atualizar(codigo, fase, linha, campos)
    return {"sucesso": True}


# ====== Cálculos (mantidos) ======

def calcular_meta(dados):
    meta = float(dados["meta_padrao"])
    pessoas_atual = int(dados["pessoas_atuais"])
    pessoas_padrao = int(dados["pessoas_padrao"])
    minutos = int(dados["minutos"])

    meta_ajustada = round(
        meta * (pessoas_atual / pessoas_padrao) * 0.85
    )

    qtd = round(meta_ajustada * (minutos / 60))

    return {"resultado": f"{minutos} min → {qtd} peças"}


def calcular_perda_producao(meta_hora, producao_real):
    meta_hora = float(meta_hora)
    producao_real = float(producao_real)

    if meta_hora <= 0:
        return {"erro": "Meta inválida"}

    if producao_real >= meta_hora:
        return {"tempo_perdido": "0 minutos e 00 segundos", "pecas_faltantes": 0}

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

    # meta_teorica = capacidade bruta por hora SEM 10% (em BLANKS/H)
    meta_teorica = 3600 / tempo

    # aplica 10% de perda (em blanks/h)
    meta_com_perda_placa = meta_teorica * 0.9

    # converte para placas/h (considerando placas por blank)
    meta_com_perda_blank = meta_com_perda_placa * blank

    # arredonda para múltiplos de blank (placas/h)
    meta_final = math.floor(meta_com_perda_blank / blank) * blank

    return {
        "sucesso": True,
        "dados": {
            "meta_hora": meta_final,  # placas/h (operacional, com 10% e múltiplo do blank)
            "meta_teorica": round(meta_teorica, 2),  # blanks/h (capacidade teórica bruta)
            "meta_teorica_placas": round(meta_teorica * blank, 2),  # placas/h (capacidade teórica bruta)
            "meta_com_perda": round(meta_com_perda_blank, 2)  # placas/h (com 10%, antes do múltiplo)
        }
    }


def calcular_tempo_smt_inverso(meta_hora, blank):
    try:
        meta = float(meta_hora)
        blank = int(blank)

        if meta <= 0 or blank <= 0:
            return {"sucesso": False, "erro": "Valores inválidos"}

        tempo = (3600 * 0.9 * blank) / meta

        return {"sucesso": True, "dados": {"tempo_montagem": round(tempo, 2)}}
    except Exception:
        return {"sucesso": False, "erro": "Erro no cálculo inverso"}


def calculo_rapido(meta_hora, minutos, blank=None):
    placas = (meta_hora / 60) * minutos

    if not blank or blank <= 1:
        return {"placas": round(placas, 2)}

    blanks = math.floor(placas / blank)

    return {"blanks": blanks, "placas_reais": blanks * blank}
