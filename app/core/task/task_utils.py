import os
from app.core.task.task_manager import load_tasks, save_all_tasks
from app.core.responsibles_manager import load_responsibles
from app.core.scheduler import adjust_task_schedule
from app.core.data_manager import DATA_DIR

def recalcular_tareas_responsables_por_pais(pais):
    print(f"[LOG] Iniciando recalculo para país: {pais}")
    responsibles = [r for r in load_responsibles() if r["location"] == pais]
    print(f"[LOG] Responsables encontrados para {pais}: {[r['name'] for r in responsibles]}")

    if not responsibles:
        print("[LOG] No hay responsables para el país.")
        return

    archivos_procesados = 0
    archivos_modificados = 0

    for archivo in os.listdir(DATA_DIR):
        if archivo.endswith("_tasks.csv") and archivo != "responsibles.csv":
            project_name = archivo.replace("_tasks.csv", "")
            print(f"[LOG] Procesando proyecto: {project_name}")
            tasks = load_tasks(project_name)
            print(f"[LOG] Total tareas cargadas: {len(tasks)}")

            modificadas = False

            for r in responsibles:
                nombre = r["name"]
                tareas_responsable = [t for t in tasks if t.owner == nombre]
                print(f"[LOG] Tareas de {nombre} encontradas: {len(tareas_responsable)}")

                if tareas_responsable:
                    nuevas_tareas = adjust_task_schedule(tareas_responsable)

                    # Reemplazar tareas viejas por las ajustadas
                    tasks = [t for t in tasks if t.owner != nombre]
                    tasks.extend(nuevas_tareas)
                    modificadas = True
                    print(f"[LOG] Tareas de {nombre} reagendadas.")

            if modificadas:
                save_all_tasks(project_name, tasks)
                archivos_modificados += 1
                print(f"[LOG] Proyecto '{project_name}' actualizado y guardado.")
            else:
                print(f"[LOG] No hubo cambios para proyecto '{project_name}'.")

            archivos_procesados += 1

    print(f"[LOG] Recalculo finalizado. Proyectos procesados: {archivos_procesados}, modificados: {archivos_modificados}")