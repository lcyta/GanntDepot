import streamlit as st
from app.views.responsibles_view.data_loader import cargar_tareas
from app.views.responsibles_view.filtros import mostrar_filtros, aplicar_filtros
from app.views.responsibles_view.tabla import mostrar_tabla
from app.views.responsibles_view.gantt import mostrar_gantt

def mostrar_tareas_view_list():
    df = cargar_tareas()
    if df is None or df.empty:
        st.info("No hay tareas disponibles.")
        return

    with st.expander("📂 Lista tareas responsables", expanded=False):
        # 1. Filtros
        f_proyecto, f_responsable, f_estado, f_factory = mostrar_filtros(df)
        # 2. Aplicar filtros
        df_filtrado = aplicar_filtros(df, f_proyecto, f_responsable, f_estado, f_factory)
        # 3. Tabla
        mostrar_tabla(df_filtrado)
        # 4. Gantt
        mostrar_gantt(df_filtrado)