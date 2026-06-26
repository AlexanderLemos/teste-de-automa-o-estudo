"""
Routes — Rotas da API REST para gerenciamento de tarefas.

Endpoints:
    GET    /api/tasks       — Listar todas as tarefas
    GET    /api/tasks/<id>  — Buscar tarefa por ID
    POST   /api/tasks       — Criar nova tarefa
    PUT    /api/tasks/<id>  — Atualizar tarefa
    DELETE /api/tasks/<id>  — Deletar tarefa
    GET    /api/tasks/stats — Estatísticas das tarefas
"""

from flask import Blueprint, request, jsonify
from .models import Task, TaskRepository
from .validators import validate_task_data
from . import get_db

bp = Blueprint("tasks", __name__)


def get_repo():
    """Obtém instância do repositório de tarefas."""
    return TaskRepository(get_db())


@bp.route("/api/tasks", methods=["GET"])
def list_tasks():
    """Lista todas as tarefas."""
    repo = get_repo()
    tasks = repo.get_all()
    return jsonify({
        "tasks": [t.to_dict() for t in tasks],
        "count": len(tasks),
    }), 200


@bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Busca tarefa por ID."""
    repo = get_repo()
    task = repo.get_by_id(task_id)

    if not task:
        return jsonify({"error": "Tarefa não encontrada."}), 404

    return jsonify({"task": task.to_dict()}), 200


@bp.route("/api/tasks", methods=["POST"])
def create_task():
    """Cria uma nova tarefa."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Corpo da requisição vazio."}), 400

    # Validar dados de entrada
    is_valid, errors = validate_task_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    task = Task(
        title=data["title"].strip(),
        description=data.get("description", ""),
        priority=data.get("priority", "media"),
        status=data.get("status", "pendente"),
    )

    repo = get_repo()
    created = repo.create(task)

    return jsonify({
        "message": "Tarefa criada com sucesso.",
        "task": created.to_dict(),
    }), 201


@bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Atualiza uma tarefa existente."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Corpo da requisição vazio."}), 400

    # Validar dados (parcial — is_update=True)
    is_valid, errors = validate_task_data(data, is_update=True)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    repo = get_repo()
    updated = repo.update(task_id, data)

    if not updated:
        return jsonify({"error": "Tarefa não encontrada."}), 404

    return jsonify({
        "message": "Tarefa atualizada com sucesso.",
        "task": updated.to_dict(),
    }), 200


@bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deleta uma tarefa por ID."""
    repo = get_repo()
    deleted = repo.delete(task_id)

    if not deleted:
        return jsonify({"error": "Tarefa não encontrada."}), 404

    return jsonify({"message": "Tarefa deletada com sucesso."}), 200


@bp.route("/api/tasks/stats", methods=["GET"])
def task_stats():
    """Retorna estatísticas das tarefas."""
    repo = get_repo()
    stats = repo.get_stats()
    return jsonify({"stats": stats}), 200
