"""
Fixtures compartilhadas para os testes.

Define configurações de teste, cliente HTTP e dados de exemplo
reutilizáveis por todos os módulos de teste.
"""

import os
import tempfile
import pytest
from app import create_app


@pytest.fixture
def app():
    """Cria uma instância da aplicação configurada para testes."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
    })

    yield app

    # Cleanup: fecha e remove o banco temporário
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Cliente HTTP para simular requisições à API."""
    return app.test_client()


@pytest.fixture
def sample_task():
    """Dados de exemplo para criação de uma tarefa."""
    return {
        "title": "Implementar login",
        "description": "Criar tela de autenticação com email e senha",
        "priority": "alta",
        "status": "pendente",
    }


@pytest.fixture
def sample_tasks():
    """Lista de tarefas para testes que precisam de múltiplos registros."""
    return [
        {"title": "Configurar CI/CD", "priority": "alta", "status": "concluida"},
        {"title": "Escrever testes unitários", "priority": "media", "status": "em_andamento"},
        {"title": "Revisar documentação", "priority": "baixa", "status": "pendente"},
        {"title": "Corrigir bug no login", "priority": "critica", "status": "pendente"},
        {"title": "Deploy em staging", "priority": "media", "status": "cancelada"},
    ]


@pytest.fixture
def populated_client(client, sample_tasks):
    """Cliente com banco já populado com tarefas de exemplo."""
    for task in sample_tasks:
        client.post("/api/tasks", json=task)
    return client
