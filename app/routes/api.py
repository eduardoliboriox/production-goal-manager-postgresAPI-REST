from flask import Blueprint, request, jsonify
from app.services import modelos_service
from app.services.modelos_service import calcular_perda_producao, calcular_meta_smt, calcular_tempo_smt_inverso

bp = Blueprint("api", __name__)

@bp.route("/modelos", methods=["GET"])
def listar():
    return jsonify({"data": modelos_service.listar_modelos()})

@bp.route("/modelos", methods=["POST"])
def cadastrar():
    dados = request.form
    return jsonify(modelos_service.cadastrar_modelo(dados))

@bp.route("/modelos/calcular", methods=["POST"])
def calcular_meta():
    return jsonify(modelos_service.calcular_meta(request.form))

@bp.route("/calcular_perda", methods=["POST"])
def calcular_perda():
    meta_hora = float(request.form.get("meta_hora"))
    producao_real = float(request.form.get("producao_real"))

    resultado = calcular_perda_producao(meta_hora, producao_real)

    return jsonify(resultado)

@bp.route("/smt/calcular_meta", methods=["POST"])
def api_calcular_meta_smt():
    tempo = request.form.get("tempo_montagem")
    blank = request.form.get("blank")

    if not tempo or not blank:
        return jsonify({"erro": "Tempo de montagem e blank são obrigatórios"}), 400

    return jsonify(calcular_meta_smt(tempo, blank))

@bp.route("/smt/calcular_tempo", methods=["POST"])
def api_calcular_tempo_smt():
    meta = request.form.get("meta_hora")
    blank = request.form.get("blank")

    if not meta or not blank:
        return jsonify({"erro": "Meta hora e blank são obrigatórios"}), 400

    return jsonify(calcular_tempo_smt_inverso(meta, blank))

@bp.route("/modelos/calculo_rapido", methods=["POST"])
def api_calculo_rapido():
    try:
        meta_hora = float(request.form.get("meta_hora"))
        minutos = float(request.form.get("minutos"))
        blank = request.form.get("blank")

        if blank:
            blank = int(blank)
        else:
            blank = None

        resultado = modelos_service.calculo_rapido(
            meta_hora=meta_hora,
            minutos=minutos,
            blank=blank
        )

        return jsonify({
            "sucesso": True,
            "dados": resultado
        })

    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": "Erro no cálculo rápido"
        }), 400






