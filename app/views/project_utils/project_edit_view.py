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

    # Paso 1: Confirmar nombre del proyecto si no está seteado aún
    if not st.session_state.get("current_project"):
        nombre_nuevo = st.text_input("Nombre del nuevo proyecto", key="nombre_nuevo")
        if st.button("Confirmar nombre"):
            if nombre_nuevo.strip() == "":
                st.error("El nombre del proyecto no puede estar vacío.")
            else:
                st.session_state.current_project = nombre_nuevo.strip()
                st.session_state.datos_proyectos[st.session_state.current_project] = {
                    "Proyecto": st.session_state.current_project,
                    "Cliente": "",
                    "Responsable": "",
                    "Estado": "Pendiente",
                    "Localidad": "",
                    "Metros²": 0,
                    "Inicio": str(pd.Timestamp.today().date()),
                    "Duración estimada (días)": 0,
                }
                st.rerun()
        return

    # Paso 2: Mostrar formulario
    datos_actualizados = render_project_form(
        st.session_state.datos_proyectos.get(st.session_state.current_project, {})
    )

    # Paso 3: Guardar cambios
    if st.button("✅ Guardar proyecto"):
        datos_actualizados["Proyecto"] = st.session_state.current_project
        guardar_proyecto(st.session_state.current_project, datos_actualizados)
        st.session_state.datos_proyectos[st.session_state.current_project] = datos_actualizados
        st.session_state.view_fake_project = False
        st.success("✅ Proyecto guardado correctamente.")
        st.rerun()