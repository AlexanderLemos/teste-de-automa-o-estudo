"""
Testes Unitários — Validators

Testa as funções de validação de forma isolada (sem banco, sem Flask).
Demonstra uso de @pytest.mark.parametrize para múltiplos cenários.
"""

import pytest
from app.validators import (
    validate_title,
    validate_priority,
    validate_status,
    validate_task_data,
)


# =====================================================================
# TESTES DE VALIDAÇÃO DE TÍTULO
# =====================================================================

class TestValidateTitle:
    """Testes para a função validate_title."""

    @pytest.mark.unit
    def test_titulo_valido(self):
        """CT-01: Título com texto válido deve ser aceito."""
        is_valid, error = validate_title("Implementar login")
        assert is_valid is True
        assert error == ""

    @pytest.mark.unit
    def test_titulo_vazio(self):
        """CT-02: Título vazio deve ser rejeitado."""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert "obrigatório" in error.lower()

    @pytest.mark.unit
    def test_titulo_none(self):
        """CT-03: Título None deve ser rejeitado."""
        is_valid, error = validate_title(None)
        assert is_valid is False

    @pytest.mark.unit
    def test_titulo_somente_espacos(self):
        """CT-04: Título com apenas espaços deve ser rejeitado."""
        is_valid, error = validate_title("     ")
        assert is_valid is False

    @pytest.mark.unit
    def test_titulo_muito_curto(self):
        """CT-05: Título com menos de 3 caracteres deve ser rejeitado."""
        is_valid, error = validate_title("AB")
        assert is_valid is False
        assert "3 caracteres" in error

    @pytest.mark.unit
    def test_titulo_muito_longo(self):
        """CT-06: Título com mais de 100 caracteres deve ser rejeitado."""
        titulo_longo = "A" * 101
        is_valid, error = validate_title(titulo_longo)
        assert is_valid is False
        assert "100" in error

    @pytest.mark.unit
    def test_titulo_somente_numeros(self):
        """CT-07: Título contendo apenas números deve ser rejeitado."""
        is_valid, error = validate_title("12345")
        assert is_valid is False
        assert "números" in error.lower()

    @pytest.mark.unit
    @pytest.mark.parametrize("titulo", [
        "ABC",                          # Exatamente 3 caracteres (limite inferior)
        "A" * 100,                      # Exatamente 100 caracteres (limite superior)
        "Tarefa 123",                   # Mix de texto e números
        "Implementar autenticação JWT", # Título comum de projeto real
    ])
    def test_titulos_validos_parametrizado(self, titulo):
        """CT-08: Títulos válidos em diferentes formatos."""
        is_valid, _ = validate_title(titulo)
        assert is_valid is True


# =====================================================================
# TESTES DE VALIDAÇÃO DE PRIORIDADE
# =====================================================================

class TestValidatePriority:
    """Testes para a função validate_priority."""

    @pytest.mark.unit
    @pytest.mark.parametrize("priority", ["baixa", "media", "alta", "critica"])
    def test_prioridades_validas(self, priority):
        """CT-09: Todas as prioridades válidas devem ser aceitas."""
        is_valid, _ = validate_priority(priority)
        assert is_valid is True

    @pytest.mark.unit
    @pytest.mark.parametrize("priority", ["urgente", "normal", "ALTA", "", "123"])
    def test_prioridades_invalidas(self, priority):
        """CT-10: Prioridades inválidas devem ser rejeitadas."""
        is_valid, error = validate_priority(priority)
        assert is_valid is False
        assert "inválida" in error.lower()


# =====================================================================
# TESTES DE VALIDAÇÃO DE STATUS
# =====================================================================

class TestValidateStatus:
    """Testes para a função validate_status."""

    @pytest.mark.unit
    @pytest.mark.parametrize("status", [
        "pendente", "em_andamento", "concluida", "cancelada"
    ])
    def test_status_validos(self, status):
        """CT-11: Todos os status válidos devem ser aceitos."""
        is_valid, _ = validate_status(status)
        assert is_valid is True

    @pytest.mark.unit
    @pytest.mark.parametrize("status", ["finalizada", "ativa", "PENDENTE", ""])
    def test_status_invalidos(self, status):
        """CT-12: Status inválidos devem ser rejeitados."""
        is_valid, error = validate_status(status)
        assert is_valid is False
        assert "inválido" in error.lower()


# =====================================================================
# TESTES DE VALIDAÇÃO COMPLETA
# =====================================================================

class TestValidateTaskData:
    """Testes para a função validate_task_data (validação completa)."""

    @pytest.mark.unit
    def test_dados_validos_completos(self):
        """CT-13: Dados completos e válidos devem ser aceitos."""
        data = {
            "title": "Nova tarefa",
            "priority": "alta",
            "status": "pendente",
        }
        is_valid, errors = validate_task_data(data)
        assert is_valid is True
        assert errors == []

    @pytest.mark.unit
    def test_multiplos_erros(self):
        """CT-14: Dados com múltiplos erros devem retornar todos os erros."""
        data = {
            "title": "",
            "priority": "urgentissima",
            "status": "feita",
        }
        is_valid, errors = validate_task_data(data)
        assert is_valid is False
        assert len(errors) == 3  # título + prioridade + status

    @pytest.mark.unit
    def test_update_parcial_sem_titulo(self):
        """CT-15: Update parcial sem título não deve exigir título."""
        data = {"priority": "alta"}
        is_valid, errors = validate_task_data(data, is_update=True)
        assert is_valid is True
        assert errors == []
