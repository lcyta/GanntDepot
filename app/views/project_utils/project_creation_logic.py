import streamlit as st
import pandas as pd
from app.views.project_utils.project_service import guardar_proyecto

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