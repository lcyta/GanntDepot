import streamlit as st
import pandas as pd
import os
from app.core.init_data import cargar_lista_proyectos
from app.core.data_manager import get_file_path
from app.core.task.project_duration import calcular_duracion_proyecto
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas

# Clase para adaptar filas de CSV a objetos con atributos
class TaskObj:
    def __init__(self, row):
        self.id = row.get("id")
        self.title = row.get("title", "Desconocido")
        self.owner = row.get("owner", "Desconocido")
        self.estado = row.get("estado", "Pendiente")
        self.start = pd.to_datetime(row.get("start")) if pd.notnull(row.get("start")) else None
        self.end = pd.to_datetime(row.get("end")) if pd.notnull(row.get("end")) else None
        self.days = row.get("days", 0)
        self.riesgo = row.get("riesgo", "Bajo")
        self.tipo = row.get("tipo", "Otras")

def mostrar_tareas_todos_proyectos():
    projects = cargar_lista_proyectos()
    if not projects:
        st.warning("No se encontraron proyectos.")
        return

    for project_name in projects:
        path = get_file_path(project_name)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            df_tasks = pd.read_csv(path)
        else:
            df_tasks = pd.DataFrame()

        tasks = [TaskObj(row) for _, row in df_tasks.iterrows()]

        # Reusar la función que ya hace todo el formateo y cálculo
        mostrar_tareas_existentes(tasks, project_name)

def mostrar_tareas_existentes(tasks, project_name):
    with st.expander(f"📑 Tareas existentes: {project_name}", expanded=False):
        df = preparar_dataframe_tareas(tasks)
        if df is None or df.empty:
            st.info("No hay tareas todavía.")
            return

        # Formatear fechas YYYY-MM-DD
        if "Inicio" in df.columns:
            df["Inicio"] = pd.to_datetime(df["Inicio"]).dt.strftime("%Y-%m-%d")
        if "Fin" in df.columns:
            df["Fin"] = pd.to_datetime(df["Fin"]).dt.strftime("%Y-%m-%d")

        # Mostrar en Streamlit
        st.dataframe(df, use_container_width=True)

        # Imprimir en consola
        print(f"\n--- Tareas del proyecto '{project_name}' ---")
        print(df)

        # Calcular duración total del proyecto
        inicio, fin, rango_dias = calcular_duracion_proyecto(tasks)
        if inicio and fin:
            st.success(f"📊 Duración total del proyecto '{project_name}': {rango_dias} días "
                       f"({inicio.date()} → {fin.date()})")
            print(f"Duración total del proyecto '{project_name}': {rango_dias} días")

            # Guardar en session_state para usar en el Gantt
            if "duracion_proyectos" not in st.session_state:
                st.session_state["duracion_proyectos"] = {}
            st.session_state["duracion_proyectos"][project_name] = (inicio, fin, rango_dias)