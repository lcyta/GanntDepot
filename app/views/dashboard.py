import streamlit as st
from app.core.dashboard_controller import DashboardController
from app.views.dashboard_utils.dashboard_sidebar import sidebar_project_management, sidebar_general_views, sidebar_project_navigation
from app.views.dashboard_utils.dashboard_pages import page_gestor_tareas, page_diagrama_gantt, page_diagrama_gantt_global
from app.views.dashboard_utils.dashboard_utils import sync_project_selection

def show_dashboard():
    controller = DashboardController(st.session_state)
    st.sidebar.title("📁 Proyectos")

    projects = controller.get_projects()

    selected_project = sidebar_project_management(controller, projects)
    sidebar_general_views(controller)

    if controller.state.vista_general in ["👥 Gestionar responsables", "📆 Calendario laboral", "📅 Calendario por responsable"]:
        # Renderizado desde dashboard_pages.py (podés agregar funciones allí para esas vistas)
        _render_general_view(controller)
        return

    if controller.state.view_fake_project:
        from app.views.project_edit_view import view_project_creation
        view_project_creation()
        return

    sync_project_selection(controller, selected_project)

    page = sidebar_project_navigation(selected_project, projects)

    page_dispatch = {
        "Gestor de tareas": lambda: page_gestor_tareas(controller, selected_project),
        "Diagrama Gantt": lambda: page_diagrama_gantt(controller, selected_project),
        "Diagrama Gantt global de proyectos": lambda: page_diagrama_gantt_global(projects),
    }

    page_dispatch.get(page, lambda: st.info("No hay proyectos creados. Usá el formulario en la barra lateral."))()

def _render_general_view(controller):
    vista = controller.state.vista_general
    from app.views.responsibles_view import view_responsibles
    from app.views.calendar_view import view_calendar
    from app.views.responsible_calendar_view import view_responsible_calendar

    if vista == "👥 Gestionar responsables":
        view_responsibles()
    elif vista == "📆 Calendario laboral":
        view_calendar()
    elif vista == "📅 Calendario por responsable":
        view_responsible_calendar()