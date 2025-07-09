import os
from app.core.task.task_manager import load_tasks, save_all_tasks
from app.core.responsibles_manager import load_responsibles
from app.core.scheduler import adjust_task_schedule
from app.core.data_manager import DATA_DIR


def filtrar_responsables_por_pais(pais):
    return [r for r in load_responsibles() if r["location"] == pais]


def obtener_tareas_por_responsable(tasks, responsable):
    return [t for t in tasks if t.owner == responsable["name"]]


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


def reemplazar_tareas_de_responsable(tasks, nombre, nuevas_tareas):
    return [t for t in tasks if t.owner != nombre] + nuevas_tareas


def recalcular_tareas_responsables_por_pais(pais):
    print(f"[LOG] Iniciando recalculo para país: {pais}")
    responsibles = filtrar_responsables_por_pais(pais)

    if not responsibles:
        print("[LOG] No hay responsables para el país.")
        return

    archivos_procesados = 0
    archivos_modificados = 0

    for archivo in os.listdir(DATA_DIR):
        if archivo.endswith("_tasks.csv") and archivo != "responsibles.csv":
            project_name = archivo.replace("_tasks.csv", "")
            fue_modificado = procesar_proyecto_para_responsables(project_name, responsibles)
            archivos_procesados += 1
            if fue_modificado:
                archivos_modificados += 1

    print(
        f"[LOG] Recalculo finalizado. Proyectos procesados: {archivos_procesados}, modificados: {archivos_modificados}"
    )