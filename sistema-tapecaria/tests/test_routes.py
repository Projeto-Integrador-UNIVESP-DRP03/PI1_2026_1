"""Suite de testes de rotas do Sistema Tapecaria.

Este arquivo valida o comportamento principal da aplicação web em nível de
interface/rotas, usando um banco SQLite temporário para isolar cada cenário.

Objetivo:
- garantir que as páginas e endpoints principais respondam corretamente;
- proteger regras de autenticação e CSRF;
- validar criação e atualização de clientes, veículos, orçamentos e pedidos;
- verificar indicadores do dashboard e fluxos de aceitação/rejeição de pedidos.

Estratégia:
- cada teste cria o mínimo necessário para o cenário em questão;
- o banco é recriado por fixture para evitar dependência entre testes;
- o cliente autenticado é reutilizado em vários casos para reduzir duplicação;
- as asserções observam respostas HTTP, redirecionamentos e dados persistidos.
"""

import sys
from datetime import date

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(__file__).split("\\tests\\")[0])

from app import create_app
from app.models import Cliente, Costura, Veiculo, Orcamento, Pedido, OrcamentoCostura, db


# =========================
# FIXTURES E AUXILIARES
# =========================
# Os testes usam um banco SQLite temporário para isolar cada cenário e evitar
# interferência entre execuções. O cliente autenticado também é criado em
# fixtures para reutilização em vários cenários.


@pytest.fixture()
def app(tmp_path):
    """Cria uma instância da aplicação com banco isolado para cada teste.

    A estrutura segue o padrão recomendado para testes Flask: uma app temporária,
    uma base SQLite em disco e um estado inicial pequeno, porém suficiente para
    cobrir as rotas que dependem de clientes, veículos e itens de costura.
    """
    database_path = tmp_path / "test.db"
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD_HASH": generate_password_hash("test-password"),
        }
    )
    with application.app_context():
        db.create_all()
        cliente = Cliente(cod_cliente="TST001", nome="Cliente Teste")
        db.session.add(cliente)
        db.session.flush()
        veiculo = Veiculo(
            id_cliente=cliente.id_cliente,
            placa="TST1A23",
            marca="Marca",
            modelo="Modelo",
        )
        costura = Costura(tipo="Costura Teste")
        db.session.add_all([veiculo, costura])
        db.session.commit()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Retorna um cliente HTTP autenticado como administrador.

    Esse fixture centraliza o login do usuário de teste e evita repetir código em
    todos os cenários que dependem de estar logado dentro da aplicação.
    """
    test_client = app.test_client()
    response = test_client.get("/login")
    assert response.status_code == 200
    with test_client.session_transaction() as session:
        token = session["csrf_token"]
    response = test_client.post(
        "/login",
        data={
            "csrf_token": token,
            "username": "admin",
            "password": "test-password",
        },
    )
    assert response.status_code == 302
    return test_client


def csrf_token(client):
    """Busca o token CSRF atual da sessão do cliente de teste.

    Esse helper evita repetição em rotas protegidas por segurança reforçada.
    """
    client.get("/")
    with client.session_transaction() as session:
        return session["csrf_token"]


def test_unauthenticated_user_is_redirected_to_login(app):
    unauthenticated_client = app.test_client()
    response = unauthenticated_client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login?next=/")


def test_invalid_login_is_rejected(app):
    unauthenticated_client = app.test_client()
    response = unauthenticated_client.get("/login")
    with unauthenticated_client.session_transaction() as session:
        token = session["csrf_token"]

    response = unauthenticated_client.post(
        "/login",
        data={"csrf_token": token, "username": "admin", "password": "wrong"},
    )
    assert response.status_code == 200
    with unauthenticated_client.session_transaction() as session:
        assert not session.get("authenticated")


def test_logout_clears_session(client):
    token = csrf_token(client)
    response = client.post("/logout", data={"csrf_token": token})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


# =========================
# AUTENTICAÇÃO E SEGURANÇA
# =========================
# Este bloco cobre o comportamento inicial da aplicação: acesso anônimo,
# autenticação do usuário administrador, encerramento de sessão e proteção CSRF.
# Esses testes garantem que a aplicação não aceite ações inseguras nem permita
# uso indevido sem autenticação.


class TestAutenticacaoESeguranca:
    """Valida o fluxo de login, logout e proteção de rotas sensíveis."""

    def test_post_without_csrf_is_rejected(self, client):
        response = client.post("/buscar", data={"cod_cliente": "TST001"})
        assert response.status_code == 400

    def test_unauthenticated_user_is_redirected_to_login(self, app):
        unauthenticated_client = app.test_client()
        response = unauthenticated_client.get("/")
        assert response.status_code == 302
        assert response.headers["Location"].endswith("/login?next=/")

    def test_invalid_login_is_rejected(self, app):
        unauthenticated_client = app.test_client()
        response = unauthenticated_client.get("/login")
        with unauthenticated_client.session_transaction() as session:
            token = session["csrf_token"]

        response = unauthenticated_client.post(
            "/login",
            data={"csrf_token": token, "username": "admin", "password": "wrong"},
        )
        assert response.status_code == 200
        with unauthenticated_client.session_transaction() as session:
            assert not session.get("authenticated")

    def test_malformed_password_hash_does_not_raise_server_error(self, app):
        app.config["ADMIN_PASSWORD_HASH"] = "invalid-hash"
        unauthenticated_client = app.test_client()
        response = unauthenticated_client.get("/login")
        with unauthenticated_client.session_transaction() as session:
            token = session["csrf_token"]

        response = unauthenticated_client.post(
            "/login",
            data={"csrf_token": token, "username": "admin", "password": "any-password"},
        )

        assert response.status_code == 200
        assert "Usuário ou senha inválidos." in response.get_data(as_text=True)

    def test_logout_clears_session(self, client):
        token = csrf_token(client)
        response = client.post("/logout", data={"csrf_token": token})
        assert response.status_code == 302
        assert response.headers["Location"].endswith("/login")


# =========================
# CLIENTES E BUSCA
# =========================
# Este bloco valida a busca, a listagem, o cadastro e a manutenção de clientes.
# Também inclui casos de inativação e atualização de dados, que representam o
# núcleo das operações de cadastro e relacionamento com veículos.


class TestClientesEBusca:
    """Garante que clientes sejam cadastrados, consultados e ocultados corretamente."""

    def test_customer_search_finds_existing_client(self, app, client):
        token = csrf_token(client)
        response = client.post(
            "/buscar",
            data={"csrf_token": token, "cod_cliente": "TST001"},
        )

        assert response.status_code == 200
        assert b"Cliente Teste" in response.data

    def test_client_list_hides_inactive_clients(self, app, client):
        with app.app_context():
            inactive_client = Cliente(cod_cliente="TST999", nome="Cliente Inativo", cliente_ativo=0)
            db.session.add(inactive_client)
            db.session.commit()

        response = client.get("/clientes")

        assert response.status_code == 200
        assert b"Cliente Teste" in response.data
        assert b"Cliente Inativo" not in response.data

    def test_client_list_escapes_delete_button_data(self, app, client):
        with app.app_context():
            quoted_client = Cliente(cod_cliente="TSTQ01", nome='Amanda "Especial"')
            db.session.add(quoted_client)
            db.session.commit()

        response = client.get("/clientes")

        assert response.status_code == 200
        assert b'data-delete-name="Amanda &#34;Especial&#34;"' in response.data
        assert b'onclick="openDeleteModal' not in response.data

    def test_client_creation_redirects_to_vehicle_form(self, app, client):
        token = csrf_token(client)
        response = client.post(
            "/salvar_cliente",
            data={
                "csrf_token": token,
                "cod_cliente": "NEW001",
                "nome": "Novo Cliente",
                "telefone": "12999990000",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            created = Cliente.query.filter_by(cod_cliente="NEW001").one()
            assert created.nome == "Novo Cliente"
            assert created.telefones[0].telefone == "12999990000"

    def test_client_update_changes_name_and_phone(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            cliente = Cliente.query.first()
            cliente_id = cliente.id_cliente

        response = client.post(
            f"/atualizar_cliente/{cliente_id}",
            data={
                "csrf_token": token,
                "nome": "Cliente Atualizado",
                "telefone": "12999998888",
                "rua": "Av. Teste",
                "numero": "123",
                "bairro": "Centro",
                "cidade": "Pindamonhangaba",
                "estado": "SP",
                "cep": "12400000",
                "complemento": "Casa",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            updated = db.session.get(Cliente, cliente_id)
            assert updated.nome == "Cliente Atualizado"
            assert updated.telefones[0].telefone == "12999998888"
            assert updated.enderecos[0].cidade == "Pindamonhangaba"

    def test_customer_soft_delete_hides_client_and_vehicle(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            cliente = Cliente.query.first()
            cliente_id = cliente.id_cliente
            veiculo = Veiculo.query.filter_by(id_cliente=cliente_id).first()
            veiculo_id = veiculo.id_veiculo

        response = client.post(
            f"/deletar_cliente/{cliente_id}",
            data={"csrf_token": token},
        )

        assert response.status_code == 302
        with app.app_context():
            assert db.session.get(Cliente, cliente_id).cliente_ativo == 0
            assert db.session.get(Veiculo, veiculo_id).veiculo_ativo == 0

        response = client.get("/clientes")
        assert response.status_code == 200
        assert b"Cliente Teste" not in response.data


# =========================
# ORÇAMENTOS
# =========================
# Os testes deste grupo focam no ciclo de orçamento: dados válidos e inválidos,
# associação de itens de costura, persistência de observações e aceitação/rejeição
# do cliente. Esse fluxo é crítico porque gera a base para a criação de pedidos.


class TestOrcamentos:
    """Valida a criação, persistência e aprovação de orçamentos."""

    def test_invalid_budget_date_is_redirected_without_creation(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle_id = Veiculo.query.first().id_veiculo

        response = client.post(
            "/salvar_orcamento",
            data={
                "csrf_token": token,
                "id_veiculo": vehicle_id,
                "dat_orcamento": "invalid-date",
                "qtd_bancos": "0",
                "qtd_apoio_cabeca": "0",
                "valor": "10",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            assert db.session.execute(db.select(OrcamentoCostura)).first() is None

    def test_budget_saves_costura_and_observation(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle_id = Veiculo.query.first().id_veiculo
            costura_id = Costura.query.first().id_costura

        response = client.post(
            "/salvar_orcamento",
            data={
                "csrf_token": token,
                "id_veiculo": vehicle_id,
                "dat_orcamento": "2026-08-26",
                "qtd_bancos": "1",
                "qtd_apoio_cabeca": "0",
                "valor": "10,50",
                "costuras": str(costura_id),
                f"obs_costura_{costura_id}": "Observacao teste",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            item = db.session.execute(db.select(OrcamentoCostura)).scalar_one()
            assert item.id_costura == costura_id
            assert item.obs_item == "Observacao teste"

    def test_budget_acceptance_creates_pending_order(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=100,
            )
            db.session.add(budget)
            db.session.commit()
            budget_id = budget.id_orcamento

        response = client.post(
            f"/orcamento/{budget_id}/aceitar",
            data={"csrf_token": token},
        )

        assert response.status_code == 302
        with app.app_context():
            order = Pedido.query.filter_by(id_orcamento=budget_id).one()
            assert order.boolean_aceite_cliente is True
            assert order.status == "Pendente"

    def test_budget_refusal_creates_rejected_order(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=100,
            )
            db.session.add(budget)
            db.session.commit()
            budget_id = budget.id_orcamento

        response = client.post(
            f"/orcamento/{budget_id}/recusar",
            data={"csrf_token": token},
        )

        assert response.status_code == 302
        with app.app_context():
            order = Pedido.query.filter_by(id_orcamento=budget_id).one()
            assert order.boolean_aceite_cliente is False
            assert order.status == "Recusado"

    def test_budget_list_page_renders_successfully(self, app, client):
        with app.app_context():
            vehicle = Veiculo.query.first()
            Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=150,
            )
            db.session.commit()

        response = client.get("/orcamentos")

        assert response.status_code == 200
        assert b"Cliente, carro ou placa" in response.data

    def test_budget_pdf_download_returns_pdf_response(self, app, client):
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=150.00,
                obs="Observação do orçamento",
            )
            db.session.add(budget)
            db.session.commit()
            budget_id = budget.id_orcamento

        response = client.get(f"/orcamento/{budget_id}/pdf")

        assert response.status_code == 200
        assert response.mimetype == "application/pdf"
        assert response.headers["Content-Disposition"].startswith("attachment; filename=")


# =========================
# VEÍCULOS E PEDIDOS
# =========================
# Neste grupo validamos o cadastro e atualização de veículos, além do ciclo de
# pedidos após a aprovação do orçamento. São casos importantes para garantir que
# dados de automóveis e status dos pedidos sigam as regras de negócio do sistema.


class TestVeiculosEPedidos:
    """Cobertura dos fluxos de veículos e status dos pedidos."""

    def test_vehicle_creation_normalizes_plate(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            client_id = Cliente.query.first().id_cliente

        response = client.post(
            "/salvar_veiculo",
            data={
                "csrf_token": token,
                "id_cliente": client_id,
                "placa": "abc-1234",
                "marca": "Fiat",
                "modelo": "Uno",
                "ano": "2020",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            vehicle = Veiculo.query.filter_by(placa="ABC1234").one()
            assert vehicle.id_cliente == client_id

    def test_vehicle_cannot_be_assigned_to_another_client(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            first_client = Cliente.query.first()
            second_client = Cliente(cod_cliente="TST002", nome="Outro Cliente")
            db.session.add(second_client)
            db.session.commit()
            vehicle = Veiculo.query.filter_by(id_cliente=first_client.id_cliente).first()
            first_client_id = first_client.id_cliente
            second_client_id = second_client.id_cliente
            vehicle_id = vehicle.id_veiculo
            vehicle_plate = vehicle.placa
            vehicle_brand = vehicle.marca
            vehicle_model = vehicle.modelo

        response = client.post(
            "/salvar_veiculo",
            data={
                "csrf_token": token,
                "id_veiculo": vehicle_id,
                "id_cliente": second_client_id,
                "placa": vehicle_plate,
                "marca": vehicle_brand,
                "modelo": vehicle_model,
            },
        )

        assert response.status_code == 302
        with app.app_context():
            assert db.session.get(Veiculo, vehicle_id).id_cliente == first_client_id

    def test_vehicle_edit_page_renders_form(self, app, client):
        with app.app_context():
            vehicle = Veiculo.query.first()
            vehicle_id = vehicle.id_veiculo

        response = client.get(f"/editar_veiculo/{vehicle_id}")

        assert response.status_code == 200
        assert b"Editar Ve\xc3\xadculo" in response.data or b"Atualizar Ve\xc3\xadculo" in response.data

    def test_vehicle_update_changes_info(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle = Veiculo.query.first()
            vehicle_id = vehicle.id_veiculo
            client_id = vehicle.id_cliente

        response = client.post(
            "/salvar_veiculo",
            data={
                "csrf_token": token,
                "id_veiculo": vehicle_id,
                "id_cliente": client_id,
                "placa": "xyz-9876",
                "marca": "Chevrolet",
                "modelo": "Onix",
                "ano": "2023",
                "cor": "Azul",
            },
        )

        assert response.status_code == 302
        with app.app_context():
            updated = db.session.get(Veiculo, vehicle_id)
            assert updated.placa == "XYZ9876"
            assert updated.marca == "Chevrolet"
            assert updated.modelo == "Onix"
            assert updated.cor == "Azul"

    def test_pedido_search_filters_by_customer_name(self, app, client):
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=200,
            )
            db.session.add(budget)
            db.session.flush()
            order = Pedido(
                id_orcamento=budget.id_orcamento,
                boolean_aceite_cliente=True,
                status="Em Andamento",
            )
            db.session.add(order)
            db.session.commit()

        response = client.get("/pedidos?search=Cliente")

        assert response.status_code == 200
        assert b"Cliente Teste" in response.data

    def test_completed_orders_page_lists_concluded_orders(self, app, client):
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=250,
            )
            db.session.add(budget)
            db.session.flush()
            order = Pedido(
                id_orcamento=budget.id_orcamento,
                boolean_aceite_cliente=True,
                status="Concluído",
                data_conclusao=date(2026, 9, 1),
            )
            db.session.add(order)
            db.session.commit()

        response = client.get("/pedidos/concluidos")

        assert response.status_code == 200
        assert b"Cliente Teste" in response.data

    def test_order_status_sets_completion_date(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=100,
            )
            db.session.add(budget)
            db.session.flush()
            order = Pedido(
                id_orcamento=budget.id_orcamento,
                boolean_aceite_cliente=True,
                status="Pendente",
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id_pedido

        response = client.post(
            f"/pedido/{order_id}/status",
            data={"csrf_token": token, "status": "Concluído"},
        )

        assert response.status_code == 302
        with app.app_context():
            updated = db.session.get(Pedido, order_id)
            assert updated.status == "Concluído"
            assert updated.data_conclusao is not None

    def test_invalid_order_status_is_rejected(self, app, client):
        token = csrf_token(client)
        with app.app_context():
            vehicle = Veiculo.query.first()
            budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(2026, 8, 26),
                valor=100,
            )
            db.session.add(budget)
            db.session.flush()
            order = Pedido(
                id_orcamento=budget.id_orcamento,
                boolean_aceite_cliente=True,
                status="Pendente",
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id_pedido

        response = client.post(
            f"/pedido/{order_id}/status",
            data={"csrf_token": token, "status": "Status Inválido"},
        )

        assert response.status_code == 302
        with app.app_context():
            updated = db.session.get(Pedido, order_id)
            assert updated.status == "Pendente"


# =========================
# DASHBOARD
# =========================
# O painel analítico depende de filtros temporais para mostrar somente dados
# relevantes. Esse bloco verifica se orçamentos muito antigos não contaminam os
# indicadores exibidos ao usuário e se o JSON do gráfico mantém a estrutura correta.


class TestDashboard:
    """Valida os dados exportados para o dashboard e o cálculo dos indicadores."""

    def test_dashboard_chart_ignores_budget_older_than_twelve_months(self, app, client):
        today = date.today()
        with app.app_context():
            vehicle = Veiculo.query.first()
            old_budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=date(today.year - 2, today.month, 1),
                valor=100,
            )
            recent_budget = Orcamento(
                id_veiculo=vehicle.id_veiculo,
                dat_orcamento=today,
                valor=200,
            )
            db.session.add_all([old_budget, recent_budget])
            db.session.commit()

        response = client.get("/api/dashboard/stats")

        assert response.status_code == 200
        labels = response.get_json()["chartData"]["labels"]
        assert f"{today.month:02d}/{today.year}" in labels
        assert f"{today.month:02d}/{today.year - 2}" not in labels
