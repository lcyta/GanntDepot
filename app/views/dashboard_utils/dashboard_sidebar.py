import streamlit as st

# Definí las vistas generales en un diccionario para no duplicar
GENERAL_VIEWS_KEYS = [
    "👥 Gestionar responsables",
    "📆 Calendario laboral",
    "📁 Gestión de proyectos",
]

def sidebar_project_management(controller, projects):
    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):
        if st.button("Crear proyecto"):
            controller.state.view_fake_project = True
            st.session_state.current_project = ""
            st.rerun()

        if not controller.state.view_fake_project and projects:
            return st.selectbox("Seleccioná un proyecto", projects)
    return None


def sidebar_general_views(controller):
    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=["Volver"] + GENERAL_VIEWS_KEYS,
            index=0,
        )


def sidebar_project_navigation(selected_project, projects, creating_project):
    if creating_project:
        return None  # No mostrar opciones de navegación de proyecto al crear uno nuevo

    opciones_nav = []
    if selected_project:
        opciones_nav.extend(["Gestor de tareas", "Diagrama Gantt"])
    opciones_nav.append("Diagrama Gantt global de proyectos")

    return st.sidebar.radio("Ir a:", opciones_nav)