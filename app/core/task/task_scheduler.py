from typing import Callable, List
from app.models.task import Task
from app.core.task.scheduler_helpers import agrupar_por_owner, ajustar_tareas_de_owner


def adjust_task_schedule(
    tasks: List[Task], get_feriados_func: Callable[[str], List[tuple]]
) -> List[Task]:
    tasks_by_owner = agrupar_por_owner(tasks)
    ajustadas = []

    for owner, tareas in tasks_by_owner.items():
        feriados = {f[0] for f in get_feriados_func(owner)}
        ajustadas += ajustar_tareas_de_owner(tareas, feriados)

    return ajustadas