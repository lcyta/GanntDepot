import streamlit as st
import json
import pandas as pd
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
    st.title("🎨 Crear/Editar Proyecto")

    # Paso 1: Confirmar nombre del proyecto si no está seteado aún
    if not st.session_state.get("current_project"):
        nombre_nuevo = st.text_input("Nombre del nuevo proyecto", key="nombre_nuevo")
        if st.button("Confirmar nombre"):
            if nombre_nuevo.strip() == "":
                st.error("El nombre del proyecto no puede estar vacío.")
            else:
                st.session_state.current_project = nombre_nuevo.strip()
                # Inicializar datos vacíos para el proyecto nuevo
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
        return  # No mostrar nada más hasta confirmar nombre

    # Paso 2: Mostrar formulario completo con datos cargados o vacíos
    datos = st.session_state.datos_proyectos.get(st.session_state.current_project, {})

    with st.expander("📌 Detalles Proyecto", expanded=True):
        cliente = st.text_input("👤 Cliente", value=datos.get("Cliente", ""), key="cliente")
        responsable = st.text_input("👤 Responsable", value=datos.get("Responsable", ""), key="responsable")
        estado = st.selectbox("Estado", ["Pendiente", "En progreso", "Finalizado"], index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente")), key="estado")
        localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""), key="localidad")
        metros = st.number_input("📏 Metros²", min_value=0, value=datos.get("Metros²", 0), step=1, key="metros")
        fecha_inicio_val = pd.to_datetime(datos.get("Inicio", str(pd.Timestamp.today().date()))).date()
        fecha_inicio = st.date_input("📅 Fecha de inicio", value=fecha_inicio_val, key="fecha_inicio")
        duracion = st.number_input("⏱️ Duración estimada (días)", min_value=0, value=datos.get("Duración estimada (días)", 0), step=1, key="duracion")

    # Botón para guardar cambios
    if st.button("✅ Guardar proyecto"):
        datos_actualizados = {
            "Proyecto": st.session_state.current_project,
            "Cliente": cliente,
            "Responsable": responsable,
            "Estado": estado,
            "Localidad": localidad,
            "Metros²": metros,
            "Inicio": str(fecha_inicio),
            "Duración estimada (días)": duracion,
        }
        guardar_datos_proyecto(st.session_state.current_project, datos_actualizados)
        agregar_proyecto_a_lista(st.session_state.current_project)
        st.session_state.datos_proyectos[st.session_state.current_project] = datos_actualizados
        st.session_state.view_fake_project = False
        st.success("✅ Proyecto guardado correctamente.")
        st.rerun()