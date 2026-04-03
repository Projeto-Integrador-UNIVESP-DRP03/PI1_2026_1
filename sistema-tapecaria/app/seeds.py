from models import db, Clientes, TelefonesCliente, EnderecosCliente, Veiculos, Tecido, Espuma, Costura, Cor, Orcamento, OrcamentoTecido, OrcamentoEspuma, OrcamentoCostura, OrcamentoCor
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    # =========================
    # CLIENTES
    # =========================
    cliente1 = Clientes(cod_cliente="CLI001", nome="João da Silva")
    cliente2 = Clientes(cod_cliente="CLI002", nome="Maria Oliveira")
    cliente3 = Clientes(cod_cliente="CLI003", nome="Carlos Souza")
    db.session.add_all([cliente1, cliente2, cliente3])
    db.session.commit()

    # TELEFONES
    tel1 = TelefonesCliente(id_cliente=cliente1.id_cliente, telefone="(21)99999-1111")
    tel2 = TelefonesCliente(id_cliente=cliente2.id_cliente, telefone="(21)97777-3333")
    db.session.add_all([tel1, tel2])
    db.session.commit()

    # ENDEREÇOS
    end1 = EnderecosCliente(id_cliente=cliente1.id_cliente, rua="Rua das Flores", numero="123",
                            bairro="Centro", cidade="Volta Redonda", estado="RJ", cep="27260000", complemento="Apto 101")
    db.session.add(end1)
    db.session.commit()

    # VEÍCULOS
    veic1 = Veiculos(id_cliente=cliente1.id_cliente, placa="ABC1234", marca="Volkswagen", modelo="Gol", ano=2015, cor="Prata")
    db.session.add(veic1)
    db.session.commit()

    # CATÁLOGO DE ITENS
    tecido1 = Tecido(id_tecido="TEC001", material="Couro", descricao="Couro sintético preto")
    espuma1 = Espuma(id_espuma="ESP001", tipo="Poliuretano", densidade="D28", descricao="Espuma firme para assentos")
    costura1 = Costura(id_costura="COS001", tipo="Ponto reto", descricao="Costura tradicional")
    cor1 = Cor(id_cor="COR001", descricao="Preto")
    db.session.add_all([tecido1, espuma1, costura1, cor1])
    db.session.commit()

    # ORÇAMENTO
    orc1 = Orcamento(id_veiculo=veic1.id_veiculo, dat_orcamento="2026-04-01", bool_original=True,
                     qtd_bancos=5, qtd_apoio_cabeca=5, bool_espuma=True, valor=3500.00,
                     obs="Orçamento completo com couro e espuma D28")
    db.session.add(orc1)
    db.session.commit()

    # ITENS DO ORÇAMENTO
    orc_tecido1 = OrcamentoTecido(id_orcamento=orc1.id_orcamento, id_tecido=tecido1.id_tecido, obs_item="Couro sintético preto")
    orc_espuma1 = OrcamentoEspuma(id_orcamento=orc1.id_orcamento, id_espuma=espuma1.id_espuma, obs_item="Espuma firme nos bancos")
    orc_costura1 = OrcamentoCostura(id_orcamento=orc1.id_orcamento, id_costura=costura1.id_costura, obs_item="Costura tradicional")
    orc_cor1 = OrcamentoCor(id_orcamento=orc1.id_orcamento, id_cor=cor1.id_cor, obs_item="Linha preta")
    db.session.add_all([orc_tecido1, orc_espuma1, orc_costura1, orc_cor1])
    db.session.commit()
