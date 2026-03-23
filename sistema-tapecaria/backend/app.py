from flask import Flask, render_template, request, redirect
import sqlite3
import os
import datetime
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../database/database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

# criando as classes para representar as tabelas do banco de dados usando SQLAlchemy
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    cod_cliente = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)

class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id_veiculo = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    placa = db.Column(db.String(10), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20), nullable=False)

class telefones_cliente(db.Model):
    __tablename__ = 'telefones_cliente'
    id_telefone = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    
class enderecos_cliente(db.Model):
    __tablename__ = 'enderecos_cliente'
    id_endereco = db.Column(db.Integer, primary_key=True)
    id_cliente  = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    endereco    = db.Column(db.String(200), nullable=False)
    rua         = db.Column(db.String(150), nullable=False)
    numero      = db.Column(db.String(10) , nullable=False)
    bairro      = db.Column(db.String(100), nullable=False)
    cidade      = db.Column(db.String(100), nullable=False)
    estado      = db.Column(db.String(2)  , nullable=False)
    cep         = db.Column(db.String(8)  , nullable=False)


def conectar(): # Função para conectar ao banco de dados SQLite, retornando a conexão estabelecida
    return sqlite3.connect("../database/database.db")


@app.route("/")
def home():
    return render_template("/consulta.html")


@app.route("/buscar", methods=["POST"])
# função para buscar um cliente no banco de dados com base no código do cliente fornecido pelo usuário, e renderizar a página de cliente com as informações do cliente e seus veículos, ou redirecionar para a página de cadastro se o cliente não for encontrado
def buscar():
    cod_cliente = request.form["cod_cliente"].upper() # obtém o código do cliente enviado pelo formulário na página de consulta

    conn = conectar() # conecta ao banco de dados usando a função conectar() definida anteriormente
    cursor = conn.cursor() # cria um cursor para executar comandos SQL no banco de dados

    cursor.execute("SELECT * FROM clientes WHERE cod_cliente = ?", (cod_cliente,)) # executa uma consulta SQL para buscar um cliente com o código fornecido, usando um parâmetro para evitar injeção de SQL
    cliente = cursor.fetchone()
    

    if cliente:
        cursor.execute("SELECT * FROM veiculos WHERE id_cliente = ?", (cliente[0],))
        veiculos = cursor.fetchall()

        return render_template(
            "cliente.html",
            cliente=cliente,
            veiculos=veiculos
        )
    else:
        return render_template("/cadastro_cliente.html", cod_cliente=cod_cliente)


@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    nome = request.form["nome"]
    cod_cliente = request.form["cod_cliente"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, cod_cliente) VALUES (?, ?)",
        (nome, cod_cliente)
    )

    conn.commit()

    return redirect("/")


# Adicionar veículo para um cliente específico, recebendo os dados do veículo através de um formulário e inserindo-os na tabela de veículos do banco de dados, associando o veículo ao cliente pelo ID do cliente
@app.route("/adicionar_veiculo", methods=["POST"])
def adicionar_veiculo():

    id_cliente = request.form["id_cliente"]
    placa = request.form["placa"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    ano = request.form["ano"]
    cor = request.form["cor"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO veiculos
        (id_cliente, placa, marca, modelo, ano, cor)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (id_cliente, placa, marca, modelo, ano, cor)
    )

    conn.commit()

    return redirect("/")


app.run(debug=True)