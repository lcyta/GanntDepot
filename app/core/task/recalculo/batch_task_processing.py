from app.core.task.recalculo.task_processing_service import procesar_proyecto_para_responsables

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