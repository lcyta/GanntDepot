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


def obtener_responsables_por_pais(pais):
    responsibles = filtrar_responsables_por_pais(pais)
    if not responsibles:
        print(f"[LOG] No hay responsables para el país: {pais}")
    return responsibles

def obtener_archivos_tasks(data_dir):
    return [
        f for f in os.listdir(data_dir)
        if f.endswith("_tasks.csv") and f != "responsibles.csv"
    ]

def procesar_archivos_por_responsables(archivos, responsibles):
    procesados = 0
    modificados = 0
    for archivo in archivos:
        project_name = archivo.replace("_tasks.csv", "")
        fue_modificado = procesar_proyecto_para_responsables(project_name, responsibles)
        procesados += 1
        if fue_modificado:
            modificados += 1
    return procesados, modificados

def recalcular_tareas_responsables_por_pais(pais, data_dir=DATA_DIR):
    print(f"[LOG] Iniciando recalculo para país: {pais}")
    responsibles = obtener_responsables_por_pais(pais)
    if not responsibles:
        return

    archivos = obtener_archivos_tasks(data_dir)
    procesados, modificados = procesar_archivos_por_responsables(archivos, responsibles)

    print(
        f"[LOG] Recalculo finalizado. Proyectos procesados: {procesados}, modificados: {modificados}"
    )