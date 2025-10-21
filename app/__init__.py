from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .api import __all__ as api_blueprints
from .client import __all__ as client_blueprints
from .config import Config
from .models import *
from .extensions import db
from .api import __all__ as blueprints


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize Swagger/Flasgger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "title": "E-commerce API Documentation",
        "version": "1.0.0",
        "description": "RESTful API for E-commerce platform with authentication, products, orders, and payment management",
        "contact": {
            "name": "E-commerce API Support",
            "url": "https://github.com/HuynhPham0302/Ecommerce",
        },
    }
    swagger = Swagger(app, config=swagger_config)

    # Initialize database
    db.init_app(app)

    # Register API blueprints
    for bp in api_blueprints:
        app.register_blueprint(bp, url_prefix="/api")

    # Register client blueprints
    for bp in client_blueprints:
        app.register_blueprint(bp, url_prefix="/")

    @app.route("/")
    def index():
        return {
            "message": "E-commerce API Server",
            "version": "1.0.0",
            "endpoints": {
                "api_base": "/api",
            },
        }

    return app
