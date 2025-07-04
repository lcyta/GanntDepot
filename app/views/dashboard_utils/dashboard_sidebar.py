import streamlit as st

def sidebar_project_management(controller, projects):
    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):
        new_project = st.text_input("Crear nuevo proyecto")
        if st.button("Crear proyecto") and new_project.strip():
            controller.create_project(new_project)
            st.experimental_rerun()

        if not controller.state.view_fake_project and projects:
            return st.selectbox("Seleccioná un proyecto", projects)
    return None

def sidebar_general_views(controller):
    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=(
                "Ninguna",
                "👥 Gestionar responsables",
                "📆 Calendario laboral",
                "📅 Calendario por responsable",
            ),
            index=0,
        )

def sidebar_project_navigation(selected_project, projects):
    opciones_nav = []
    if selected_project:
        opciones_nav.extend(["Gestor de tareas", "Diagrama Gantt"])
    opciones_nav.append("Diagrama Gantt global de proyectos")

    return st.sidebar.radio("Ir a:", opciones_nav)