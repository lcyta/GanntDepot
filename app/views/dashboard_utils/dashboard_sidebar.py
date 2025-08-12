import streamlit as st

def sidebar_project_management(controller, projects):
    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):

        if controller.state.view_fake_project:
            return 
    
        if st.button("Crear proyecto"):
            controller.state.view_fake_project = True
            st.session_state.current_project = ""
            st.rerun()

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