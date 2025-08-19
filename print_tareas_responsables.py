import pandas as pd
import os
from app.models.task import Task
from app.core.scheduler import adjust_task_schedule
from app.views.task_views_operations.mostrar_tareas import preparar_una_tarea
from app.core.init_data import cargar_lista_proyectos

# Carpeta donde están los CSV
DATA_DIR = os.path.join(os.getcwd(), "data")  # usa cwd para Streamlit
print("Buscando CSV en:", DATA_DIR)


def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None

    # Ajustar tareas según scheduler
    tasks = adjust_task_schedule(tasks)

    # Preparar DataFrame
    data = [preparar_una_tarea(t) for t in tasks]
    df = pd.DataFrame(data)

    # Formatear duraciones
    df["Duración real"] = df["Duración real"].apply(
        lambda x: f"{x} días" if x is not None else "Inválido"
    )
    df["Duración transcurrida"] = df["Duración transcurrida"].apply(
        lambda x: f"{x} días" if x is not None else "Inválido"
    )
    return df


def mostrar_todas_las_tareas():
    """
    Devuelve un único DataFrame con todas las tareas de todos los proyectos.
    Agrega la columna 'Proyecto' para identificar de dónde viene cada tarea.
    """
    proyectos = cargar_lista_proyectos()
    lista_df = []

    for proyecto in proyectos:
        file_name = f"{proyecto.lower()}_tasks.csv"
        file_path = os.path.join(DATA_DIR, file_name)

        if not os.path.exists(file_path):
            continue

        # Leer CSV
        df_csv = pd.read_csv(file_path)

        # Convertir filas a Task
        tasks = []
        for _, row in df_csv.iterrows():
            task_obj = Task(
                title=row["title"],
                owner=row["owner"],
                days=row["days"],
                start=pd.to_datetime(row["start"]),
                end=pd.to_datetime(row["end"]),
                estado=row.get("estado"),
                riesgo=row.get("riesgo"),
                tipo=row.get("tipo"),
            )
            tasks.append(task_obj)

        # Preparar DataFrame final
        df_final = preparar_dataframe_tareas(tasks)

        # Agregar columna de proyecto
        if df_final is not None and not df_final.empty:
            columnas = [
                "Responsable",
                "Tarea",
                "Estado",
                "Inicio",
                "Fin",
                "Duración estimada",
                "Duración real",
                "Duración transcurrida",
            ]
            df_final = df_final[columnas]
            df_final["Proyecto"] = proyecto  # 👈 columna nueva

            lista_df.append(df_final)

    # Concatenar todos los DataFrames en uno solo
    if lista_df:
        df_total = pd.concat(lista_df, ignore_index=True)
        return df_total

    return pd.DataFrame()  # DataFrame vacío si no hay tareas