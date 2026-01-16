from app.extensions import get_db

def listar_codigos():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT codigo FROM modelos ORDER BY codigo")
            return [r["codigo"] for r in cur.fetchall()]

def listar_modelos():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT codigo, cliente, setor, meta, fase
                FROM modelos
                ORDER BY codigo
            """)
            return cur.fetchall()


def inserir(dados):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO modelos (codigo, cliente, setor, meta, fase)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dados["codigo"],
                dados["cliente"],
                dados["setor"],
                dados["meta"],
                dados["fase"]
            ))
