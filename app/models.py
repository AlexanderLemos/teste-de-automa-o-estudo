"""
Models — Representação de dados da aplicação.

Define a estrutura da entidade Task e operações de CRUD no banco de dados.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Modelo de dados para uma Tarefa."""

    title: str
    description: str = ""
    priority: str = "media"
    status: str = "pendente"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Valores válidos para validação
    VALID_PRIORITIES = ("baixa", "media", "alta", "critica")
    VALID_STATUSES = ("pendente", "em_andamento", "concluida", "cancelada")

    def to_dict(self) -> dict:
        """Converte a task para dicionário (serialização JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_completed(self) -> bool:
        """Verifica se a tarefa está concluída."""
        return self.status == "concluida"

    def is_active(self) -> bool:
        """Verifica se a tarefa está ativa (pendente ou em andamento)."""
        return self.status in ("pendente", "em_andamento")

    def is_high_priority(self) -> bool:
        """Verifica se a tarefa é de alta prioridade ou crítica."""
        return self.priority in ("alta", "critica")


class TaskRepository:
    """Repositório para operações de CRUD de tarefas no banco SQLite."""

    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[Task]:
        """Retorna todas as tarefas."""
        rows = self.db.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC"
        ).fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Busca tarefa por ID."""
        row = self.db.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return self._row_to_task(row) if row else None

    def create(self, task: Task) -> Task:
        """Cria uma nova tarefa no banco."""
        cursor = self.db.execute(
            """INSERT INTO tasks (title, description, priority, status)
               VALUES (?, ?, ?, ?)""",
            (task.title, task.description, task.priority, task.status),
        )
        self.db.commit()
        task.id = cursor.lastrowid
        return self.get_by_id(task.id)

    def update(self, task_id: int, data: dict) -> Optional[Task]:
        """Atualiza uma tarefa existente."""
        existing = self.get_by_id(task_id)
        if not existing:
            return None

        title = data.get("title", existing.title)
        description = data.get("description", existing.description)
        priority = data.get("priority", existing.priority)
        status = data.get("status", existing.status)

        self.db.execute(
            """UPDATE tasks
               SET title = ?, description = ?, priority = ?, status = ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (title, description, priority, status, task_id),
        )
        self.db.commit()
        return self.get_by_id(task_id)

    def delete(self, task_id: int) -> bool:
        """Deleta uma tarefa por ID. Retorna True se deletou."""
        cursor = self.db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db.commit()
        return cursor.rowcount > 0

    def get_stats(self) -> dict:
        """Retorna estatísticas das tarefas."""
        tasks = self.get_all()
        total = len(tasks)

        if total == 0:
            return {
                "total": 0,
                "pendente": 0,
                "em_andamento": 0,
                "concluida": 0,
                "cancelada": 0,
                "taxa_conclusao": 0.0,
            }

        stats = {
            "total": total,
            "pendente": sum(1 for t in tasks if t.status == "pendente"),
            "em_andamento": sum(1 for t in tasks if t.status == "em_andamento"),
            "concluida": sum(1 for t in tasks if t.status == "concluida"),
            "cancelada": sum(1 for t in tasks if t.status == "cancelada"),
        }
        stats["taxa_conclusao"] = round(
            (stats["concluida"] / total) * 100, 2
        )
        return stats

    @staticmethod
    def _row_to_task(row) -> Task:
        """Converte uma row do SQLite para um objeto Task."""
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
