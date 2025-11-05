from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = "producao.db"

# Evitar bloqueios de rede/proxy
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

# =====================
# BANCO DE DADOS
# =====================

def inicializar_bd():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS modelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            cliente TEXT,
            setor TEXT,
            meta_padrao REAL,
            pessoas_padrao INTEGER
        )
    """)
    conn.commit()
    conn.close()

inicializar_bd()


def carregar_codigos():
    """Carrega todos os códigos para popular dropdowns"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT codigo FROM modelos ORDER BY codigo")
    codigos = [r[0] for r in cur.fetchall()]
    conn.close()
    return codigos

# =====================
# ROTAS PRINCIPAIS
# =====================

@app.route("/")
def index():
    """Página inicial"""
    return render_template("index.html", codigos=carregar_codigos())

# --- CADASTRAR ---
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    codigo = request.form["codigo"]
    cliente = request.form["cliente"]
    setor = request.form["setor"]
    meta = request.form["meta"]
    pessoas = request.form["pessoas"]

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO modelos (codigo, cliente, setor, meta_padrao, pessoas_padrao)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, cliente, setor, meta, pessoas))
        conn.commit()
        msg = f"✅ Modelo {codigo} cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        msg = "⚠️ Erro: código já cadastrado!"
    finally:
        conn.close()

    return render_template("index.html", codigos=carregar_codigos(), mensagem=msg)

# --- EDITAR ---
@app.route("/editar", methods=["POST"])
def editar():
    codigo = request.form["codigo"]
    nova_meta = request.form.get("nova_meta")
    novas_pessoas = request.form.get("novas_pessoas")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM modelos WHERE codigo = ?", (codigo,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return render_template("index.html", codigos=carregar_codigos(), mensagem="⚠️ Modelo não encontrado!")

    if nova_meta:
        cur.execute("UPDATE modelos SET meta_padrao = ? WHERE codigo = ?", (nova_meta, codigo))
    if novas_pessoas:
        cur.execute("UPDATE modelos SET pessoas_padrao = ? WHERE codigo = ?", (novas_pessoas, codigo))
    conn.commit()
    conn.close()
    return render_template("index.html", codigos=carregar_codigos(), mensagem=f"✅ Modelo {codigo} atualizado com sucesso!")

# --- EXCLUIR ---
@app.route("/excluir", methods=["POST"])
def excluir():
    codigo = request.form["codigo"]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM modelos WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()
    return render_template("index.html", codigos=carregar_codigos(), mensagem=f"🗑️ Modelo {codigo} excluído com sucesso!")

# --- LISTAR (AJAX JSON) ---
@app.route("/listar")
def listar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT codigo, cliente, setor, meta_padrao, pessoas_padrao FROM modelos ORDER BY codigo")
    dados = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(dados)

# --- CALCULAR META ---
@app.route("/calcular", methods=["POST"])
def calcular():
    codigo = request.form["codigo"]
    pessoas_atuais = int(request.form["pessoas_atuais"])
    minutos = int(request.form["minutos"])

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT meta_padrao, pessoas_padrao FROM modelos WHERE codigo = ?", (codigo,))
    r = cur.fetchone()
    conn.close()

    if not r:
        return jsonify({"resultado": "⚠️ Modelo não encontrado!"})

    meta_padrao, pessoas_padrao = r

    # Cálculo proporcional
    if pessoas_atuais != pessoas_padrao:
        meta_ajustada = round(meta_padrao * (pessoas_atuais / pessoas_padrao) * 0.85)
    else:
        meta_ajustada = round(meta_padrao)

    qtd_minutos = round(meta_ajustada * (minutos / 60))
    resultado = f"✅ Meta ajustada: <b>{meta_ajustada}</b> peças/hora<br>{minutos} minutos → <b>{qtd_minutos}</b> peças"

    return jsonify({"resultado": resultado})


# =====================
# EXECUTAR LOCALMENTE / REDE
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
