import streamlit as st
from app.views.project_utils.project_creation_logic import crear_datos_iniciales_proyecto

def handle_project_name_input():
    nombre_nuevo = st.text_input("Nombre del nuevo proyecto", key="nombre_nuevo")

    col1, col2 = st.columns([1, 1])
    with col1:
        confirmar = st.button("Confirmar nombre")
    with col2:
        volver = st.button("Volver")

    if confirmar:
        if nombre_nuevo.strip() == "":
            st.error("El nombre del proyecto no puede estar vacío.")
        else:
            st.session_state.current_project = nombre_nuevo.strip()
            st.session_state.datos_proyectos[st.session_state.current_project] = crear_datos_iniciales_proyecto(st.session_state.current_project)
            st.rerun()

    if volver:
        st.session_state.view_fake_project = False
        st.session_state.current_project = None
        st.rerun()