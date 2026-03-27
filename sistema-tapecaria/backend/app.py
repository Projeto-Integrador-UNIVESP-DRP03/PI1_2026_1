from flask import Flask, render_template, request, redirect
import sqlite3
import os
import datetime
from flask_sqlalchemy import SQLAlchemy

# Conectando ao banco de dados SQLite usando SQLAlchemy, configurando a URI do banco de dados com base no caminho do arquivo e inicializando a extensão SQLAlchemy com a aplicação Flask
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
    rua         = db.Column(db.String(150), nullable=False)
    numero      = db.Column(db.String(10) , nullable=False)
    bairro      = db.Column(db.String(100), nullable=False)
    cidade      = db.Column(db.String(100), nullable=False)
    estado      = db.Column(db.String(2)  , nullable=False)
    cep         = db.Column(db.String(8)  , nullable=False)


def conectar(): # Função para conectar ao banco de dados SQLite, retornando a conexão estabelecida
    return sqlite3.connect("../database/database.db")
######

# Rota para a página inicial, renderizando o template de consulta
@app.route("/")
def home():
    return render_template("/consulta.html")

# Rota para a página de busca
# Rota para a página de busca
@app.route("/buscar", methods=["POST"])
def buscar():

    cod_cliente = request.form["cod_cliente"].upper()

    # buscar cliente
    cliente = Cliente.query.filter_by(
        cod_cliente=cod_cliente
    ).first()

    # se cliente existir
    if cliente:

        telefone = telefones_cliente.query.filter_by(
            id_cliente=cliente.id_cliente
        ).first()

        endereco = enderecos_cliente.query.filter_by(
            id_cliente=cliente.id_cliente
        ).first()

        veiculos = Veiculo.query.filter_by(
            id_cliente=cliente.id_cliente
        ).all()

        return render_template(
            "cliente.html",
            cliente=cliente,
            telefone=telefone,
            endereco=endereco,
            veiculos=veiculos
        )

    # se cliente não existir
    else:
        return render_template(
            "cadastro_cliente.html",
            cod_cliente=cod_cliente
        )


# Rota para listar os clientes, buscando todos os clientes do banco de dados e renderizando a página de lista de clientes com as informações dos clientes
@app.route("/clientes")
def listar_clientes():

    clientes = Cliente.query.all()
    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )
    
# Rota para deletar um cliente, recebendo o ID do cliente como parâmetro, buscando o cliente no banco de dados, deletando o cliente e redirecionando para a página de lista de clientes
@app.route("/deletar_cliente/<int:id_cliente>", methods=["POST"])
def deletar_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)
    telefone = telefones_cliente.query.filter_by(
        id_cliente=id_cliente
    ).first()
    endereco = enderecos_cliente.query.filter_by(
        id_cliente=id_cliente
    ).first()
    # deletar telefone
    if telefone:
        db.session.delete(telefone)
    # deletar endereço
    if endereco:
        db.session.delete(endereco)
    # deletar cliente
    db.session.delete(cliente)
    db.session.commit()

    return redirect("/clientes")

# Rota para editar um cliente, recebendo o ID do cliente como parâmetro, buscando o cliente no banco de dados e renderizando a página de edição de cliente com as informações do cliente
@app.route("/editar/<int:id>")
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    telefone = telefones_cliente.query.filter_by(
        id_cliente=id
    ).first()

    endereco = enderecos_cliente.query.filter_by(
        id_cliente=id
    ).first()

    return render_template(
        "editar_cliente.html",
        cliente=cliente,
        telefone=telefone,
        endereco=endereco
    )


@app.route("/atualizar_cliente/<int:id_cliente>", methods=["POST"])
def atualizar_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)

    telefone = telefones_cliente.query.filter_by(
        id_cliente=id_cliente
    ).first()

    endereco = enderecos_cliente.query.filter_by(
        id_cliente=id_cliente
    ).first()

    # atualizar cliente
    cliente.nome = request.form["nome"]

    # atualizar telefone
    if telefone:
        telefone.telefone = request.form["telefone"]

    # atualizar endereço
    if endereco:
        endereco.rua = request.form["rua"]
        endereco.numero = request.form["numero"]
        endereco.bairro = request.form["bairro"]
        endereco.cidade = request.form["cidade"]
        endereco.estado = request.form["estado"]
        endereco.cep = request.form["cep"]

    db.session.commit()

    return redirect(f"/editar/{id_cliente}")

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    cod_cliente = request.form["cod_cliente"]
    nome = request.form["nome"]
    telefone = request.form["telefone"]

    rua = request.form["rua"]
    numero = request.form["numero"]
    bairro = request.form["bairro"]
    cidade = request.form["cidade"]
    estado = request.form["estado"]
    cep = request.form["cep"]

    # inserir cliente
    novo_cliente = Cliente(
        cod_cliente=cod_cliente,
        nome=nome
    )

    db.session.add(novo_cliente)
    db.session.commit()

    # pegar id gerado
    id_cliente = novo_cliente.id_cliente

    # inserir telefone
    novo_telefone = telefones_cliente(
        id_cliente=id_cliente,
        telefone=telefone
    )

    db.session.add(novo_telefone)

    # inserir endereço
    novo_endereco = enderecos_cliente(
        id_cliente=id_cliente,
        rua=rua,
        numero=numero,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        cep=cep
    )

    db.session.add(novo_endereco)

    db.session.commit()

    return redirect("/clientes")


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