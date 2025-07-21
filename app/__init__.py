from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .models import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    app.config.from_object(Config)


    @app.route("/")
    def index():
        return "Server is running"
    
    with app.context():
        db.create_all()

    return app
