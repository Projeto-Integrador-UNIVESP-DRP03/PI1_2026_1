import os
from flask import Flask
from app.models import db
from app.routes import main


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(BASE_DIR, "database", "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "uma_chave_bem_secreta_e_unica"
# inicializa o banco
db.init_app(app)

# registra as rotas
app.register_blueprint(main)

# para debug
#print(app.url_map)

#if __name__ == "__main__":
#    app.run(debug=True)
    
# para abrir a aplicação sem o modo debug, use o comando abaixo    
if __name__ == "__main__":
    app.run(debug=False)