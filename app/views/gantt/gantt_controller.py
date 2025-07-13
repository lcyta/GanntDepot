from app.core.task.task_manager import load_tasks
from app.views.gantt.gantt_data_service import construir_datos_gantt_por_proyecto

def obtener_datos_gantt(project_list):
    datos = []
    for project in project_list:
        tasks = load_tasks(project)
        gantt_data = construir_datos_gantt_por_proyecto(tasks, project)
        if gantt_data:
            datos.append(gantt_data)
    return datos