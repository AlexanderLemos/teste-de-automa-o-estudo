# 🧪 Web Task Manager — Projeto de Testes com pytest

Projeto de demonstração de **testes automatizados** para uma aplicação web RESTful, utilizando **Python**, **Flask** e **pytest**.

> Desenvolvido como portfólio para demonstrar competências em **QA, testes unitários, testes de integração e automação de testes** em aplicações web.

---

## 🏗️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **Python 3.10+** | Linguagem principal |
| **Flask** | Framework web (API REST) |
| **pytest** | Framework de testes automatizados |
| **pytest-cov** | Cobertura de código |
| **SQLite** | Banco de dados leve |

---

## 📁 Estrutura do Projeto

```
web-task-manager/
├── app/
│   ├── __init__.py        # Factory da aplicação Flask
│   ├── models.py          # Modelos de dados (Task)
│   ├── routes.py          # Rotas da API REST
│   └── validators.py      # Validações de entrada
├── tests/
│   ├── conftest.py        # Fixtures compartilhadas
│   ├── test_models.py     # Testes unitários — Model
│   ├── test_validators.py # Testes unitários — Validações
│   ├── test_routes.py     # Testes de integração — API
│   └── test_cases.md      # Documentação de Casos de Teste
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🚀 Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar a aplicação
python -m flask --app app run --debug

# 3. Rodar os testes
pytest

# 4. Rodar com cobertura
pytest --cov=app --cov-report=term-missing
```

---

## 📋 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/tasks` | Listar todas as tarefas |
| `GET` | `/api/tasks/<id>` | Buscar tarefa por ID |
| `POST` | `/api/tasks` | Criar nova tarefa |
| `PUT` | `/api/tasks/<id>` | Atualizar tarefa |
| `DELETE` | `/api/tasks/<id>` | Deletar tarefa |
| `GET` | `/api/tasks/stats` | Estatísticas das tarefas |

---

## ✅ Tipos de Testes Implementados

- **Testes Unitários**: Validação de modelos e funções isoladas
- **Testes de Integração**: Validação dos endpoints da API completa
- **Testes Parametrizados**: Múltiplos cenários com `@pytest.mark.parametrize`
- **Fixtures**: Setup/teardown reutilizáveis com `conftest.py`
- **Cobertura de Código**: Relatório com `pytest-cov`

---

## 👤 Autor

**Alexander Souza de Lemos**
Engenharia de Software — FAMETRO (5º período)
[LinkedIn](https://www.linkedin.com/in/alexander-lemos)
