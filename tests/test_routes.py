"""
Testes de Integração — API Routes

Testa os endpoints da API completa (Flask + SQLite).
Simula requisições HTTP reais e valida respostas.
"""

import pytest


# =====================================================================
# TESTES: POST /api/tasks — Criar tarefa
# =====================================================================

class TestCreateTask:
    """Testes de integração para criação de tarefas."""

    @pytest.mark.integration
    def test_criar_tarefa_com_sucesso(self, client, sample_task):
        """CT-23: POST com dados válidos deve criar tarefa (201)."""
        response = client.post("/api/tasks", json=sample_task)
        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == "Tarefa criada com sucesso."
        assert data["task"]["title"] == sample_task["title"]
        assert data["task"]["id"] is not None

    @pytest.mark.integration
    def test_criar_tarefa_apenas_titulo(self, client):
        """CT-24: POST com apenas título deve criar tarefa com defaults."""
        response = client.post("/api/tasks", json={"title": "Tarefa simples"})
        assert response.status_code == 201

        task = response.get_json()["task"]
        assert task["priority"] == "media"
        assert task["status"] == "pendente"

    @pytest.mark.integration
    def test_criar_tarefa_sem_titulo(self, client):
        """CT-25: POST sem título deve retornar erro 400."""
        response = client.post("/api/tasks", json={"description": "Sem título"})
        assert response.status_code == 400

    @pytest.mark.integration
    def test_criar_tarefa_corpo_vazio(self, client):
        """CT-26: POST com corpo vazio deve retornar erro 400."""
        response = client.post(
            "/api/tasks",
            data="",
            content_type="application/json",
        )
        assert response.status_code == 400

    @pytest.mark.integration
    def test_criar_tarefa_prioridade_invalida(self, client):
        """CT-27: POST com prioridade inválida deve retornar erro 400."""
        response = client.post("/api/tasks", json={
            "title": "Tarefa teste",
            "priority": "urgentissima",
        })
        assert response.status_code == 400
        errors = response.get_json()["errors"]
        assert any("prioridade" in e.lower() for e in errors)


# =====================================================================
# TESTES: GET /api/tasks — Listar tarefas
# =====================================================================

class TestListTasks:
    """Testes de integração para listagem de tarefas."""

    @pytest.mark.integration
    def test_listar_tarefas_vazio(self, client):
        """CT-28: GET com banco vazio deve retornar lista vazia."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

        data = response.get_json()
        assert data["tasks"] == []
        assert data["count"] == 0

    @pytest.mark.integration
    def test_listar_tarefas_com_dados(self, populated_client):
        """CT-29: GET com dados deve retornar todas as tarefas."""
        response = populated_client.get("/api/tasks")
        assert response.status_code == 200

        data = response.get_json()
        assert data["count"] == 5
        assert len(data["tasks"]) == 5


# =====================================================================
# TESTES: GET /api/tasks/<id> — Buscar por ID
# =====================================================================

class TestGetTask:
    """Testes de integração para busca de tarefa por ID."""

    @pytest.mark.integration
    def test_buscar_tarefa_existente(self, client, sample_task):
        """CT-30: GET com ID válido deve retornar a tarefa."""
        # Criar tarefa
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.get_json()["task"]["id"]

        # Buscar
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.get_json()["task"]["title"] == sample_task["title"]

    @pytest.mark.integration
    def test_buscar_tarefa_inexistente(self, client):
        """CT-31: GET com ID inexistente deve retornar 404."""
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404
        assert "não encontrada" in response.get_json()["error"].lower()


# =====================================================================
# TESTES: PUT /api/tasks/<id> — Atualizar tarefa
# =====================================================================

class TestUpdateTask:
    """Testes de integração para atualização de tarefas."""

    @pytest.mark.integration
    def test_atualizar_titulo(self, client, sample_task):
        """CT-32: PUT com novo título deve atualizar a tarefa."""
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.get_json()["task"]["id"]

        response = client.put(f"/api/tasks/{task_id}", json={
            "title": "Título atualizado"
        })
        assert response.status_code == 200
        assert response.get_json()["task"]["title"] == "Título atualizado"

    @pytest.mark.integration
    def test_atualizar_status_para_concluida(self, client, sample_task):
        """CT-33: PUT alterando status para 'concluida'."""
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.get_json()["task"]["id"]

        response = client.put(f"/api/tasks/{task_id}", json={
            "status": "concluida"
        })
        assert response.status_code == 200
        assert response.get_json()["task"]["status"] == "concluida"

    @pytest.mark.integration
    def test_atualizar_tarefa_inexistente(self, client):
        """CT-34: PUT com ID inexistente deve retornar 404."""
        response = client.put("/api/tasks/9999", json={"title": "Teste"})
        assert response.status_code == 404

    @pytest.mark.integration
    def test_atualizar_com_dados_invalidos(self, client, sample_task):
        """CT-35: PUT com status inválido deve retornar 400."""
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.get_json()["task"]["id"]

        response = client.put(f"/api/tasks/{task_id}", json={
            "status": "finalizada"
        })
        assert response.status_code == 400


# =====================================================================
# TESTES: DELETE /api/tasks/<id> — Deletar tarefa
# =====================================================================

class TestDeleteTask:
    """Testes de integração para deleção de tarefas."""

    @pytest.mark.integration
    def test_deletar_tarefa_existente(self, client, sample_task):
        """CT-36: DELETE com ID válido deve remover a tarefa."""
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.get_json()["task"]["id"]

        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # Verificar que não existe mais
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    @pytest.mark.integration
    def test_deletar_tarefa_inexistente(self, client):
        """CT-37: DELETE com ID inexistente deve retornar 404."""
        response = client.delete("/api/tasks/9999")
        assert response.status_code == 404


# =====================================================================
# TESTES: GET /api/tasks/stats — Estatísticas
# =====================================================================

class TestTaskStats:
    """Testes de integração para estatísticas de tarefas."""

    @pytest.mark.integration
    def test_stats_banco_vazio(self, client):
        """CT-38: Stats com banco vazio deve retornar zeros."""
        response = client.get("/api/tasks/stats")
        assert response.status_code == 200

        stats = response.get_json()["stats"]
        assert stats["total"] == 0
        assert stats["taxa_conclusao"] == 0.0

    @pytest.mark.integration
    def test_stats_com_dados(self, populated_client):
        """CT-39: Stats com dados deve calcular corretamente."""
        response = populated_client.get("/api/tasks/stats")
        assert response.status_code == 200

        stats = response.get_json()["stats"]
        assert stats["total"] == 5
        assert stats["concluida"] == 1
        assert stats["em_andamento"] == 1
        assert stats["pendente"] == 2
        assert stats["cancelada"] == 1
        assert stats["taxa_conclusao"] == 20.0  # 1/5 = 20%


# =====================================================================
# TESTES: Fluxo completo (CRUD E2E)
# =====================================================================

class TestCRUDFlow:
    """Teste end-to-end: ciclo completo de vida de uma tarefa."""

    @pytest.mark.integration
    def test_ciclo_completo_tarefa(self, client):
        """CT-40: Fluxo completo — criar, ler, atualizar, concluir, deletar."""
        # 1. CRIAR
        response = client.post("/api/tasks", json={
            "title": "Deploy da aplicação",
            "priority": "critica",
        })
        assert response.status_code == 201
        task_id = response.get_json()["task"]["id"]

        # 2. LER
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.get_json()["task"]["status"] == "pendente"

        # 3. ATUALIZAR — mover para em_andamento
        response = client.put(f"/api/tasks/{task_id}", json={
            "status": "em_andamento"
        })
        assert response.status_code == 200
        assert response.get_json()["task"]["status"] == "em_andamento"

        # 4. CONCLUIR
        response = client.put(f"/api/tasks/{task_id}", json={
            "status": "concluida"
        })
        assert response.status_code == 200
        assert response.get_json()["task"]["status"] == "concluida"

        # 5. VERIFICAR STATS
        response = client.get("/api/tasks/stats")
        stats = response.get_json()["stats"]
        assert stats["total"] == 1
        assert stats["taxa_conclusao"] == 100.0

        # 6. DELETAR
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # 7. CONFIRMAR DELEÇÃO
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404


class TestStaticRoutes:
    """Testes para rotas estáticas (Frontend)."""

    @pytest.mark.integration
    def test_serve_index_html(self, client):
        """O root URL (/) deve servir o index.html (200)."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"Task Manager" in response.data

