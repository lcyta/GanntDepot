from app.core.task_manager import load_tasks_by_responsible, save_all_tasks
from app.core.scheduler import adjust_task_schedule
from collections import defaultdict

def update_tasks_for_responsible(owner_name: str):
    """
    Carga todas las tareas del responsable, recalcula fechas
    y guarda las tareas en sus respectivos proyectos.
    """

    # Cargar todas las tareas asignadas al responsable (de todos los proyectos)
    tasks = load_tasks_by_responsible(owner_name)

    if not tasks:
        print(f"[LOG] No se encontraron tareas para responsable {owner_name}")
        return

    print(f"[LOG] {len(tasks)} tareas encontradas para responsable {owner_name}")

    # Agrupar tareas por proyecto para procesar y guardar por proyecto
    tasks_por_proyecto = defaultdict(list)
    for task in tasks:
        if not hasattr(task, 'project_name') or not task.project_name:
            print(f"[WARN] La tarea '{task.title}' no tiene asignado proyecto. Se omite.")
            continue
        tasks_por_proyecto[task.project_name].append(task)

    # Procesar cada proyecto por separado
    for proyecto, tareas in tasks_por_proyecto.items():
        # Recalcular fechas
        tareas_ajustadas = adjust_task_schedule(tareas)

        # Guardar las tareas ajustadas
        save_all_tasks(proyecto, tareas_ajustadas)

        print(f"[LOG] Tareas actualizadas y guardadas en proyecto '{proyecto}'")