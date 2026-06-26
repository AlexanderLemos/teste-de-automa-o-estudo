"""
Testes E2E com Playwright — Task Manager Web UI

Testa a interface web do Task Manager simulando interações reais do usuário
no navegador (clicar, digitar, verificar elementos).

Tipos de teste:
- Navegação e carregamento de página
- Criação de tarefas via formulário
- Validação de entrada (campos obrigatórios, mínimo de caracteres)
- Marcar tarefa como concluída (checkbox)
- Deletar tarefa
- Filtros (Todas, Ativas, Concluídas)
- Contadores/estatísticas em tempo real
"""

import re

import pytest
from playwright.sync_api import Page, expect


# URL da página (arquivo local)
PAGE_URL = "file:///C:/Users/AlexanderSL/.gemini/antigravity/scratch/web-task-manager/app/static/index.html"


# =====================================================================
# FIXTURES
# =====================================================================

@pytest.fixture(autouse=True)
def setup_page(page: Page):
    """Carrega a página antes de cada teste."""
    page.goto(PAGE_URL)
    page.wait_for_load_state("domcontentloaded")
    yield


# =====================================================================
# TESTES: Carregamento da Página
# =====================================================================

class TestPageLoad:
    """Verifica se a página carrega corretamente."""

    def test_titulo_da_pagina(self, page: Page):
        """E2E-01: A página deve ter o título correto."""
        expect(page).to_have_title("Task Manager")

    def test_elementos_principais_visiveis(self, page: Page):
        """E2E-02: Input, botão e lista devem estar visíveis."""
        expect(page.locator("#task-input")).to_be_visible()
        expect(page.locator("#add-btn")).to_be_visible()
        expect(page.locator("#task-list")).to_be_visible()

    def test_contadores_iniciam_zerados(self, page: Page):
        """E2E-03: Todos os contadores devem iniciar em 0."""
        expect(page.locator("#total-count")).to_have_text("0")
        expect(page.locator("#active-count")).to_have_text("0")
        expect(page.locator("#completed-count")).to_have_text("0")

    def test_estado_vazio_exibido(self, page: Page):
        """E2E-04: Mensagem de 'nenhuma tarefa' deve aparecer."""
        expect(page.locator(".empty-state")).to_be_visible()
        expect(page.locator(".empty-state")).to_contain_text("Nenhuma tarefa")


# =====================================================================
# TESTES: Criar Tarefa
# =====================================================================

class TestCreateTask:
    """Testa a criação de tarefas pelo formulário."""

    def test_criar_tarefa_com_clique(self, page: Page):
        """E2E-05: Digitar texto e clicar 'Adicionar' deve criar tarefa."""
        page.fill("#task-input", "Estudar Playwright")
        page.click("#add-btn")

        # Tarefa deve aparecer na lista
        expect(page.locator(".task-item")).to_have_count(1)
        expect(page.locator(".task-text")).to_have_text("Estudar Playwright")

    def test_criar_tarefa_com_enter(self, page: Page):
        """E2E-06: Pressionar Enter no input deve criar tarefa."""
        page.fill("#task-input", "Tarefa via Enter")
        page.press("#task-input", "Enter")

        expect(page.locator(".task-item")).to_have_count(1)

    def test_input_limpa_apos_criar(self, page: Page):
        """E2E-07: O input deve ficar vazio após criar tarefa."""
        page.fill("#task-input", "Tarefa teste")
        page.click("#add-btn")

        expect(page.locator("#task-input")).to_have_value("")

    def test_criar_multiplas_tarefas(self, page: Page):
        """E2E-08: Deve ser possível criar várias tarefas."""
        tarefas = ["Tarefa 1", "Tarefa 2", "Tarefa 3"]
        for tarefa in tarefas:
            page.fill("#task-input", tarefa)
            page.click("#add-btn")

        expect(page.locator(".task-item")).to_have_count(3)

    def test_criar_tarefa_com_prioridade_alta(self, page: Page):
        """E2E-09: Selecionar prioridade 'Alta' antes de criar."""
        page.select_option("#priority-select", "alta")
        page.fill("#task-input", "Tarefa urgente")
        page.click("#add-btn")

        expect(page.locator(".priority-alta")).to_be_visible()


# =====================================================================
# TESTES: Validação de Entrada
# =====================================================================

class TestValidation:
    """Testa validações do formulário."""

    def test_campo_vazio_mostra_erro(self, page: Page):
        """E2E-10: Clicar 'Adicionar' sem texto deve mostrar erro."""
        page.click("#add-btn")

        expect(page.locator("#error-message")).to_be_visible()
        expect(page.locator("#error-message")).to_contain_text("obrigatório")

    def test_titulo_curto_mostra_erro(self, page: Page):
        """E2E-11: Título com menos de 3 caracteres deve mostrar erro."""
        page.fill("#task-input", "AB")
        page.click("#add-btn")

        expect(page.locator("#error-message")).to_be_visible()
        expect(page.locator("#error-message")).to_contain_text("3 caracteres")

    def test_tarefa_nao_criada_com_erro(self, page: Page):
        """E2E-12: Nenhuma tarefa deve ser adicionada se houver erro."""
        page.click("#add-btn")  # campo vazio
        expect(page.locator(".task-item")).to_have_count(0)


# =====================================================================
# TESTES: Completar Tarefa (Checkbox)
# =====================================================================

class TestCompleteTask:
    """Testa a funcionalidade de marcar tarefa como concluída."""

    def test_marcar_como_concluida(self, page: Page):
        """E2E-13: Clicar no checkbox deve marcar tarefa como concluída."""
        page.fill("#task-input", "Tarefa para concluir")
        page.click("#add-btn")

        # Clicar no checkbox
        page.click(".task-checkbox")

        # Deve ter a classe 'completed'
        expect(page.locator(".task-item")).to_have_class(re.compile("completed"))

    def test_desmarcar_tarefa(self, page: Page):
        """E2E-14: Clicar no checkbox novamente deve desmarcar."""
        page.fill("#task-input", "Tarefa toggle")
        page.click("#add-btn")

        page.click(".task-checkbox")  # marca
        page.click(".task-checkbox")  # desmarca

        # Não deve ter 'completed'
        expect(page.locator(".task-item")).not_to_have_class(re.compile("completed"))


# =====================================================================
# TESTES: Deletar Tarefa
# =====================================================================

class TestDeleteTask:
    """Testa a funcionalidade de deletar tarefa."""

    def test_deletar_tarefa(self, page: Page):
        """E2E-15: Clicar no botão ✕ deve remover a tarefa."""
        page.fill("#task-input", "Tarefa para deletar")
        page.click("#add-btn")

        expect(page.locator(".task-item")).to_have_count(1)

        page.click(".delete-btn")

        expect(page.locator(".task-item")).to_have_count(0)

    def test_deletar_uma_de_varias(self, page: Page):
        """E2E-16: Deletar uma tarefa não deve afetar as outras."""
        page.fill("#task-input", "Tarefa A")
        page.click("#add-btn")
        page.fill("#task-input", "Tarefa B")
        page.click("#add-btn")

        expect(page.locator(".task-item")).to_have_count(2)

        # Deletar a primeira (mais recente, que está no topo)
        page.locator(".delete-btn").first.click()

        expect(page.locator(".task-item")).to_have_count(1)


# =====================================================================
# TESTES: Filtros
# =====================================================================

class TestFilters:
    """Testa os filtros de visualização."""

    def _create_mixed_tasks(self, page: Page):
        """Helper: cria 3 tarefas, completa 1."""
        for title in ["Ativa 1", "Ativa 2", "Concluída 1"]:
            page.fill("#task-input", title)
            page.click("#add-btn")

        # Marca a última como concluída (é a primeira da lista)
        page.locator(".task-checkbox").first.click()

    def test_filtro_todas(self, page: Page):
        """E2E-17: Filtro 'Todas' deve exibir todas as tarefas."""
        self._create_mixed_tasks(page)

        page.click('[data-filter="all"]')
        expect(page.locator(".task-item")).to_have_count(3)

    def test_filtro_ativas(self, page: Page):
        """E2E-18: Filtro 'Ativas' deve exibir apenas não-concluídas."""
        self._create_mixed_tasks(page)

        page.click('[data-filter="active"]')
        expect(page.locator(".task-item")).to_have_count(2)

    def test_filtro_concluidas(self, page: Page):
        """E2E-19: Filtro 'Concluídas' deve exibir apenas concluídas."""
        self._create_mixed_tasks(page)

        page.click('[data-filter="completed"]')
        expect(page.locator(".task-item")).to_have_count(1)

    def test_filtro_ativo_destacado(self, page: Page):
        """E2E-20: O botão do filtro selecionado deve ter classe 'active'."""
        page.click('[data-filter="active"]')
        expect(page.locator('[data-filter="active"]')).to_have_class(re.compile("active"))
        expect(page.locator('[data-filter="all"]')).not_to_have_class(re.compile("active"))


# =====================================================================
# TESTES: Contadores / Estatísticas
# =====================================================================

class TestCounters:
    """Testa os contadores em tempo real."""

    def test_contador_total(self, page: Page):
        """E2E-21: Contador 'Total' deve refletir o número de tarefas."""
        page.fill("#task-input", "Tarefa 1")
        page.click("#add-btn")
        page.fill("#task-input", "Tarefa 2")
        page.click("#add-btn")

        expect(page.locator("#total-count")).to_have_text("2")

    def test_contador_ativas(self, page: Page):
        """E2E-22: Contador 'Ativas' deve decrementar ao completar."""
        page.fill("#task-input", "Tarefa ativa")
        page.click("#add-btn")

        expect(page.locator("#active-count")).to_have_text("1")

        page.click(".task-checkbox")

        expect(page.locator("#active-count")).to_have_text("0")

    def test_contador_concluidas(self, page: Page):
        """E2E-23: Contador 'Concluídas' deve incrementar ao completar."""
        page.fill("#task-input", "Tarefa para concluir")
        page.click("#add-btn")

        expect(page.locator("#completed-count")).to_have_text("0")

        page.click(".task-checkbox")

        expect(page.locator("#completed-count")).to_have_text("1")

    def test_contadores_apos_deletar(self, page: Page):
        """E2E-24: Contadores devem atualizar após deletar tarefa."""
        page.fill("#task-input", "Tarefa temp")
        page.click("#add-btn")

        expect(page.locator("#total-count")).to_have_text("1")

        page.click(".delete-btn")

        expect(page.locator("#total-count")).to_have_text("0")
        expect(page.locator("#active-count")).to_have_text("0")


# =====================================================================
# TESTE: Fluxo E2E Completo
# =====================================================================

class TestE2EFlow:
    """Teste end-to-end: simula um fluxo completo de uso."""

    def test_fluxo_completo_usuario(self, page: Page):
        """E2E-25: Fluxo completo — criar, filtrar, completar, deletar."""
        # 1. Criar 3 tarefas com prioridades diferentes
        for title, priority in [
            ("Bug crítico no login", "alta"),
            ("Atualizar README", "baixa"),
            ("Escrever testes E2E", "media"),
        ]:
            page.select_option("#priority-select", priority)
            page.fill("#task-input", title)
            page.click("#add-btn")

        expect(page.locator("#total-count")).to_have_text("3")

        # 2. Completar uma tarefa
        page.locator(".task-checkbox").first.click()
        expect(page.locator("#completed-count")).to_have_text("1")
        expect(page.locator("#active-count")).to_have_text("2")

        # 3. Filtrar por ativas
        page.click('[data-filter="active"]')
        expect(page.locator(".task-item")).to_have_count(2)

        # 4. Filtrar por concluídas
        page.click('[data-filter="completed"]')
        expect(page.locator(".task-item")).to_have_count(1)

        # 5. Voltar para todas
        page.click('[data-filter="all"]')
        expect(page.locator(".task-item")).to_have_count(3)

        # 6. Deletar a tarefa concluída
        page.locator(".task-item.completed .delete-btn").click()
        expect(page.locator("#total-count")).to_have_text("2")
        expect(page.locator("#completed-count")).to_have_text("0")
