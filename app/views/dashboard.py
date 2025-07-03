import streamlit as st
from app.views.task_view import view_tasks
from app.views.gantt_view import view_projects_gantt
from app.views.gantt_tasks_view import view_tasks_gantt
from app.views.responsibles_view import view_responsibles
from app.views.calendar_view import view_calendar
from app.views.responsible_calendar_view import view_responsible_calendar
from app.views.project_edit_view import view_project_creation

from app.core.dashboard_controller import DashboardController  # Importa el controlador

def show_dashboard():
    controller = DashboardController(st.session_state)

    st.sidebar.title("📁 Proyectos")

    projects = controller.get_projects()

    # Gestionar creación proyecto
    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):
        new_project = st.text_input("Crear nuevo proyecto")
        if st.button("Crear proyecto") and new_project.strip():
            controller.create_project(new_project)
            st.experimental_rerun()  # recarga para que se actualice la lista

        selected_project = None
        if not controller.state.view_fake_project and projects:
            selected_project = st.selectbox("Seleccioná un proyecto", projects)

    # Vistas generales
    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=(
                "Ninguna",
                "👥 Gestionar responsables",
                "📆 Calendario laboral",
                "📅 Calendario por responsable"
            ),
            index=0,
        )

    # Navegar vistas generales
    if controller.state.vista_general == "👥 Gestionar responsables":
        view_responsibles()
        return
    elif controller.state.vista_general == "📆 Calendario laboral":
        view_calendar()
        return
    elif controller.state.vista_general == "📅 Calendario por responsable":
        view_responsible_calendar()
        return

    # Vista proyecto fake
    if controller.state.view_fake_project:
        view_project_creation()
        return

    # Selección proyecto
    if selected_project != controller.state.current_project:
        controller.select_project(selected_project)
        controller.state.task_changed = False
        controller.state.calendar_dirty = False
    elif controller.state.calendar_dirty and selected_project:
        controller.reload_tasks()
        controller.state.calendar_dirty = False

    opciones_nav = []
    if selected_project:
        opciones_nav.extend(["Gestor de tareas", "Diagrama Gantt"])
    opciones_nav.append("Diagrama Gantt global de proyectos")

    page = st.sidebar.radio("Ir a:", opciones_nav)

    # Aquí tu lógica para las vistas según page
    if page == "Gestor de tareas":
        # Mostrar título y botones para editar o borrar proyecto (igual que antes)
        col_title, col_edit, col_delete = st.columns([5, 1, 1])
        col_title.title(f"Proyecto: {selected_project}")

        # ... y seguir con la lógica de renombrar y borrar proyecto, pero usando controller.rename_project, controller.delete_project, etc.
        # Y para mostrar tareas:
        if controller.state.task_changed:
            controller.reload_tasks()
            controller.state.task_changed = False

        view_tasks(controller.state.tasks, selected_project)

    elif page == "Diagrama Gantt":
        view_tasks_gantt(controller.state.tasks, selected_project)

    elif page == "Diagrama Gantt global de proyectos":
        view_projects_gantt(projects)

    if not selected_project and not projects:
        st.info("No hay proyectos creados. Usá el formulario en la barra lateral.")