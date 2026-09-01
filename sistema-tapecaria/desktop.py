import os
import sys
import threading
import webbrowser
import time
import shutil
import secrets
from flask import Flask
from waitress import serve

# Configuração de caminhos para PyInstaller
if getattr(sys, 'frozen', False):
    # BASE_DIR é onde os arquivos estáticos/templates estão (extraídos pelo PyInstaller)
    BASE_DIR = sys._MEIPASS
    # EXE_DIR é onde o executável .exe reside fisicamente
    EXE_DIR = os.path.dirname(sys.executable)
    # DB_DIR deve ser fora do _MEIPASS para que os dados persistam
    DB_DIR = os.path.join(EXE_DIR, "instance")
    
    # Lógica de migração: Se o banco não existe na pasta do executável, copia o banco inicial que foi empacotado
    bundled_db = os.path.join(BASE_DIR, "instance", "database.db")
    local_db = os.path.join(DB_DIR, "database.db")
    
    if not os.path.exists(local_db):
        os.makedirs(DB_DIR, exist_ok=True)
        if os.path.exists(bundled_db):
            try:
                shutil.copy2(bundled_db, local_db)
            except Exception as e:
                print(f"Erro ao copiar banco inicial: {e}")
    
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, "instance")
    app = Flask(__name__)

# Importações dos módulos do sistema
from app.models import db
from app.routes import main

# Garante que o diretório do banco existe
os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.abspath(os.path.join(DB_DIR, "database.db")).replace("\\", "/")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# Inicializa o banco
db.init_app(app)

# Registra as rotas
app.register_blueprint(main)

# Garante que as tabelas existam
with app.app_context():
    db.create_all()

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print(f"Iniciando o Sistema ZitOS...")
    print(f"Banco de dados em: {db_path}")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Roda o servidor Waitress
    serve(app, host="127.0.0.1", port=5000)
