from app.core.responsibles_manager import load_responsibles
from app.core.task.recalculo.task_filters import filtrar_responsables_por_pais
from app.core.task.recalculo.task_file_service import obtener_archivos_tasks
from app.core.task.recalculo.batch_task_processing import procesar_archivos_por_responsables
from app.core.data_manager import DATA_DIR


def obtener_responsables_por_pais(pais):
    responsibles = load_responsibles()
    filtrados = filtrar_responsables_por_pais(responsibles, pais)
    if not filtrados:
        print(f"[LOG] No hay responsables para el país: {pais}")
    return filtrados


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