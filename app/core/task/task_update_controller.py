from collections import defaultdict
from app.core.scheduler import adjust_task_schedule
from app.core.task.task_manager import load_tasks_by_responsible, save_all_tasks

def update_tasks_for_responsible(owner_name: str):
    tasks = load_tasks_by_responsible(owner_name)

    if not tasks:
        print(f"[LOG] No se encontraron tareas para responsable {owner_name}")
        return

    tasks_por_proyecto = defaultdict(list)
    for task in tasks:
        if not hasattr(task, 'project_name') or not task.project_name:
            print(f"[WARN] Tarea sin proyecto: {task.title}")
            continue
        tasks_por_proyecto[task.project_name].append(task)

    for proyecto, tareas in tasks_por_proyecto.items():
        tareas_ajustadas = adjust_task_schedule(tareas)
        save_all_tasks(proyecto, tareas_ajustadas)
        print(f"[LOG] Proyecto '{proyecto}' actualizado")

