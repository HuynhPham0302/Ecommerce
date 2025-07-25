from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .models import *
from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)


    @app.route("/")
    def index():
        return "Server is running"
    
    with app.app_context():
        db.create_all()

    return app
