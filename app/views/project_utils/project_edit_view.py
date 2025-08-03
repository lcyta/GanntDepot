import streamlit as st
import json
from app.core.data_manager import guardar_datos_proyecto, PROJECTS_FILE
from app.core.init_data import cargar_lista_proyectos
from app.core.data_manager import get_file_path
from app.views.project_utils.project_objective import render_project_objectives
from app.views.project_utils.project_photos import (
    render_photo_uploader,
    render_photo_slider,
)
from app.views.project_utils.project_team import render_project_team

def agregar_proyecto_a_lista(nombre):
    proyectos = cargar_lista_proyectos()
    if nombre not in proyectos:
        proyectos.append(nombre)
        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            for p in proyectos:
                f.write(p + "\n")

def view_project_creation():
    st.title(f"🎨 Crear/Editar Proyecto: {st.session_state.current_project}")

    # Inputs para que usuario complete los datos
    cliente = st.text_input("Cliente", key="cliente")
    responsable = st.text_input("Responsable", key="responsable")
    estado = st.selectbox("Estado", ["Pendiente", "En progreso", "Finalizado"], key="estado")
    localidad = st.text_input("Localidad", key="localidad")
    metros = st.number_input("Metros²", min_value=0, value=0, step=1, key="metros")
    fecha_inicio = st.date_input("Fecha de inicio", key="fecha_inicio")
    duracion = st.number_input("Duración estimada (días)", min_value=0, value=0, step=1, key="duracion")

    # Inicializar listas y contadores para imágenes
    if "imagenes_proyecto_bytes" not in st.session_state:
        st.session_state.imagenes_proyecto_bytes = []
    if "imagen_index" not in st.session_state:
        st.session_state.imagen_index = 0

    # Mostrar módulos adicionales si los tenés
    render_project_objectives()
    render_photo_uploader()
    render_photo_slider()
    render_project_team()

    # Botón para guardar datos
    if st.button("✅ Confirmar proyecto"):
        datos = {
            "Proyecto": st.session_state.current_project,
            "Cliente": cliente,
            "Responsable": responsable,
            "Estado": estado,
            "Localidad": localidad,
            "Metros²": metros,
            "Inicio": str(fecha_inicio),
            "Duración estimada (días)": duracion,
        }
        guardar_datos_proyecto(st.session_state.current_project, datos)
        agregar_proyecto_a_lista(st.session_state.current_project)
        st.session_state.datos_proyectos[st.session_state.current_project] = datos
        st.session_state.view_fake_project = False
        st.success("✅ Proyecto guardado correctamente.")
        st.rerun()