import pandas as pd
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas

def calcular_duracion_proyecto(tasks):
    """
    Devuelve inicio, fin y duración total en días de un conjunto de tareas.
    """
    df_tareas = preparar_dataframe_tareas(tasks)
    if df_tareas is None or df_tareas.empty:
        return None, None, 0

    # Convertir fechas a datetime
    df_tareas["Inicio"] = pd.to_datetime(df_tareas["Inicio"])
    df_tareas["Fin"] = pd.to_datetime(df_tareas["Fin"])

    fecha_inicio_min = df_tareas["Inicio"].min()
    fecha_fin_max = df_tareas["Fin"].max()
    rango_dias = (fecha_fin_max - fecha_inicio_min).days

    return fecha_inicio_min, fecha_fin_max, rango_dias