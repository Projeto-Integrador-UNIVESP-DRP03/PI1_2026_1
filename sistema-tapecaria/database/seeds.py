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
        nome="João da Silva",
        cliente_ativo=1
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
        veiculo_ativo=1,
        id_cliente=cliente1.id_cliente
    )

    db.session.add_all([telefone1, endereco1, veiculo1])

    # =========================
    # CLIENTE 2
    # =========================

    cliente2 = Cliente(
        id_cliente=2,
        cod_cliente="CLI002",
        nome="Maria Oliveira",
        cliente_ativo=1
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
        veiculo_ativo=1,
        id_cliente=cliente2.id_cliente
    )

    db.session.add_all([telefone2, endereco2, veiculo2])

    # =========================
    # CLIENTE 3
    # =========================

    cliente3 = Cliente(
        id_cliente=3,
        cod_cliente="CLI003",
        nome="Ana Santos",
        cliente_ativo=1
    )

    db.session.add(cliente3)
    db.session.commit()

    telefone3 = TelefoneCliente(
        id_telefone=3,
        telefone="24999990003",
        id_cliente=cliente3.id_cliente
    )

    endereco3 = EnderecoCliente(
        id_endereco=3,
        rua="Rua dos Ipês",
        numero="789",
        bairro="Jardim",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente3.id_cliente
    )

    veiculo3 = Veiculo(
        id_veiculo=3,
        placa="DEF3C67",
        modelo="Uno",
        marca="Fiat",
        ano=2019,
        cor="Vermelho",
        veiculo_ativo=1,
        id_cliente=cliente3.id_cliente
    )

    db.session.add_all([telefone3, endereco3, veiculo3])

    # =========================
    # CLIENTE 4
    # =========================

    cliente4 = Cliente(
        id_cliente=4,
        cod_cliente="CLI004",
        nome="Carlos Pereira",
        cliente_ativo=1
    )

    db.session.add(cliente4)
    db.session.commit()

    telefone4 = TelefoneCliente(
        id_telefone=4,
        telefone="24999990004",
        id_cliente=cliente4.id_cliente
    )

    endereco4 = EnderecoCliente(
        id_endereco=4,
        rua="Av. Sete de Setembro",
        numero="101",
        bairro="Centro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente4.id_cliente
    )

    veiculo4a = Veiculo(
        id_veiculo=4,
        placa="GHI4D89",
        modelo="Fiesta",
        marca="Ford",
        ano=2020,
        cor="Azul",
        veiculo_ativo=1,
        id_cliente=cliente4.id_cliente
    )

    veiculo4b = Veiculo(
        id_veiculo=5,
        placa="JKL5E01",
        modelo="Civic",
        marca="Honda",
        ano=2021,
        cor="Preto",
        veiculo_ativo=1,
        id_cliente=cliente4.id_cliente
    )

    db.session.add_all([telefone4, endereco4, veiculo4a, veiculo4b])

    # =========================
    # CLIENTE 5
    # =========================

    cliente5 = Cliente(
        id_cliente=5,
        cod_cliente="CLI005",
        nome="Beatriz Lima",
        cliente_ativo=1
    )

    db.session.add(cliente5)
    db.session.commit()

    telefone5 = TelefoneCliente(
        id_telefone=5,
        telefone="24999990005",
        id_cliente=cliente5.id_cliente
    )

    endereco5 = EnderecoCliente(
        id_endereco=5,
        rua="Rua do Comércio",
        numero="202",
        bairro="Comércio",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente5.id_cliente
    )

    # Sem veículos para este cliente (0 veículos)

    db.session.add_all([telefone5, endereco5])

    # =========================
    # CLIENTE 6
    # =========================

    cliente6 = Cliente(
        id_cliente=6,
        cod_cliente="CLI006",
        nome="Daniel Costa",
        cliente_ativo=1
    )

    db.session.add(cliente6)
    db.session.commit()

    telefone6 = TelefoneCliente(
        id_telefone=6,
        telefone="24999990006",
        id_cliente=cliente6.id_cliente
    )

    endereco6 = EnderecoCliente(
        id_endereco=6,
        rua="Rua São João",
        numero="303",
        bairro="São João",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente6.id_cliente
    )

    veiculo6a = Veiculo(
        id_veiculo=6,
        placa="MNO6F23",
        modelo="Corolla",
        marca="Toyota",
        ano=2018,
        cor="Branco",
        veiculo_ativo=1,
        id_cliente=cliente6.id_cliente
    )

    veiculo6b = Veiculo(
        id_veiculo=7,
        placa="PQR7G45",
        modelo="HB20",
        marca="Hyundai",
        ano=2022,
        cor="Prata",
        veiculo_ativo=1,
        id_cliente=cliente6.id_cliente
    )

    veiculo6c = Veiculo(
        id_veiculo=8,
        placa="STU8H67",
        modelo="Renegade",
        marca="Jeep",
        ano=2023,
        cor="Cinza",
        veiculo_ativo=1,
        id_cliente=cliente6.id_cliente
    )

    db.session.add_all([telefone6, endereco6, veiculo6a, veiculo6b, veiculo6c])

    # =========================
    # CLIENTE 7
    # =========================

    cliente7 = Cliente(
        id_cliente=7,
        cod_cliente="CLI007",
        nome="Eduarda Ferreira",
        cliente_ativo=1
    )

    db.session.add(cliente7)
    db.session.commit()

    telefone7 = TelefoneCliente(
        id_telefone=7,
        telefone="24999990007",
        id_cliente=cliente7.id_cliente
    )

    endereco7 = EnderecoCliente(
        id_endereco=7,
        rua="Av. Paulo de Frontin",
        numero="404",
        bairro="Vila Santa Cecília",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente7.id_cliente
    )

    veiculo7 = Veiculo(
        id_veiculo=9,
        placa="VWX9I89",
        modelo="Compass",
        marca="Jeep",
        ano=2021,
        cor="Verde",
        veiculo_ativo=1,
        id_cliente=cliente7.id_cliente
    )

    db.session.add_all([telefone7, endereco7, veiculo7])

    # =========================
    # CLIENTE 8
    # =========================

    cliente8 = Cliente(
        id_cliente=8,
        cod_cliente="CLI008",
        nome="Fernando Alves",
        cliente_ativo=1
    )

    db.session.add(cliente8)
    db.session.commit()

    telefone8 = TelefoneCliente(
        id_telefone=8,
        telefone="24999990008",
        id_cliente=cliente8.id_cliente
    )

    endereco8 = EnderecoCliente(
        id_endereco=8,
        rua="Rua Tiradentes",
        numero="505",
        bairro="Retiro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente8.id_cliente
    )

    veiculo8a = Veiculo(
        id_veiculo=10,
        placa="YZA0J01",
        modelo="Tucson",
        marca="Hyundai",
        ano=2019,
        cor="Marrom",
        veiculo_ativo=1,
        id_cliente=cliente8.id_cliente
    )

    veiculo8b = Veiculo(
        id_veiculo=11,
        placa="BCD1K23",
        modelo="Creta",
        marca="Hyundai",
        ano=2020,
        cor="Azul",
        veiculo_ativo=1,
        id_cliente=cliente8.id_cliente
    )

    db.session.add_all([telefone8, endereco8, veiculo8a, veiculo8b])

    # =========================
    # CLIENTE 9
    # =========================

    cliente9 = Cliente(
        id_cliente=9,
        cod_cliente="CLI009",
        nome="Gabriela Rocha",
        cliente_ativo=1
    )

    db.session.add(cliente9)
    db.session.commit()

    telefone9 = TelefoneCliente(
        id_telefone=9,
        telefone="24999990009",
        id_cliente=cliente9.id_cliente
    )

    endereco9 = EnderecoCliente(
        id_endereco=9,
        rua="Rua Quinze de Novembro",
        numero="606",
        bairro="Centro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente9.id_cliente
    )

    # Sem veículos (0)

    db.session.add_all([telefone9, endereco9])

    # =========================
    # CLIENTE 10
    # =========================

    cliente10 = Cliente(
        id_cliente=10,
        cod_cliente="CLI010",
        nome="Henrique Mendes",
        cliente_ativo=1
    )

    db.session.add(cliente10)
    db.session.commit()

    telefone10 = TelefoneCliente(
        id_telefone=10,
        telefone="24999990010",
        id_cliente=cliente10.id_cliente
    )

    endereco10 = EnderecoCliente(
        id_endereco=10,
        rua="Av. dos Trabalhadores",
        numero="707",
        bairro="Vila Brasília",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente10.id_cliente
    )

    veiculo10a = Veiculo(
        id_veiculo=12,
        placa="EFG2L45",
        modelo="EcoSport",
        marca="Ford",
        ano=2017,
        cor="Preto",
        veiculo_ativo=1,
        id_cliente=cliente10.id_cliente
    )

    veiculo10b = Veiculo(
        id_veiculo=13,
        placa="HIJ3M67",
        modelo="Ranger",
        marca="Ford",
        ano=2022,
        cor="Branco",
        veiculo_ativo=1,
        id_cliente=cliente10.id_cliente
    )

    veiculo10c = Veiculo(
        id_veiculo=14,
        placa="KLM4N89",
        modelo="Fusion",
        marca="Ford",
        ano=2018,
        cor="Prata",
        veiculo_ativo=0,
        id_cliente=cliente10.id_cliente
    )

    veiculo10d = Veiculo(
        id_veiculo=15,
        placa="NOP5O01",
        modelo="Focus",
        marca="Ford",
        ano=2019,
        cor="Vermelho",
        id_cliente=cliente10.id_cliente
    )

    db.session.add_all([telefone10, endereco10, veiculo10a, veiculo10b, veiculo10c, veiculo10d])

    # =========================
    # CLIENTE 11
    # =========================

    cliente11 = Cliente(
        id_cliente=11,
        cod_cliente="CLI011",
        nome="Isabela Nunes",
        cliente_ativo=1
    )

    db.session.add(cliente11)
    db.session.commit()

    telefone11 = TelefoneCliente(
        id_telefone=11,
        telefone="24999990011",
        id_cliente=cliente11.id_cliente
    )

    endereco11 = EnderecoCliente(
        id_endereco=11,
        rua="Rua da Paz",
        numero="808",
        bairro="Jardim América",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente11.id_cliente
    )

    veiculo11 = Veiculo(
        id_veiculo=16,
        placa="QRS6P23",
        modelo="Onix Plus",
        marca="Chevrolet",
        ano=2021,
        cor="Cinza",
        veiculo_ativo=1,
        id_cliente=cliente11.id_cliente
    )

    db.session.add_all([telefone11, endereco11, veiculo11])

    # =========================
    # CLIENTE 12
    # =========================

    cliente12 = Cliente(
        id_cliente=12,
        cod_cliente="CLI012",
        nome="João Pedro",
        cliente_ativo=1
    )

    db.session.add(cliente12)
    db.session.commit()

    telefone12 = TelefoneCliente(
        id_telefone=12,
        telefone="24999990012",
        id_cliente=cliente12.id_cliente
    )

    endereco12 = EnderecoCliente(
        id_endereco=12,
        rua="Av. Getúlio Vargas",
        numero="909",
        bairro="Centro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente12.id_cliente
    )

    veiculo12a = Veiculo(
        id_veiculo=17,
        placa="TUV7Q45",
        modelo="Gol Trend",
        marca="Volkswagen",
        ano=2016,
        cor="Azul",
        veiculo_ativo=1,
        id_cliente=cliente12.id_cliente
    )

    veiculo12b = Veiculo(
        id_veiculo=18,
        placa="WXY8R67",
        modelo="Polo",
        marca="Volkswagen",
        ano=2020,
        cor="Preto",
        veiculo_ativo=1,
        id_cliente=cliente12.id_cliente
    )

    db.session.add_all([telefone12, endereco12, veiculo12a, veiculo12b])

    # =========================
    # CLIENTE 13
    # =========================

    cliente13 = Cliente(
        id_cliente=13,
        cod_cliente="CLI013",
        nome="Karina Souza",
        cliente_ativo=0
    )

    db.session.add(cliente13)
    db.session.commit()

    telefone13 = TelefoneCliente(
        id_telefone=13,
        telefone="24999990013",
        id_cliente=cliente13.id_cliente
    )

    endereco13 = EnderecoCliente(
        id_endereco=13,
        rua="Rua do Porto",
        numero="1010",
        bairro="Porto Velho",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente13.id_cliente
    )

    # Sem veículos (0)

    db.session.add_all([telefone13, endereco13])

    # =========================
    # CLIENTE 14
    # =========================

    cliente14 = Cliente(
        id_cliente=14,
        cod_cliente="CLI014",
        nome="Lucas Barbosa",
        cliente_ativo=1
    )

    db.session.add(cliente14)
    db.session.commit()

    telefone14 = TelefoneCliente(
        id_telefone=14,
        telefone="24999990014",
        id_cliente=cliente14.id_cliente
    )

    endereco14 = EnderecoCliente(
        id_endereco=14,
        rua="Av. Industrial",
        numero="1111",
        bairro="Industrial",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente14.id_cliente
    )

    veiculo14a = Veiculo(
        id_veiculo=19,
        placa="ZAB9S89",
        modelo="Strada",
        marca="Fiat",
        ano=2019,
        cor="Branco",
        veiculo_ativo=1,
        id_cliente=cliente14.id_cliente
    )

    veiculo14b = Veiculo(
        id_veiculo=20,
        placa="CDE0T01",
        modelo="Toro",
        marca="Fiat",
        ano=2023,
        cor="Vermelho",
        veiculo_ativo=0,
        id_cliente=cliente14.id_cliente
    )

    veiculo14c = Veiculo(
        id_veiculo=21,
        placa="FGH1U23",
        modelo="Mobi",
        marca="Fiat",
        ano=2022,
        cor="Azul",
        veiculo_ativo=1,
        id_cliente=cliente14.id_cliente
    )

    db.session.add_all([telefone14, endereco14, veiculo14a, veiculo14b, veiculo14c])

    # =========================
    # CLIENTE 15
    # =========================

    cliente15 = Cliente(
        id_cliente=15,
        cod_cliente="CLI015",
        nome="Mariana Castro",
        cliente_ativo=1
    )

    db.session.add(cliente15)
    db.session.commit()

    telefone15 = TelefoneCliente(
        id_telefone=15,
        telefone="24999990015",
        id_cliente=cliente15.id_cliente
    )

    endereco15 = EnderecoCliente(
        id_endereco=15,
        rua="Rua São Paulo",
        numero="1212",
        bairro="São Paulo",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente15.id_cliente
    )

    veiculo15 = Veiculo(
        id_veiculo=22,
        placa="IJK2V45",
        modelo="Argo",
        marca="Fiat",
        ano=2021,
        cor="Prata",
        veiculo_ativo=1,
        id_cliente=cliente15.id_cliente
    )

    db.session.add_all([telefone15, endereco15, veiculo15])

    # =========================
    # CLIENTE 16
    # =========================

    cliente16 = Cliente(
        id_cliente=16,
        cod_cliente="CLI016",
        nome="Nicolas Ribeiro",
        cliente_ativo=1
    )

    db.session.add(cliente16)
    db.session.commit()

    telefone16 = TelefoneCliente(
        id_telefone=16,
        telefone="24999990016",
        id_cliente=cliente16.id_cliente
    )

    endereco16 = EnderecoCliente(
        id_endereco=16,
        rua="Av. Brasil",
        numero="1313",
        bairro="Brasil",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente16.id_cliente
    )

    veiculo16a = Veiculo(
        id_veiculo=23,
        placa="LMN3W67",
        modelo="Saveiro",
        marca="Volkswagen",
        ano=2018,
        cor="Cinza",
        veiculo_ativo=0,
        id_cliente=cliente16.id_cliente
    )

    veiculo16b = Veiculo(
        id_veiculo=24,
        placa="OPQ4X89",
        modelo="Virtus",
        marca="Volkswagen",
        ano=2022,
        cor="Preto",
        veiculo_ativo=1,
        id_cliente=cliente16.id_cliente
    )

    veiculo16c = Veiculo(
        id_veiculo=25,
        placa="RST5Y01",
        modelo="T-Cross",
        marca="Volkswagen",
        ano=2023,
        cor="Branco",
        veiculo_ativo=0,
        id_cliente=cliente16.id_cliente
    )

    veiculo16d = Veiculo(
        id_veiculo=26,
        placa="UVW6Z23",
        modelo="Nivus",
        marca="Volkswagen",
        ano=2024,
        cor="Azul",
        veiculo_ativo=1,
        id_cliente=cliente16.id_cliente
    )

    veiculo16e = Veiculo(
        id_veiculo=27,
        placa="XYZ7A45",
        modelo="Taos",
        marca="Volkswagen",
        ano=2021,
        cor="Verde",
        veiculo_ativo=1,
        id_cliente=cliente16.id_cliente
    )

    db.session.add_all([telefone16, endereco16, veiculo16a, veiculo16b, veiculo16c, veiculo16d, veiculo16e])

    # =========================
    # CLIENTE 17
    # =========================

    cliente17 = Cliente(
        id_cliente=17,
        cod_cliente="CLI017",
        nome="Olivia Gomes",
        cliente_ativo=1
    )

    db.session.add(cliente17)
    db.session.commit()

    telefone17 = TelefoneCliente(
        id_telefone=17,
        telefone="24999990017",
        id_cliente=cliente17.id_cliente
    )

    endereco17 = EnderecoCliente(
        id_endereco=17,
        rua="Rua Rio de Janeiro",
        numero="1414",
        bairro="Rio de Janeiro",
        cidade="Volta Redonda",
        estado="RJ",
        id_cliente=cliente17.id_cliente
    )

    # Sem veículos (0)

    db.session.add_all([telefone17, endereco17])

    db.session.commit()

    print("Seeds inseridas com sucesso!")