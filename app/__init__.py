from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db.init_app(app)

    @app.route("/")
    def index():
        return "Server is running"

    return app
