import streamlit as st
import pandas as pd
import os
from app.models.task import Task
from app.core.scheduler import adjust_task_schedule
from app.core.init_data import cargar_lista_proyectos
from app.core.data_access.responsible_repository import ResponsibleRepository  # 👈 tu clase

# -------------------------------
# 🔹 Cargar responsables desde CSV
# -------------------------------
responsible_repo = ResponsibleRepository()
df_responsibles = responsible_repo.load_all()

def obtener_factory_de_responsable(responsable: str) -> str:
    """
    Busca la fábrica/sede de un responsable desde el CSV.
    """
    if df_responsibles.empty:
        return "No asignada"

    row = df_responsibles[df_responsibles["name"].str.strip().str.lower() == responsable.strip().lower()]
    if not row.empty:
        return row.iloc[0]["factory"]
    return "No asignada"

# -------------------------------
# 🔹 Preparar una tarea en formato dict
# -------------------------------
def preparar_una_tarea(task):
    start = pd.to_datetime(task.start)
    end = pd.to_datetime(task.end)

    return {
        "Responsable": task.owner,
        "Fábrica/Sede": obtener_factory_de_responsable(task.owner),
        "Tarea": task.title,
        "Estado": task.estado,
        "Inicio": start.date(),
        "Fin": end.date(),
        "Duración estimada": f"{task.days} días",
        "Duración real": (end.date() - start.date()).days + 1 if start and end else "Inválido",
        #"Duración transcurrida": (pd.to_datetime("today").date() - start.date()).days + 1 if start else "Inválido",
    }

# -------------------------------
# 🔹 Preparar DataFrame de tareas
# -------------------------------
def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None

    tasks = adjust_task_schedule(tasks)
    data = [preparar_una_tarea(t) for t in tasks]
    df = pd.DataFrame(data)

    df["Duración real"] = df["Duración real"].apply(
        lambda x: f"{x} días" if x is not None else "Inválido"
    )
    '''df["Duración transcurrida"] = df["Duración transcurrida"].apply(
        lambda x: f"{x} días" if x is not None else "Inválido"
    )
    '''
    return df

# -------------------------------
# 🔹 Mostrar todas las tareas
# -------------------------------
DATA_DIR = os.path.join(os.getcwd(), "data")

def mostrar_todas_las_tareas():
    proyectos = cargar_lista_proyectos()
    lista_df = []

    for proyecto in proyectos:
        file_name = f"{proyecto.lower()}_tasks.csv"
        file_path = os.path.join(DATA_DIR, file_name)

        if not os.path.exists(file_path):
            continue

        df_csv = pd.read_csv(file_path)

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

        df_final = preparar_dataframe_tareas(tasks)

        if df_final is not None and not df_final.empty:
            df_final["Proyecto"] = proyecto
            lista_df.append(df_final)

    if lista_df:
        df_total = pd.concat(lista_df, ignore_index=True)
        return df_total

    return pd.DataFrame()