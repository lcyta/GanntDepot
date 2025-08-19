import pandas as pd
from app.utils.date_utils import calcular_duracion_real, calcular_duracion_transcurrida

def format_duracion(duracion):
    return f"{duracion} días" if duracion is not None else "Inválido"

def preparar_una_tarea(task):
    inicio = getattr(task, "start", None)
    duracion_real = calcular_duracion_real(inicio, getattr(task, "end", None))
    duracion_transcurrida = calcular_duracion_transcurrida(inicio)

    # Calcular fecha de fin real
    fin = inicio + pd.Timedelta(days=duracion_real) if inicio is not None and duracion_real is not None else None

    return {
        "Responsable": getattr(task, "owner", "Desconocido"),
        "Tarea": getattr(task, "title", "Desconocido"),
        "Estado": getattr(task, "estado", "Pendiente"),
        "Inicio": inicio,
        "Fin": fin,
        "Duración estimada": getattr(task, "days", 0),
        "Duración real": duracion_real,
        "Duración transcurrida": duracion_transcurrida
    }

def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None
    data = [preparar_una_tarea(task) for task in tasks]
    df = pd.DataFrame(data)

    # Opcional: formatear las columnas para mostrar en Streamlit
    df["Duración real"] = df["Duración real"].apply(format_duracion)
    df["Duración transcurrida"] = df["Duración transcurrida"].apply(format_duracion)

    return df