import sys
import os

# adiciona a raiz do projeto ao path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    print("Recriando banco de dados...")

    db.drop_all()
    db.create_all()

    print("Banco recriado com sucesso!")