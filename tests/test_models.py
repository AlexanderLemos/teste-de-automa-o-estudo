"""
Testes Unitários — Models

Testa o modelo Task de forma isolada (sem banco de dados).
Valida a lógica de negócio dos métodos do modelo.
"""

import pytest
from app.models import Task


class TestTaskModel:
    """Testes unitários para o modelo Task."""

    @pytest.mark.unit
    def test_criar_task_com_valores_padrao(self):
        """CT-16: Task criada apenas com título deve ter defaults corretos."""
        task = Task(title="Minha tarefa")
        assert task.title == "Minha tarefa"
        assert task.description == ""
        assert task.priority == "media"
        assert task.status == "pendente"
        assert task.id is None

    @pytest.mark.unit
    def test_criar_task_com_todos_campos(self):
        """CT-17: Task criada com todos os campos preenchidos."""
        task = Task(
            title="Tarefa completa",
            description="Descrição detalhada",
            priority="critica",
            status="em_andamento",
            id=42,
        )
        assert task.id == 42
        assert task.priority == "critica"
        assert task.status == "em_andamento"

    @pytest.mark.unit
    def test_to_dict(self):
        """CT-18: Serialização para dicionário deve conter todas as chaves."""
        task = Task(title="Test", id=1)
        result = task.to_dict()
        expected_keys = {"id", "title", "description", "priority", "status", "created_at", "updated_at"}
        assert set(result.keys()) == expected_keys
        assert result["id"] == 1
        assert result["title"] == "Test"

    @pytest.mark.unit
    def test_is_completed_verdadeiro(self):
        """CT-19: Tarefa com status 'concluida' deve retornar True."""
        task = Task(title="Done", status="concluida")
        assert task.is_completed() is True

    @pytest.mark.unit
    @pytest.mark.parametrize("status", ["pendente", "em_andamento", "cancelada"])
    def test_is_completed_falso(self, status):
        """CT-20: Tarefa com status diferente de 'concluida' deve retornar False."""
        task = Task(title="Not done", status=status)
        assert task.is_completed() is False

    @pytest.mark.unit
    @pytest.mark.parametrize("status,expected", [
        ("pendente", True),
        ("em_andamento", True),
        ("concluida", False),
        ("cancelada", False),
    ])
    def test_is_active(self, status, expected):
        """CT-21: Verifica se is_active retorna corretamente para cada status."""
        task = Task(title="Test", status=status)
        assert task.is_active() is expected

    @pytest.mark.unit
    @pytest.mark.parametrize("priority,expected", [
        ("baixa", False),
        ("media", False),
        ("alta", True),
        ("critica", True),
    ])
    def test_is_high_priority(self, priority, expected):
        """CT-22: Verifica se is_high_priority funciona para cada prioridade."""
        task = Task(title="Test", priority=priority)
        assert task.is_high_priority() is expected
