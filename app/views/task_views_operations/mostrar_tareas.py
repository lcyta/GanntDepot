import pandas as pd
from app.utils.date_utils import calcular_duracion_real, calcular_duracion_transcurrida

def format_duracion(duracion):
    return f"{duracion} días" if duracion is not None else "Inválido"

def preparar_una_tarea(task):
    """
    Convierte un objeto Task a diccionario para DataFrame.
    """
    duracion_real = calcular_duracion_real(getattr(task, "start", None), getattr(task, "end", None))
    duracion_transcurrida = calcular_duracion_transcurrida(getattr(task, "start", None))

    return {
        "Responsable": getattr(task, "owner", "Desconocido"),
        "Cliente": getattr(task, "cliente", "N/A"),            # Si no existe, poner "N/A"
        "Estado": getattr(task, "estado", "Pendiente"),
        "Localidad": getattr(task, "localidad", "N/A"),
        "Metros²": getattr(task, "metros", 0),
        "Inicio": getattr(task, "start", None),
        "Duración estimada": getattr(task, "duracion_estimada", 0),
        "Duración real": f"{duracion_real} días" if duracion_real is not None else "Inválido",
        "Duración transcurrida": f"{duracion_transcurrida} días" if duracion_transcurrida is not None else "Inválido"
    }

def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None
    data = [preparar_una_tarea(task) for task in tasks]
    return pd.DataFrame(data)

def calcular_totales_tareas(tasks):
    df = preparar_dataframe_tareas(tasks)
    if df is None or df.empty:
        return None

    # Pasar duraciones a número
    df["Duración estimada"] = df["Duración estimada"].astype(int)
    df["Duración real"] = df["Duración real"].str.replace(" días", "").astype(int)
    df["Duración transcurrida"] = df["Duración transcurrida"].str.replace(" días", "").astype(int)

    resumen = {
        "Duración estimada total": df["Duración estimada"].sum(),
        "Duración real total": df["Duración real"].sum(),
        "Duración transcurrida total": df["Duración transcurrida"].sum()
    }

    resumen_df = pd.DataFrame([resumen])
    print("\n📊 Resumen de Duraciones")
    print(resumen_df)
    return resumen_df

def actualizar_info_proyecto_con_totales(tasks, project_name, cargar_datos_guardados_proyectos, guardar_datos_proyecto):
    totales_df = calcular_totales_tareas(tasks)
    if totales_df is None:
        print(f"No hay tareas para el proyecto {project_name}")
        return

    info_guardada = cargar_datos_guardados_proyectos([project_name])
    info = info_guardada.get(project_name, {})

    for col in totales_df.columns:
        info[col] = int(totales_df.at[0, col])

    guardar_datos_proyecto(project_name, info)
    print(f"✅ Info del proyecto '{project_name}' actualizada con totales")