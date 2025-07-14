from typing import List, Callable
from app.models.task import Task
from app.core.scheduler import adjust_task_schedule
from app.core.task.task_manager import save_all_tasks


def actualizar_tareas_por_proyecto(
    proyecto: str, tareas: List[Task], get_feriados_func: Callable = None
):
    if get_feriados_func:
        tareas = adjust_task_schedule(tareas, get_feriados_func)
        save_all_tasks(proyecto, tareas, ajusta=False)
    else:
        save_all_tasks(proyecto, tareas)
    print(f"[LOG] Proyecto '{proyecto}' actualizado")