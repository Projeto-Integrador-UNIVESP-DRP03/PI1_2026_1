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
        Tecido(material="Courvin", cor="Preto", descricao="Material sintético resistente muito utilizado em bancos automotivos."),
        Tecido(material="Courvin", cor="Cinza", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Bege", descricao="Material sintético utilizado em interiores claros."),
        Tecido(material="Couro Natural", cor="Preto", descricao="Material premium de alta durabilidade e acabamento sofisticado."),
        Tecido(material="Couro Natural", cor="Marrom", descricao="Couro natural utilizado em bancos de veículos premium."),
        Tecido(material="Suede", cor="Preto", descricao="Material sintético aveludado usado em personalizações automotivas."),
        Tecido(material="Suede", cor="Vermelho", descricao="Material aveludado utilizado em customizações esportivas."),
        Tecido(material="Tecido Automotivo", cor="Cinza", descricao="Tecido padrão utilizado em bancos originais de fábrica."),
        Tecido(material="Tecido Automotivo", cor="Grafite", descricao="Tecido resistente utilizado em interiores escuros."),
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