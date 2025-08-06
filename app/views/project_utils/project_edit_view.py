import streamlit as st
import json
import pandas as pd
from app.views.project_utils.project_creation_view import render_project_form
from app.views.project_utils.project_service import guardar_proyecto
from app.core.data_manager import guardar_datos_proyecto, PROJECTS_FILE
from app.core.init_data import cargar_lista_proyectos
from app.core.data_manager import get_file_path
from app.views.project_utils.project_objective import render_project_objectives
from app.views.project_utils.project_photos import (
    render_photo_uploader,
    render_photo_slider,
)
from app.views.project_utils.project_team import render_project_team

def view_project_creation():
    st.title("🎨 Crear/Editar Proyecto")

    if not st.session_state.get("current_project"):
        handle_project_name_input()
        return

    datos_actualizados = render_project_form(
        st.session_state.datos_proyectos.get(st.session_state.current_project, {})
    )

    if st.button("✅ Guardar proyecto"):
        save_project(datos_actualizados)

def handle_project_name_input():
    nombre_nuevo = st.text_input("Nombre del nuevo proyecto", key="nombre_nuevo")

    col1, col2 = st.columns([1,1])
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

def crear_datos_iniciales_proyecto(nombre_proyecto):
    return {
        "Proyecto": nombre_proyecto,
        "Cliente": "",
        "Responsable": "",
        "Estado": "Pendiente",
        "Localidad": "",
        "Metros²": 0,
        "Inicio": str(pd.Timestamp.today().date()),
        "Duración estimada (días)": 0,
    }

def save_project(datos_actualizados):
    datos_actualizados["Proyecto"] = st.session_state.current_project
    guardar_proyecto(st.session_state.current_project, datos_actualizados)
    st.session_state.datos_proyectos[st.session_state.current_project] = datos_actualizados
    st.session_state.view_fake_project = False
    st.success("✅ Proyecto guardado correctamente.")
    st.rerun()