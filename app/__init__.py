from flask import Flask
from .config import Config
from .routes import pages, api
from .extensions import get_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    criar_tabelas(app)
    return app


def criar_tabelas(app):
    with app.app_context():
        from .extensions import get_db
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS modelos (
                        id SERIAL PRIMARY KEY,
                        codigo TEXT UNIQUE NOT NULL,
                        cliente TEXT,
                        setor TEXT,
                        meta_padrao NUMERIC,
                        pessoas_padrao INTEGER
                    )
                """)
