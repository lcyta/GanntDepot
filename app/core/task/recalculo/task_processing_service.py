from app.core.task.task_manager import load_tasks, save_all_tasks
from app.core.scheduler import adjust_task_schedule
from app.core.task.recalculo.task_filters import (
    obtener_tareas_por_responsable,
    reemplazar_tareas_de_responsable
)

def procesar_proyecto_para_responsables(project_name, responsibles):
    print(f"[LOG] Procesando proyecto: {project_name}")
    tasks = load_tasks(project_name)
    tareas_modificadas = False

    for responsable in responsibles:
        nombre = responsable["name"]
        tareas_responsable = obtener_tareas_por_responsable(tasks, responsable)
        print(f"[LOG] Tareas de {nombre} encontradas: {len(tareas_responsable)}")

        if tareas_responsable:
            nuevas_tareas = adjust_task_schedule(tareas_responsable)
            tasks = reemplazar_tareas_de_responsable(tasks, nombre, nuevas_tareas)
            tareas_modificadas = True
            print(f"[LOG] Tareas de {nombre} reagendadas.")

    if tareas_modificadas:
        save_all_tasks(project_name, tasks)
        print(f"[LOG] Proyecto '{project_name}' actualizado y guardado.")
        return True

    print(f"[LOG] No hubo cambios para proyecto '{project_name}'.")
    return False