import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import create_app
from app.models import db, Cliente, TelefoneCliente, EnderecoCliente, Veiculo

app = create_app()

with app.app_context():

    print("Inserindo dados iniciais...")

    # Evita duplicar seeds
    if Cliente.query.first():
        print("O banco já possui dados. Seeds não executadas.")
        exit()

    # =========================
    # CLIENTE 1
    # =========================

    cliente1 = Cliente(
        id_cliente=1,
        cod_cliente="CLI001",
        nome="João da Silva"
    )

    db.session.add(cliente1)
    db.session.commit()

    telefone1 = TelefoneCliente(
        id_telefone=1,
        telefone="24999990001",
        id_cliente=cliente1.id_cliente
    )

    endereco1 = EnderecoCliente(
        id_endereco=1,
        rua="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente1.id_cliente
    )

    veiculo1 = Veiculo(
        id_veiculo=1,
        placa="ABC1A23",
        modelo="Gol",
        marca="Volkswagen",
        ano=2018,
        id_cliente=cliente1.id_cliente
    )

    db.session.add_all([telefone1, endereco1, veiculo1])

    # =========================
    # CLIENTE 2
    # =========================

    cliente2 = Cliente(
        id_cliente=2,
        cod_cliente="CLI002",
        nome="Maria Oliveira"
    )

    db.session.add(cliente2)
    db.session.commit()

    telefone2 = TelefoneCliente(
        id_telefone=2,
        telefone="24999990002",
        id_cliente=cliente2.id_cliente
    )

    endereco2 = EnderecoCliente(
        id_endereco=2,
        rua="Av. Amaral Peixoto",
        numero="456",
        bairro="Aterrado",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente2.id_cliente
    )

    veiculo2 = Veiculo(
        id_veiculo=2,
        placa="XYZ2B45",
        modelo="Onix",
        marca="Chevrolet",
        ano=2022,
        id_cliente=cliente2.id_cliente
    )

    db.session.add_all([telefone2, endereco2, veiculo2])

    # =========================

    db.session.commit()

    print("Seeds inseridas com sucesso!")