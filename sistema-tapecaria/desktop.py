import os
import sys
import threading
import webbrowser
import time
from flask import Flask
from waitress import serve

# Em um executável do Pyinstaller, o caminho base pode mudar
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    # O banco de dados vai ficar na mesma pasta do executável final
    DB_DIR = os.path.join(os.path.dirname(sys.executable), "instance")
    
    # IMPORTANTE: Quando o flask roda pelo pyinstaller, precisamos ajudar ele a encontrar os templates e estáticos
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, "instance")
    app = Flask(__name__)

# Importações dos módulos do sistema (devem vir depois para não dar erro de circular import caso haja)
from app.models import db
from app.routes import main

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "uma_chave_bem_secreta_e_unica"

# inicializa o banco
db.init_app(app)

# registra as rotas
app.register_blueprint(main)

# Garante que as tabelas sejam criadas se não existirem
with app.app_context():
    db.create_all()

def open_browser():
    # Espera o servidor iniciar
    time.sleep(1.5)
    # Abre no navegador padrão
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("Iniciando o Sistema de Tapeçaria...")
    
    # Inicia a thread para abrir o navegador
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Inicia o servidor usando waitress (próprio para produção/desktop no windows)
    serve(app, host="127.0.0.1", port=5000)
