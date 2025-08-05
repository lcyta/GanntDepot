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
    """
    Convierte los datos de proyectos a un DataFrame listo para Gantt.
    """
    proyectos_data = generar_datos_iniciales(project_list)
    registros = []

    for nombre, datos in proyectos_data.items():
        try:
            fecha_inicio = pd.to_datetime(datos["Inicio"]).date()
        except Exception:
            # Si no hay fecha válida, asignar hoy
            fecha_inicio = pd.Timestamp.today().date()

        duracion = int(datos.get("Duración estimada (días)", 0))
        fecha_fin = fecha_inicio + timedelta(days=duracion)

        registros.append({
            "Proyecto": nombre,
            "Inicio": fecha_inicio,
            "Fin": fecha_fin,
            "Responsable": datos.get("Responsable", ""),
            "Cliente": datos.get("Cliente", ""),
            "Localidad": datos.get("Localidad", ""),
            "Metros²": f"{datos.get('Metros²', 0)} m²",
            "Duración estimada": f"{duracion} días",
            "Estado": datos.get("Estado", "Pendiente")
        })

    return pd.DataFrame(registros)