from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"  # padronizei no plural

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
        db.ForeignKey("clientes.id_cliente"),  # corrigido
        nullable=False
    )
    telefone = db.Column(db.String(20), nullable=False)


class EnderecoCliente(db.Model):
    __tablename__ = "enderecos_cliente"

    id_endereco = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),  # corrigido
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
    __tablename__ = "veiculos"  # padronizei no plural

    id_veiculo = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),  # corrigido
        nullable=False
    )
    placa = db.Column(db.String(10), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(30))


class OrdemServico(db.Model):
    __tablename__ = "ordens_servico"  # plural para consistência

    id_os = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_veiculo = db.Column(db.Integer, db.ForeignKey("veiculos.id_veiculo"), nullable=False)  # corrigido
    data_abertura = db.Column(db.Date)
    quantidade_bancos = db.Column(db.Integer)
    padrao_veiculo = db.Column(db.Boolean)
    personalizacao_igual = db.Column(db.Boolean)
    observacoes = db.Column(db.String(1020))
    
    veiculo = relationship("Veiculo", backref="ordens_servico")
    bancos = relationship("Banco", back_populates="ordem_servico")


class Espuma(db.Model):
    __tablename__ = "espumas"

    id_espuma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String)
    densidade = db.Column(db.String(20))
    descricao = db.Column(db.String(1020))

    bancos = relationship("Banco", back_populates="espuma")


class Banco(db.Model):
    __tablename__ = "bancos"

    id_banco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_os = db.Column(db.Integer, db.ForeignKey("ordens_servico.id_os"), nullable=False)  # corrigido
    posicao = db.Column(db.String(100))
    troca_espuma = db.Column(db.Boolean)
    id_espuma = db.Column(db.Integer, db.ForeignKey("espumas.id_espuma"))

    ordem_servico = relationship("OrdemServico", back_populates="bancos")
    espuma = relationship("Espuma", back_populates="bancos")
    personalizacoes = relationship("Personalizacao", back_populates="banco")
    tecidos = relationship("BancoTecido", back_populates="banco")


class Costura(db.Model):
    __tablename__ = "costuras"

    id_costura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(1020))

    personalizacoes = relationship("Personalizacao", back_populates="costura")


class Cor(db.Model):
    __tablename__ = "cores"

    id_cor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)

    personalizacoes = relationship("Personalizacao", back_populates="cor_linha")
    banco_tecidos = relationship("BancoTecido", back_populates="cor")


class Personalizacao(db.Model):
    __tablename__ = "personalizacoes"

    id_personalizacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_banco = db.Column(db.Integer, db.ForeignKey("bancos.id_banco"), nullable=False)
    id_costura = db.Column(db.Integer, db.ForeignKey("costuras.id_costura"))
    id_cor_linha = db.Column(db.Integer, db.ForeignKey("cores.id_cor"))

    banco = relationship("Banco", back_populates="personalizacoes")
    costura = relationship("Costura", back_populates="personalizacoes")
    cor_linha = relationship("Cor", back_populates="personalizacoes")


class Tecido(db.Model):
    __tablename__ = "tecidos"

    id_tecido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    material = db.Column(db.String(100))
    fornecedor = db.Column(db.String(100))

    banco_tecidos = relationship("BancoTecido", back_populates="tecido")


class BancoTecido(db.Model):
    __tablename__ = "banco_tecidos"

    id_banco = db.Column(db.Integer, db.ForeignKey("bancos.id_banco"), primary_key=True)
    id_tecido = db.Column(db.Integer, db.ForeignKey("tecidos.id_tecido"), primary_key=True)
    parte_banco = db.Column(db.String(100), primary_key=True)
    id_cor = db.Column(db.Integer, db.ForeignKey("cores.id_cor"))

    banco = relationship("Banco", back_populates="tecidos")
    tecido = relationship("Tecido", back_populates="banco_tecidos")
    cor = relationship("Cor", back_populates="banco_tecidos")
