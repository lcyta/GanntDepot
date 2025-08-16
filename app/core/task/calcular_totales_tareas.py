import pandas as pd
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
from app.core.data_manager import cargar_datos_guardados_proyectos, guardar_datos_proyecto

def calcular_totales_tareas(tasks):
    df = preparar_dataframe_tareas(tasks)
    if df is None or df.empty:
        return None

    # Pasar duraciones a número (sacando " días")
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

# Actualiza info del proyecto con los totales
def actualizar_info_proyecto_con_totales(tasks, project_name):
    totales_df = calcular_totales_tareas(tasks)
    if totales_df is None:
        print(f"No hay tareas para el proyecto {project_name}")
        return

    # Cargar info guardada del proyecto
    info_guardada = cargar_datos_guardados_proyectos([project_name])
    info = info_guardada.get(project_name, {})

    # Agregar totales al diccionario del proyecto
    for col in totales_df.columns:
        info[col] = int(totales_df.at[0, col])

    # Guardar cambios
    guardar_datos_proyecto(project_name, info)
    print(f"✅ Info del proyecto '{project_name}' actualizada con totales")