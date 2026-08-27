import sys
from datetime import date

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(__file__).split("\\tests\\")[0])

from app import create_app
from app.models import Cliente, Costura, Veiculo, Orcamento, Pedido, OrcamentoCostura, db


@pytest.fixture()
def app(tmp_path):
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


def test_post_without_csrf_is_rejected(client):
    response = client.post("/buscar", data={"cod_cliente": "TST001"})
    assert response.status_code == 400


def test_invalid_budget_date_is_redirected_without_creation(app, client):
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


def test_budget_saves_costura_and_observation(app, client):
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


def test_client_creation_redirects_to_vehicle_form(app, client):
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


def test_vehicle_creation_normalizes_plate(app, client):
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


def test_vehicle_cannot_be_assigned_to_another_client(app, client):
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


def test_order_status_sets_completion_date(app, client):
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


def test_dashboard_chart_ignores_budget_older_than_twelve_months(app, client):
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
