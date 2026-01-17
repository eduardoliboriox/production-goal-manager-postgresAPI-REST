from flask import Flask
from .config import Config
from .routes import pages, api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    executar_migracao_forcada(app)  # 👈 ISSO É O QUE FALTAVA
    return app


def executar_migracao_forcada(app):
    with app.app_context():
        from .extensions import get_db
        with get_db() as conn:
            with conn.cursor() as cur:

                # REMOVE COLUNA ERRADA
                cur.execute("""
                    ALTER TABLE modelos
                    DROP COLUMN IF EXISTS meta;
                """)

                # ADICIONA AS CERTAS
                cur.execute("""
                    ALTER TABLE modelos
                    ADD COLUMN IF NOT EXISTS meta_padrao NUMERIC,
                    ADD COLUMN IF NOT EXISTS pessoas_padrao INTEGER,
                    ADD COLUMN IF NOT EXISTS tempo_montagem NUMERIC,
                    ADD COLUMN IF NOT EXISTS fase TEXT;
                """)

            conn.commit()


app = create_app()
