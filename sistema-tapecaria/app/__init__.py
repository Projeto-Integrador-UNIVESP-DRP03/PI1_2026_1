from flask import Flask, abort, redirect, request, session, url_for
from sqlalchemy import event
from sqlalchemy.engine import Engine
from .models import db
import os
import secrets


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(connection, connection_record):
    if connection.__class__.__module__.startswith("sqlite3"):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(test_config=None):
    # Diretório base do projeto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(project_dir, "templates"),
        static_folder=os.path.join(project_dir, "static")
    )

    # Caminho da pasta instance
    instance_path = os.path.join(BASE_DIR, "..", "instance")

    # Garante que a pasta instance exista
    os.makedirs(instance_path, exist_ok=True)

    # Caminho do banco
    db_path = os.path.join(instance_path, "database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SECRET KEY
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        secrets.token_hex(32)
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE") == "1"
    app.config["ADMIN_USERNAME"] = os.environ.get("ADMIN_USERNAME", "admin")
    app.config["ADMIN_PASSWORD_HASH"] = os.environ.get("ADMIN_PASSWORD_HASH", "")
    if test_config:
        app.config.update(test_config)

    @app.context_processor
    def csrf_context():
        token = session.get("csrf_token")
        if not token:
            token = secrets.token_urlsafe(32)
            session["csrf_token"] = token
        return {"csrf_token": token}

    @app.before_request
    def validate_csrf():
        if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
            return

        expected = session.get("csrf_token")
        received = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
        if not expected or not received or not secrets.compare_digest(expected, received):
            abort(400, description="Token CSRF inválido ou ausente.")

    @app.before_request
    def require_authentication():
        if request.endpoint in {"main.login", "static"}:
            return
        if not session.get("authenticated"):
            return redirect(url_for("main.login", next=request.path))

    # Inicializa banco
    db.init_app(app)

    # Registra rotas
    from .routes import main
    app.register_blueprint(main)

    return app