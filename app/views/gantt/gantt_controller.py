from app.core.task.task_manager import load_tasks
from app.views.gantt.gantt_data_service import construir_datos_gantt_por_proyecto
import pandas as pd
from app.core.init_data import generar_datos_iniciales
from datetime import timedelta

def obtener_datos_gantt(project_list):
    datos = []
    for project in project_list:
        tasks = load_tasks(project)
        gantt_data = construir_datos_gantt_por_proyecto(tasks, project)
        if gantt_data:
            datos.append(gantt_data)
    return datos

def obtener_dataframe_proyectos(project_list):
    proyectos_data = generar_datos_iniciales(project_list)

    registros = []
    for nombre, datos in proyectos_data.items():
        # Se elimina el filtro por estado para incluir todos
        fecha_inicio = datos["Inicio"]
        duracion = datos["Duración estimada (días)"]
        fecha_fin = fecha_inicio + timedelta(days=duracion)

        registros.append({
            "Proyecto": nombre,
            "Inicio": fecha_inicio,
            "Fin": fecha_fin,
            "Responsable": datos["Responsable"],
            "Cliente": datos["Cliente"],
            "Localidad": datos["Localidad"],
            "Metros²": f"{datos['Metros²']} m²",
            "Duración estimada": f"{duracion} días",
            "Estado": datos["Estado"]
        })

    return pd.DataFrame(registros)