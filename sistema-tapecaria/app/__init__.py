from flask import Flask
from .models import db
import os

def create_app():

    app = Flask(__name__)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "database", "database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SECRET_KEY"] = "sua_chave"

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app