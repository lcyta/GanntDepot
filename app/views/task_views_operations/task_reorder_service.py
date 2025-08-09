from app.core.scheduler import adjust_task_schedule

def validar_indices(mover_idx, destino_idx, total_tareas):
    if mover_idx == destino_idx:
        return False, "❌ No se puede mover una tarea debajo de sí misma."
    
    fuera_rango = not (0 <= mover_idx < total_tareas and 0 <= destino_idx < total_tareas)
    if fuera_rango:
        return False, "❌ Índices fuera de rango."
    
    return True, None

def reorder_tasks(tasks, mover_idx, destino_idx):
    """
    Reordena las tareas moviendo la tarea en `mover_idx`
    debajo de la tarea en `destino_idx`.
    """
    valido, mensaje = validar_indices(mover_idx, destino_idx, len(tasks))
    if not valido:
        return tasks, mensaje

    task_to_move = tasks.pop(mover_idx)

    if mover_idx < destino_idx:
        destino_idx -= 1

    destino_idx = min(destino_idx, len(tasks) - 1)
    destino_titulo = tasks[destino_idx].title
    tasks.insert(destino_idx + 1, task_to_move)

    return tasks, f"✅ Tarea '{task_to_move.title}' movida debajo de '{destino_titulo}'"