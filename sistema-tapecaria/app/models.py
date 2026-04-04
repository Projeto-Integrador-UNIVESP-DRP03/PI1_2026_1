from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =========================
# CLIENTES
# =========================
class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_cliente = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    
    telefones = db.relationship("TelefoneCliente", backref="cliente", lazy=True, cascade="all, delete-orphan")
    enderecos = db.relationship("EnderecoCliente", backref="cliente", lazy=True, cascade="all, delete-orphan")
    veiculos = db.relationship("Veiculo", backref="cliente", lazy=True, cascade="all, delete-orphan")


# =========================
# TELEFONES
# =========================
class TelefoneCliente(db.Model):
    __tablename__ = "telefones_cliente"

    id_telefone = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)


# =========================
# ENDEREÇOS
# =========================
class EnderecoCliente(db.Model):
    __tablename__ = "enderecos_cliente"

    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)

    rua = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(8))
    complemento = db.Column(db.String(100))


# =========================
# VEÍCULOS
# =========================
class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id_veiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)

    placa = db.Column(db.String(7), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(30))

    orcamentos = db.relationship("Orcamento", backref="veiculo", lazy=True)


# =========================
# CATÁLOGO
# =========================

class Tecido(db.Model):
    __tablename__ = "tecido"

    id_tecido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(30))
    descricao = db.Column(db.Text)


class Espuma(db.Model):
    __tablename__ = "espuma"

    id_espuma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)
    densidade = db.Column(db.String(20))
    descricao = db.Column(db.Text)


class Costura(db.Model):
    __tablename__ = "costura"

    id_costura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)


class Cor(db.Model):
    __tablename__ = "cor"

    id_cor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text)


# =========================
# ORÇAMENTO
# =========================
class Orcamento(db.Model):
    __tablename__ = "orcamento"

    id_orcamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_veiculo = db.Column(db.Integer, db.ForeignKey("veiculos.id_veiculo"), nullable=False)

    dat_orcamento = db.Column(db.Date, nullable=False)

    bool_original = db.Column(db.Boolean, default=False)
    bool_logo_prensada = db.Column(db.Boolean, default=False)

    qtd_bancos = db.Column(db.Integer, default=0)
    qtd_apoio_cabeca = db.Column(db.Integer, default=0)

    bool_espuma = db.Column(db.Boolean, default=False)

    valor = db.Column(db.Numeric(10,2), nullable=False)

    obs = db.Column(db.Text)

    pedidos = db.relationship("Pedido", backref="orcamento", lazy=True)
    tecidos = db.relationship("OrcamentoTecido")
    costuras = db.relationship("OrcamentoCostura")
    cores = db.relationship("OrcamentoCor")
    espumas = db.relationship("OrcamentoEspuma")


# =========================
# ITENS DO ORÇAMENTO
# =========================

class OrcamentoEspuma(db.Model):

    __tablename__ = "orcamento_espuma"

    id_orcamento_espuma = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_orcamento = db.Column(
        db.Integer,
        db.ForeignKey("orcamento.id_orcamento")
    )

    id_espuma = db.Column(
        db.Integer,
        db.ForeignKey("espuma.id_espuma")
    )

    obs_item = db.Column(db.String(200))

    espuma = db.relationship("Espuma")


class OrcamentoCostura(db.Model):

    __tablename__ = "orcamento_costura"

    id_orcamento_costura = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_orcamento = db.Column(
        db.Integer,
        db.ForeignKey("orcamento.id_orcamento")
    )

    id_costura = db.Column(
        db.Integer,
        db.ForeignKey("costura.id_costura")
    )

    obs_item = db.Column(db.String(200))

    costura = db.relationship("Costura")


class OrcamentoCor(db.Model):

    __tablename__ = "orcamento_cor"

    id_orcamento_cor = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_orcamento = db.Column(
        db.Integer,
        db.ForeignKey("orcamento.id_orcamento")
    )

    id_cor = db.Column(
        db.Integer,
        db.ForeignKey("cor.id_cor")
    )

    obs_item = db.Column(db.String(200))

    cor = db.relationship("Cor")


class OrcamentoTecido(db.Model):

    __tablename__ = "orcamento_tecido"

    id_orcamento_tecido = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_orcamento = db.Column(
        db.Integer,
        db.ForeignKey("orcamento.id_orcamento")
    )

    id_tecido = db.Column(
        db.Integer,
        db.ForeignKey("tecido.id_tecido")
    )

    obs_item = db.Column(db.String(200))

    tecido = db.relationship("Tecido")
# =========================
# PEDIDOS
# =========================
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_orcamento = db.Column(
        db.Integer,
        db.ForeignKey("orcamento.id_orcamento"),
        nullable=False
    )

    boolean_aceite_cliente = db.Column(db.Boolean, default=False)

    dat_aceite_cliente = db.Column(db.Date)
    data_inicio = db.Column(db.Date)
    data_conclusao = db.Column(db.Date)

    observacoes_pedido = db.Column(db.Text)

    aceite_cliente = db.Column(db.Boolean)

    status = db.Column(db.String(50))

    valor_total = db.Column(db.Float)

    metodo_pagamento = db.Column(db.String(50))