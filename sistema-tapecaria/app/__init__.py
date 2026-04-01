from flask import Flask
from .models import db
import os
import secrets

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "database", "database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Usa variável de ambiente SECRET_KEY
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(32)) or "minha_chave_dev"
   
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    print("SECRET_KEY carregada:", app.config["SECRET_KEY"])
    return app
