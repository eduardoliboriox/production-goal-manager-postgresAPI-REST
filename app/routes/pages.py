from flask import Blueprint, render_template
from app.services.modelos_service import listar_codigos

bp = Blueprint("pages", __name__)

@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html", codigos=listar_codigos())

@bp.route("/modelos")
def modelos():
    return render_template("modelos.html", codigos=listar_codigos())

@bp.route("/calculo")
def calculo():
    return render_template("calcular.html", codigos=listar_codigos())

@bp.route("/perdas")
def perdas():
    return render_template("perdas.html")
