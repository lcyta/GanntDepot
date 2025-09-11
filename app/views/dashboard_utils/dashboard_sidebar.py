import streamlit as st
from app.utils.actions_registry import ACTIONS_PROJECT_CREATION
import json

def sidebar_project_management(controller, projects):
    # Obtener el username logueado
    username = st.session_state.get("username")
    
    # Cargar usuarios desde archivo (o desde session_state si ya lo cargaste antes)
    with open("data/usuarios_gestion.json", "r") as f:
        usuarios = json.load(f)
    
    # Obtener permisos del usuario logueado
    usuario = next((u for u in usuarios if u["username"] == username), None)
    permisos = usuario.get("permissions", []) if usuario else []

    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):

        # Mostrar botón "Crear proyecto" si tiene permiso
        if "crear_proyecto" in permisos:
            if st.button("Crear proyecto"):
                controller.state.view_fake_project = True
                st.session_state.current_project = ""
                st.rerun()

        # Mostrar selectbox de proyectos si no se está creando uno nuevo
        if not controller.state.view_fake_project and projects:
            return st.selectbox("Seleccioná un proyecto", projects)

    return None


def sidebar_project_navigation(selected_project, projects, creating_project):
    if creating_project:
        return None

    opciones_nav = []
    if selected_project:
        opciones_nav.extend(["Gestor de tareas", "Diagrama Gantt"])
        opciones_nav.append("Diagrama Gantt global de proyectos")

    return st.sidebar.radio("Ir a:", opciones_nav)