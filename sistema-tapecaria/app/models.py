from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):

    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    cod_cliente = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)

    telefone = db.relationship(
        "TelefoneCliente",
        backref="cliente",
        uselist=False,
        cascade="all, delete"
    )

    endereco = db.relationship(
        "EnderecoCliente",
        backref="cliente",
        uselist=False,
        cascade="all, delete"
    )

    veiculos = db.relationship(
        "Veiculo",
        backref="cliente",
        cascade="all, delete"
    )


class TelefoneCliente(db.Model):

    __tablename__ = "telefones_cliente"

    id_telefone = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    telefone = db.Column(db.String(20), nullable=False)


class EnderecoCliente(db.Model):

    __tablename__ = "enderecos_cliente"

    id_endereco = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    rua = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(8))
    complemento = db.Column(db.String(100))


class Veiculo(db.Model):

    __tablename__ = "veiculos"

    id_veiculo = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    placa = db.Column(db.String(10))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(80))
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(30))