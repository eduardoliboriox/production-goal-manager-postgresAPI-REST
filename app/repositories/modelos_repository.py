from app.extensions import get_db


def listar_codigos():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT codigo FROM modelos ORDER BY codigo")
            return [r["codigo"] for r in cur.fetchall()]


def listar_modelos():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    codigo,
                    cliente,
                    setor,
                    linha,
                    meta_padrao,
                    tempo_montagem,
                    blank,
                    fase,
                    criado_em
                FROM modelos
                ORDER BY criado_em DESC
            """)
            return cur.fetchall()


def buscar_ultimo_modelo():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT codigo
                FROM modelos
                ORDER BY criado_em DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            return row["codigo"] if row else None


def inserir(dados):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO modelos (
                    codigo,
                    cliente,
                    setor,
                    linha,
                    meta_padrao,
                    tempo_montagem,
                    blank,
                    fase
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["codigo"],
                dados["cliente"],
                dados["setor"],
                dados["linha"],
                dados["meta_padrao"],
                dados.get("tempo_montagem"),
                dados["blank"],
                dados["fase"]
            ))
        conn.commit()


def excluir(codigo, fase, linha):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM modelos WHERE codigo = %s AND fase = %s AND linha = %s",
                (codigo, fase, linha)
            )
        conn.commit()


def atualizar(codigo, fase, linha, campos):
    sets = ", ".join(f"{k} = %s" for k in campos)
    valores = list(campos.values()) + [codigo, fase, linha]

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE modelos
                SET {sets}
                WHERE codigo = %s AND fase = %s AND linha = %s
                """,
                valores
            )
        conn.commit()
