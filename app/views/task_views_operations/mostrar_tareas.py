from datetime import datetime, date
from app.utils.date_utils import calcular_duracion_real, calcular_duracion_transcurrida
import pandas as pd

def format_date(dt):
    if isinstance(dt, datetime):
        return dt.date()
    elif isinstance(dt, date):
        return dt
    else:
        return "Fecha inválida"

def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None
    
    data = []
    for task in tasks:
        duracion_real = calcular_duracion_real(task.start, task.end)
        duracion_transcurrida = calcular_duracion_transcurrida(task.start)
        data.append({
            "Responsable": task.owner,
            "Título": task.title,
            "Inicio": format_date(task.start),
            "Fin": format_date(task.end),
            "Duración estimada": f"{task.days} días",
            "Duración real": f"{duracion_real} días" if duracion_real is not None else "Inválido",
            "Duración transcurrida": f"{duracion_transcurrida} días" if duracion_transcurrida is not None else "Inválido",
            "Tipo": task.tipo,
            "Estado": task.estado,
            "Riesgo": task.riesgo
        })
    return pd.DataFrame(data)