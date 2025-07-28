from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .models import *
from .extensions import db
from .api import __all__ as blueprints


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix="/api")

    @app.route("/")
    def index():
        return {
            "message": "E-commerce API Server",
            "version": "1.0.0",
            "endpoints": {
                "api_base": "/api",
            }
        }
    
    return app
