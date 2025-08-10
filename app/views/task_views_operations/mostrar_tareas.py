from datetime import datetime, date
import pandas as pd
from app.utils.date_utils import calcular_duracion_real, calcular_duracion_transcurrida

def format_date(dt):
    if isinstance(dt, datetime):
        return dt.date()
    elif isinstance(dt, date):
        return dt
    else:
        return "Fecha inválida"

def format_duracion(duracion):
    return f"{duracion} días" if duracion is not None else "Inválido"

def preparar_una_tarea(task):
    duracion_real = calcular_duracion_real(task.start, task.end)
    duracion_transcurrida = calcular_duracion_transcurrida(task.start)
    return {
        "Responsable": task.owner,
        "Título": task.title,
        "Inicio": format_date(task.start),
        "Fin": format_date(task.end),
        "Duración estimada": f"{task.days} días",
        "Duración real": format_duracion(duracion_real),
        "Duración transcurrida": format_duracion(duracion_transcurrida),
        "Tipo": task.tipo,
        "Estado": task.estado,
        "Riesgo": task.riesgo,
    }

def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None
    
    data = [preparar_una_tarea(task) for task in tasks]
    return pd.DataFrame(data)