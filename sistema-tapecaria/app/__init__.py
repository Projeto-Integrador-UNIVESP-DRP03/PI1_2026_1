from flask import Flask
from .models import db
import os
import secrets


def create_app():
    app = Flask(__name__)

    # Diretório base do projeto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Caminho da pasta instance
    instance_path = os.path.join(BASE_DIR, "..", "instance")

    # Garante que a pasta instance exista
    os.makedirs(instance_path, exist_ok=True)

    # Caminho do banco
    db_path = os.path.join(instance_path, "database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SECRET KEY
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        secrets.token_hex(32)
    )

    # Inicializa banco
    db.init_app(app)

    # Registra rotas
    from .routes import main
    app.register_blueprint(main)

    return app