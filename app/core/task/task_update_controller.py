# app/core/task/task_update_controller.py
from app.core.task.task_manager import load_tasks_by_responsible
from app.core.task.task_grouping_service import agrupar_tareas_por_proyecto
from app.core.task.task_update_service import actualizar_tareas_por_proyecto


def update_tasks_for_responsible(owner_name: str, get_feriados_func=None):
    tasks = load_tasks_by_responsible(owner_name)

    if not tasks:
        print(f"[LOG] No se encontraron tareas para responsable {owner_name}")
        return

    tareas_por_proyecto = agrupar_tareas_por_proyecto(tasks)

    for proyecto, tareas in tareas_por_proyecto.items():
        actualizar_tareas_por_proyecto(proyecto, tareas, get_feriados_func)