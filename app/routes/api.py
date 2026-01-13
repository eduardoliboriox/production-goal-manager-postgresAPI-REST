from flask import Blueprint, request, jsonify
from app.services import modelos_service

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


@bp.route("/perdas", methods=["POST"])
def calcular_perda():
    return jsonify(modelos_service.calcular_perda(request.form))
