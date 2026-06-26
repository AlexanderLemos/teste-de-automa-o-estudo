"""
Validators — Validação de dados de entrada.

Funções puras para validação de campos da Task, facilitando testes unitários.
"""


def validate_title(title: str) -> tuple[bool, str]:
    """
    Valida o título de uma tarefa.

    Regras:
        - Não pode ser vazio ou somente espaços
        - Deve ter entre 3 e 100 caracteres
        - Não pode conter apenas números

    Returns:
        Tupla (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "O título é obrigatório."

    title = title.strip()

    if len(title) < 3:
        return False, "O título deve ter pelo menos 3 caracteres."

    if len(title) > 100:
        return False, "O título deve ter no máximo 100 caracteres."

    if title.isdigit():
        return False, "O título não pode conter apenas números."

    return True, ""


def validate_priority(priority: str) -> tuple[bool, str]:
    """
    Valida a prioridade de uma tarefa.

    Valores aceitos: baixa, media, alta, critica.
    """
    valid_priorities = ("baixa", "media", "alta", "critica")

    if priority not in valid_priorities:
        return False, f"Prioridade inválida. Valores aceitos: {', '.join(valid_priorities)}."

    return True, ""


def validate_status(status: str) -> tuple[bool, str]:
    """
    Valida o status de uma tarefa.

    Valores aceitos: pendente, em_andamento, concluida, cancelada.
    """
    valid_statuses = ("pendente", "em_andamento", "concluida", "cancelada")

    if status not in valid_statuses:
        return False, f"Status inválido. Valores aceitos: {', '.join(valid_statuses)}."

    return True, ""


def validate_task_data(data: dict, is_update: bool = False) -> tuple[bool, list[str]]:
    """
    Valida todos os campos de uma tarefa.

    Args:
        data: Dicionário com os dados da tarefa.
        is_update: Se True, campos são opcionais (parcial update).

    Returns:
        Tupla (is_valid, list_of_errors)
    """
    errors = []

    # Validar título
    if "title" in data or not is_update:
        title = data.get("title", "")
        is_valid, error = validate_title(title)
        if not is_valid:
            errors.append(error)

    # Validar prioridade (se fornecida)
    if "priority" in data:
        is_valid, error = validate_priority(data["priority"])
        if not is_valid:
            errors.append(error)

    # Validar status (se fornecido)
    if "status" in data:
        is_valid, error = validate_status(data["status"])
        if not is_valid:
            errors.append(error)

    return len(errors) == 0, errors
