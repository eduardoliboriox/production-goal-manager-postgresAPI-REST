from flask import Flask
from .config import Config
from .routes import pages, api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    return app
