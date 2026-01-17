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
                SELECT
                    codigo,
                    cliente,
                    setor,
                    meta_padrao,
                    pessoas_padrao,
                    tempo_montagem,
                    fase
                FROM modelos
                ORDER BY codigo
            """)
            return cur.fetchall()

def inserir(dados):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO modelos (
                    codigo,
                    cliente,
                    setor,
                    meta_padrao,
                    tempo_montagem,
                    fase
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                dados["codigo"],
                dados["cliente"],
                dados["setor"],
                dados["meta_padrao"],
                dados["tempo_montagem"],
                dados["fase"]
            ))
        conn.commit()


def excluir(codigo):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM modelos WHERE codigo = %s", (codigo,))
        conn.commit()

def atualizar_meta(codigo, nova_meta):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE modelos SET meta_padrao = %s WHERE codigo = %s",
                (nova_meta, codigo)
            )
        conn.commit()
