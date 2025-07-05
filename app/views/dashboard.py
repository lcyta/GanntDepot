import streamlit as st
from app.core.dashboard_controller import DashboardController
from app.views.dashboard_utils.dashboard_sidebar import (
    sidebar_project_management,
    sidebar_general_views,
    sidebar_project_navigation,
)
from app.views.dashboard_utils.dashboard_pages import (
    page_gestor_tareas,
    page_diagrama_gantt,
    page_diagrama_gantt_global,
)
from app.views.dashboard_utils.dashboard_utils import sync_project_selection
from app.views.project_utils.project_edit_view import view_project_creation
from app.views.dashboard_utils.dashboard_router import render_general_view  # Importamos aquí la función para vistas generales

def show_dashboard():
    controller = DashboardController(st.session_state)
    st.sidebar.title("📁 Proyectos")

    projects = controller.get_projects()
    selected_project = sidebar_project_management(controller, projects)
    sidebar_general_views(controller)
    page = sidebar_project_navigation(selected_project, projects)  # 👉 SIEMPRE visible

    if controller.state.view_fake_project:
        view_project_creation()
        return

    sync_project_selection(controller, selected_project)

    if controller.state.vista_general in [
        "👥 Gestionar responsables",
        "📆 Calendario laboral",
        "📅 Calendario por responsable",
    ]:
        render_general_view(controller)  # Acá delegamos la lógica de esas vistas
    else:
        page_dispatch = {
            "Gestor de tareas": lambda: page_gestor_tareas(controller, selected_project),
            "Diagrama Gantt": lambda: page_diagrama_gantt(controller, selected_project),
            "Diagrama Gantt global de proyectos": lambda: page_diagrama_gantt_global(projects),
        }
        page_dispatch.get(page, lambda: st.info("No hay proyectos creados. Usá el formulario en la barra lateral."))()