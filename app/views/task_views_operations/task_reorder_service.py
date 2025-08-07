from app.core.scheduler import adjust_task_schedule

def reorder_tasks(tasks, mover_idx, destino_idx):
    """
    Reordena las tareas moviendo la tarea en `mover_idx`
    debajo de la tarea en `destino_idx`.
    """
    if mover_idx == destino_idx:
        return tasks, "❌ No se puede mover una tarea debajo de sí misma."

    if mover_idx < 0 or mover_idx >= len(tasks) or destino_idx < 0 or destino_idx >= len(tasks):
        return tasks, "❌ Índices fuera de rango."

    task_to_move = tasks.pop(mover_idx)

    # Ajuste por cambio de índice tras pop
    if mover_idx < destino_idx:
        destino_idx -= 1

    destino_idx = min(destino_idx, len(tasks) - 1)
    destino_titulo = tasks[destino_idx].title
    tasks.insert(destino_idx + 1, task_to_move)

    return tasks, f"✅ Tarea '{task_to_move.title}' movida debajo de '{destino_titulo}'"