import pandas as pd
from datetime import timedelta
from app.core.scheduler import adjust_task_schedule

def preparar_dataframe(tasks):
    # Ajustar fechas considerando días hábiles y feriados
    tasks = adjust_task_schedule(tasks)

    df = pd.DataFrame([{
        "ID": t.id,
        "Tarea": t.title,
        "Responsable": t.owner,
        "Inicio": t.start,
        "Fin": t.end + timedelta(days=1),  # Para incluir el día completo
        "Duración Estimada": t.days,
        "Estado": t.estado,
        "Riesgo": t.riesgo,
        "Tipo": t.tipo,
    } for t in tasks])

    return df