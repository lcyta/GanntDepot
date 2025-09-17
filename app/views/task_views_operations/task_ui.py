import streamlit as st
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
import pandas as pd
from app.core.task.project_duration import calcular_duracion_proyecto
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# ------------------------
# Helpers
# ------------------------
def resaltar_estado(row):
    color = ""
    if row["Estado"] == "Terminado":
        color = "background-color: #d4edda; color: #155724;"
    elif row["Estado"] == "En curso":
        color = "background-color: #fff3cd; color: #856404;"
    elif row["Estado"] == "En Espera":
        color = "background-color: #f8d7da; color: #721c24;"
    return [color] * len(row)

def mostrar_dataframe_styled(df):
    df_styled = df.style.apply(resaltar_estado, axis=1)
    st.dataframe(df_styled, use_container_width=True)

def imprimir_tareas_consola(project_name, df):
    print(f"\n--- Tareas del proyecto '{project_name}' ---")
    print(df)

def actualizar_duracion_proyecto(project_name, tasks):
    inicio, fin, rango_dias = calcular_duracion_proyecto(tasks)
    if inicio and fin:
        st.success(f"📊 Duración total del proyecto: {rango_dias} días "
                   f"({inicio.date()} → {fin.date()})")
        print(f"Duración total del proyecto '{project_name}': {rango_dias} días")

        if "duracion_proyectos" not in st.session_state:
            st.session_state["duracion_proyectos"] = {}
        st.session_state["duracion_proyectos"][project_name] = (inicio, fin, rango_dias)

# ------------------------
# Función principal
# ------------------------
def mostrar_tareas_existentes(tasks, project_name):
    with st.expander("📑 Tareas existentes", expanded=False):
        df = preparar_dataframe_tareas(tasks)
        if df is None or df.empty:
            st.info("No hay tareas todavía.")
            return

        mostrar_dataframe_styled(df)
        imprimir_tareas_consola(project_name, df)
        actualizar_duracion_proyecto(project_name, tasks)
        return df