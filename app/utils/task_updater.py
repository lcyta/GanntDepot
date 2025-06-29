from app.core.task_manager import load_tasks, save_all_tasks,load_tasks_by_responsible
from app.core.scheduler import adjust_task_schedule

def update_tasks_for_responsible(owner_name):
    tasks = load_tasks_by_responsible(owner_name)
    if not tasks:
        print(f"[LOG] No se encontraron tareas para responsable {owner_name}")
        return

    print(f"[LOG] {len(tasks)} tareas encontradas para responsable {owner_name}")

    tasks_por_proyecto = {}
    for t in tasks:
        tasks_por_proyecto.setdefault(t.project_name, []).append(t)

    for proyecto, tareas in tasks_por_proyecto.items():
        print(f"[LOG] Ajustando tareas en proyecto: {proyecto}")
        todas = load_tasks(proyecto)
        todas = [t for t in todas if t.owner != owner_name]
        nuevas = adjust_task_schedule(tareas)
        todas.extend(nuevas)
        save_all_tasks(proyecto, todas)
        print(f"[LOG] Guardado exitoso de tareas ajustadas en {proyecto}")