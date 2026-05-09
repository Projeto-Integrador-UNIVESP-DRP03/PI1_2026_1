import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import create_app
from app.models import db, Tecido, Costura, Cor

app = create_app()

with app.app_context():

    print("Inserindo dados de catálogo...")

    # =========================
    # TECIDOS
    # =========================

    tecidos = [
        Tecido(material="Courvin", cor="Eco 04", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco 09", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco 05", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco 17", descricao="Material sintético resistente com acabamento automotivo."),    
        Tecido(material="Courvin", cor="Eco 13", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco 24", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco 02", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Eco Caramelo", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Marrom", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Marrom Escuro", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Bege", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Azul Escuro", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Azul", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Azul Claro", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Vinho", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Vermelho Sangue", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Orange", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Pueblo", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Branco", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Camurça", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Xadrez", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 04", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 09", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 05", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 17", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 13", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 24", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL HB20", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL Caramelo", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 11", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 21", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 25", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 02", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="CL 22", descricao="Material sintético resistente com acabamento automotivo."),  
        Tecido(material="Courvin", cor="CL Terracota", descricao="Material sintético resistente com acabamento automotivo."),
        Tecido(material="Courvin", cor="Fresh", descricao="Material sintético resistente com acabamento automotivo."),
    ]
    print("Catálogo de tecidos criado com sucesso!")
    # =========================
    # COSTURAS
    # =========================

    costuras = [
        Costura(tipo="Diamante Duplo", descricao="Costura decorativa e estrutural com linha dupla."),
        Costura(tipo="Colmeia", descricao="Costura de franzido que cria uma textura em relevo no tecido."),
        Costura(tipo="Programada 1", descricao="Costura destacada utilizada em personalizações automotivas."),
        Costura(tipo="Colmeia com Faixa", descricao="Costura de franzido que cria uma textura em relevo no tecido, com faixa no seu interior."),
        Costura(tipo="Diamante Padrão", descricao="Costura decorativa e estrutural com linha simples."),
        Costura(tipo="Sportline 1", descricao="Costura destacada com design elegante e esportivo."),
        Costura(tipo="Programada 2", descricao="Costura destacada utilizada em personalizações automotivas."),
        Costura(tipo="Sportline 2", descricao="Costura destacada com design elegante e esportivo."),
        Costura(tipo="Programada 3", descricao="Costura destacada utilizada em personalizações automotivas."),
        Costura(tipo="Sportline 3", descricao="Costura destacada com design elegante e esportivo."),
        Costura(tipo="Diamante", descricao="Costura decorativa e estrutural com linha simples e losangos pequenos."),
        Costura(tipo="Personalizada pelo cliente", descricao="Costura personalizada pelo cliente."),
    ]
    print("Catálogo de costuras criado com sucesso!")
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
    print("Catálogo de cores criado com sucesso!")
    # =========================
    # INSERÇÃO NO BANCO
    # =========================

    db.session.add_all(tecidos)
    db.session.add_all(costuras)
    db.session.add_all(cores)

    db.session.commit()

    print("Dados de catálogo inseridos com sucesso!")