import streamlit as st
import plotly.figure_factory as ff
from app.views.gantt.gantt_controller import obtener_datos_gantt

def view_projects_gantt(project_list):
    st.subheader("📅 Diagrama Gantt de todos los proyectos")

    gantt_data = obtener_datos_gantt(project_list)

    if not gantt_data:
        st.info("No hay tareas en ningún proyecto.")
        return

    fig = ff.create_gantt(
        gantt_data,
        index_col="Resource",
        show_colorbar=True,
        group_tasks=True
    )
    st.plotly_chart(fig, use_container_width=True)