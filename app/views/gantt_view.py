import streamlit as st
from app.views.gantt.gantt_projects_controller import obtener_grafico_gantt_proyectos
from app.views.gantt_proyectos_info import mostrar_grafico_info_proyectos

def view_projects_gantt(project_list):
    st.subheader("📅 Diagrama Gantt de todos los proyectos")

    #obtener_grafico_gantt_proyectos(project_list)
    fig= mostrar_grafico_info_proyectos()

    '''
    if fig is None:
        st.info("No hay proyectos registrados.")
        return
    '''
    #st.plotly_chart(fig, use_container_width=True)