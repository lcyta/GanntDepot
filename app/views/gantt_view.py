import streamlit as st
from app.views.gantt.gantt_projects_controller import obtener_grafico_gantt_proyectos

def view_projects_gantt(project_list):
    st.subheader("📅 Diagrama Gantt de todos los proyectos")

    fig = obtener_grafico_gantt_proyectos(project_list)
   

    if fig is None:
        st.info("No hay proyectos registrados.")
        return
  
    st.plotly_chart(fig, use_container_width=True)