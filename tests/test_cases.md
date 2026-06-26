# 📋 Documentação de Casos de Teste — Web Task Manager

## Convenções
- **CT-XX**: Identificador do caso de teste
- **Tipo**: Unitário (U) | Integração (I)
- **Prioridade**: Alta (A) | Média (M) | Baixa (B)

---

## Validadores (`test_validators.py`)

| ID | Tipo | Prioridade | Cenário | Resultado Esperado |
|----|------|------------|---------|--------------------|
| CT-01 | U | A | Título com texto válido | Aceito |
| CT-02 | U | A | Título vazio ("") | Rejeitado — "obrigatório" |
| CT-03 | U | A | Título None | Rejeitado |
| CT-04 | U | M | Título só com espaços | Rejeitado |
| CT-05 | U | M | Título < 3 caracteres | Rejeitado — "3 caracteres" |
| CT-06 | U | M | Título > 100 caracteres | Rejeitado — "100" |
| CT-07 | U | B | Título só com números | Rejeitado — "números" |
| CT-08 | U | M | Títulos válidos (parametrizado) | Aceito (4 cenários) |
| CT-09 | U | A | Prioridades válidas | Aceito (4 valores) |
| CT-10 | U | A | Prioridades inválidas | Rejeitado (5 valores) |
| CT-11 | U | A | Status válidos | Aceito (4 valores) |
| CT-12 | U | A | Status inválidos | Rejeitado (4 valores) |
| CT-13 | U | A | Dados completos e válidos | Aceito, sem erros |
| CT-14 | U | M | Dados com 3 erros | Rejeitado, retorna 3 erros |
| CT-15 | U | M | Update parcial sem título | Aceito (título não exigido) |

## Modelos (`test_models.py`)

| ID | Tipo | Prioridade | Cenário | Resultado Esperado |
|----|------|------------|---------|--------------------|
| CT-16 | U | A | Task criada só com título | Defaults: media, pendente, id=None |
| CT-17 | U | M | Task com todos os campos | Valores corretos atribuídos |
| CT-18 | U | A | to_dict() serialização | Dict com 7 chaves esperadas |
| CT-19 | U | M | is_completed() com "concluida" | True |
| CT-20 | U | M | is_completed() com outros status | False (3 cenários) |
| CT-21 | U | M | is_active() por status | Parametrizado (4 cenários) |
| CT-22 | U | M | is_high_priority() por prioridade | Parametrizado (4 cenários) |

## API — Rotas (`test_routes.py`)

| ID | Tipo | Prioridade | Cenário | Resultado Esperado |
|----|------|------------|---------|--------------------|
| CT-23 | I | A | POST /api/tasks — dados válidos | 201, tarefa criada |
| CT-24 | I | M | POST — apenas título | 201, defaults aplicados |
| CT-25 | I | A | POST — sem título | 400, erro de validação |
| CT-26 | I | M | POST — corpo vazio | 400, erro |
| CT-27 | I | M | POST — prioridade inválida | 400, erro de prioridade |
| CT-28 | I | M | GET /api/tasks — banco vazio | 200, lista vazia, count=0 |
| CT-29 | I | A | GET /api/tasks — com dados | 200, count=5 |
| CT-30 | I | A | GET /api/tasks/id — existente | 200, tarefa retornada |
| CT-31 | I | A | GET /api/tasks/id — inexistente | 404, "não encontrada" |
| CT-32 | I | A | PUT — atualizar título | 200, título alterado |
| CT-33 | I | M | PUT — status → concluida | 200, status alterado |
| CT-34 | I | M | PUT — ID inexistente | 404 |
| CT-35 | I | M | PUT — dados inválidos | 400 |
| CT-36 | I | A | DELETE — tarefa existente | 200, tarefa removida |
| CT-37 | I | M | DELETE — ID inexistente | 404 |
| CT-38 | I | M | GET /stats — banco vazio | 200, total=0 |
| CT-39 | I | A | GET /stats — com dados | 200, cálculos corretos |
| CT-40 | I | A | Fluxo CRUD completo (E2E) | Criar → Ler → Atualizar → Concluir → Deletar |

---

## Resumo

| Métrica | Valor |
|---------|-------|
| **Total de casos de teste** | 40 |
| **Testes unitários** | 22 |
| **Testes de integração** | 18 |
| **Testes parametrizados** | 7 (cobrindo 28+ cenários) |
| **Cobertura estimada** | 90%+ |
