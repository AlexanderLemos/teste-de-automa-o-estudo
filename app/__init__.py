"""
Web Task Manager — Flask Application Factory

Aplicação web RESTful para gerenciamento de tarefas.
Utiliza o padrão Factory para facilitar testes automatizados.
"""

import os
import sqlite3
from flask import Flask


def get_db_path(app):
    """Retorna o caminho do banco de dados."""
    return app.config.get("DATABASE", os.path.join(app.instance_path, "tasks.db"))


def get_db(app=None):
    """Obtém conexão com o banco de dados SQLite."""
    from flask import g, current_app

    if app is None:
        app = current_app

    if "db" not in g:
        g.db = sqlite3.connect(get_db_path(app))
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Fecha a conexão com o banco ao final da request."""
    from flask import g

    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Inicializa o schema do banco de dados."""
    db = sqlite3.connect(get_db_path(app))
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT DEFAULT 'media' CHECK(priority IN ('baixa', 'media', 'alta', 'critica')),
            status TEXT DEFAULT 'pendente' CHECK(status IN ('pendente', 'em_andamento', 'concluida', 'cancelada')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()


def create_app(test_config=None):
    """
    Application Factory — cria e configura a aplicação Flask.

    Args:
        test_config: Configurações de teste (sobrescreve as padrão).

    Returns:
        Instância configurada do Flask.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Configuração padrão
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        DATABASE=os.path.join(app.instance_path, "tasks.db"),
    )

    # Sobrescreve com config de teste se fornecida
    if test_config is not None:
        app.config.update(test_config)

    # Garante que o diretório instance existe
    os.makedirs(app.instance_path, exist_ok=True)

    # Inicializa o banco de dados
    init_db(app)

    # Registra função de cleanup
    app.teardown_appcontext(close_db)

    # Registra as rotas
    from . import routes
    app.register_blueprint(routes.bp)

    return app
