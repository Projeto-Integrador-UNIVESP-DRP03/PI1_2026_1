import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import create_app
from app.models import db, Tecido, Espuma, Costura, Cor

app = create_app()

with app.app_context():

    print("Inserindo dados de catálogo...")

    # =========================
    # TECIDOS
    # =========================

    tecidos = [
        Tecido(material="Courvim", cor="04", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="09", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="05", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="17", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="13", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="24", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="HB20", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="32", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="11", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="02", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="25", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="21", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Courvim", cor="22", descricao="Couro sintético resistente para bancos automotivos."),
        Tecido(material="Couro", cor="04", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="09", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="05", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="17", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="13", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="24", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="HB20", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="32", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="Terracota", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="11", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="21", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="02", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="25", descricao="Couro Legítimo."),
        Tecido(material="Couro", cor="22", descricao="Couro Legítimo.")
    ]

    # =========================
    # ESPUMAS
    # =========================

    espumas = [
        Espuma(tipo="Espuma D28", densidade="28", descricao="Espuma macia utilizada principalmente em encostos."),
        Espuma(tipo="Espuma D33", densidade="33", descricao="Espuma de média densidade utilizada em assentos."),
        Espuma(tipo="Espuma D45", densidade="45", descricao="Espuma de alta densidade para maior resistência e durabilidade."),
        Espuma(tipo="Espuma Soft", densidade="26", descricao="Espuma confortável utilizada em acabamentos premium."),
        Espuma(tipo="Espuma Alta Resiliência", densidade="40", descricao="Espuma de alta performance com maior recuperação."),
    ]

    # =========================
    # COSTURAS
    # =========================

    costuras = [
        Costura(tipo="Costura Simples", descricao="Costura padrão utilizada em bancos originais."),
        Costura(tipo="Costura Dupla", descricao="Costura reforçada com duas linhas paralelas."),
        Costura(tipo="Costura Diamante", descricao="Costura em padrão losango utilizada em bancos personalizados."),
        Costura(tipo="Costura Francesa", descricao="Costura sofisticada utilizada em acabamento premium."),
        Costura(tipo="Costura Esportiva", descricao="Costura destacada utilizada em personalizações automotivas."),
    ]

    # =========================
    # CORES
    # =========================

    cores = [
        Cor(descricao="Preto"),
        Cor(descricao="Cinza"),
        Cor(descricao="Grafite"),
        Cor(descricao="Bege"),
        Cor(descricao="Marrom"),
        Cor(descricao="Caramelo"),
        Cor(descricao="Vermelho"),
        Cor(descricao="Azul"),
        Cor(descricao="Branco"),
        Cor(descricao="Verde"),
        Cor(descricao="Rosa"),
    ]

    # =========================
    # INSERÇÃO NO BANCO
    # =========================

    db.session.add_all(tecidos)
    db.session.add_all(espumas)
    db.session.add_all(costuras)
    db.session.add_all(cores)

    db.session.commit()

    print("Dados de catálogo inseridos com sucesso!")