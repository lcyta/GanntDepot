from collections import defaultdict
from app.models.task import Task
from typing import List, Dict


def agrupar_tareas_por_proyecto(tasks: List[Task]) -> Dict[str, List[Task]]:
    tareas_por_proyecto = defaultdict(list)
    for task in tasks:
        if not hasattr(task, "project_name") or not task.project_name:
            print(f"[WARN] Tarea sin proyecto: {task.title}")
            continue
        tareas_por_proyecto[task.project_name].append(task)
    return tareas_por_proyecto