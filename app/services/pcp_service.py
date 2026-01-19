from datetime import datetime, timedelta
import math

# ======================================================
# DEFINIÇÃO DOS TURNOS
# ======================================================
TURNOS = [
    # ---------- 1º TURNO ----------
    {"turno": 1, "ref": "H-01", "inicio": "07:00", "fim": "08:00", "refeicao": False},
    {"turno": 1, "ref": "H-02", "inicio": "08:00", "fim": "09:00", "refeicao": False},
    {"turno": 1, "ref": "H-03", "inicio": "09:00", "fim": "10:00", "refeicao": False},
    {"turno": 1, "ref": "H-04", "inicio": "10:00", "fim": "11:00", "refeicao": False},
    {"turno": 1, "ref": "H-05", "inicio": "11:00", "fim": "12:00", "refeicao": True},
    {"turno": 1, "ref": "H-06", "inicio": "12:00", "fim": "13:00", "refeicao": False},
    {"turno": 1, "ref": "H-07", "inicio": "13:00", "fim": "14:00", "refeicao": False},
    {"turno": 1, "ref": "H-08", "inicio": "14:00", "fim": "15:00", "refeicao": False},
    {"turno": 1, "ref": "H-09", "inicio": "15:00", "fim": "16:00", "refeicao": False},
    {"turno": 1, "ref": "H-10", "inicio": "16:00", "fim": "16:48", "refeicao": False},

    # ---------- 2º TURNO ----------
    {"turno": 2, "ref": "H-01", "inicio": "16:48", "fim": "17:00", "refeicao": False},
    {"turno": 2, "ref": "H-02", "inicio": "17:00", "fim": "18:00", "refeicao": False},
    {"turno": 2, "ref": "H-03", "inicio": "18:00", "fim": "19:00", "refeicao": False},
    {"turno": 2, "ref": "H-04", "inicio": "19:00", "fim": "20:00", "refeicao": False},
    {"turno": 2, "ref": "H-05", "inicio": "20:00", "fim": "21:00", "refeicao": True},
    {"turno": 2, "ref": "H-06", "inicio": "21:00", "fim": "22:00", "refeicao": False},
    {"turno": 2, "ref": "H-07", "inicio": "22:00", "fim": "23:00", "refeicao": False},
    {"turno": 2, "ref": "H-08", "inicio": "23:00", "fim": "00:00", "refeicao": False},
    {"turno": 2, "ref": "H-09", "inicio": "00:00", "fim": "01:00", "refeicao": False},
    {"turno": 2, "ref": "H-10", "inicio": "01:00", "fim": "02:00", "refeicao": False},
    {"turno": 2, "ref": "H-11", "inicio": "02:00", "fim": "02:35", "refeicao": False},

    # ---------- 3º TURNO ----------
    {"turno": 3, "ref": "H-01", "inicio": "02:35", "fim": "03:00", "refeicao": False},
    {"turno": 3, "ref": "H-02", "inicio": "03:00", "fim": "04:00", "refeicao": True},
    {"turno": 3, "ref": "H-03", "inicio": "04:00", "fim": "05:00", "refeicao": False},
    {"turno": 3, "ref": "H-04", "inicio": "05:00", "fim": "06:00", "refeicao": False},
    {"turno": 3, "ref": "H-05", "inicio": "06:00", "fim": "07:00", "refeicao": False},
]

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================
def _parse_time(hhmm):
    return datetime.strptime(hhmm, "%H:%M")

# ======================================================
# CÁLCULO PRINCIPAL
# ======================================================
def calcular_pcp(
    total_op: int,
    produzido: int,
    hora_inicio: str,
    meta_hora: float,
    blank: int,
    turnos_aplicados: list,
    considerar_refeicao: bool
):
    restante = max(total_op - produzido, 0)
    atual = _parse_time(hora_inicio)
    timeline = []

    for bloco in TURNOS:

        # 🔹 Turno não selecionado
        if bloco["turno"] not in turnos_aplicados:
            continue

        # 🔹 Pula refeição se usuário marcar "Não"
        if bloco["refeicao"] and not considerar_refeicao:
            continue

        ini = _parse_time(bloco["inicio"])
        fim = _parse_time(bloco["fim"])

        if atual >= fim:
            continue

        inicio_real = max(atual, ini)
        minutos_disponiveis = (fim - inicio_real).total_seconds() / 60

        if minutos_disponiveis <= 0:
            continue

        # 🔹 Capacidade bruta
        capacidade = (meta_hora / 60) * minutos_disponiveis

        # 🔹 Aplica blank apenas se > 1
        if blank and blank > 1:
            capacidade = math.floor(capacidade / blank) * blank

        capacidade = int(capacidade)

        if capacidade <= 0:
            continue

        produzido_bloco = min(capacidade, restante)
        restante -= produzido_bloco

        timeline.append({
            "turno": bloco["turno"],
            "referencia": bloco["ref"],
            "inicio": inicio_real.strftime("%H:%M"),
            "fim": fim.strftime("%H:%M"),
            "produzido": produzido_bloco
        })

        # 🔹 Finalizou aqui
        if restante <= 0:
            minutos_necessarios = (produzido_bloco / meta_hora) * 60
            fim_real = inicio_real + timedelta(minutes=minutos_necessarios)

            return {
                "conclusao": fim_real.strftime("%H:%M"),
                "timeline": timeline
            }

        atual = fim

    return {
        "conclusao": None,
        "timeline": timeline,
        "erro": "Produção não finalizada nos turnos selecionados"
    }
