import streamlit as st
from app.controllers.dashboard_controller import DashboardController
from app.views.dashboard_utils.dashboard_sidebar import (
    sidebar_project_management,
    sidebar_project_navigation,
)
from app.views.dashboard_utils.sidebar_general_views import sidebar_general_views
from app.views.dashboard_utils.dashboard_pages import (
    page_gestor_tareas,
    page_diagrama_gantt,
    page_diagrama_gantt_global,
)
from app.views.dashboard_utils.dashboard_utils import sync_project_selection
from app.views.project_utils.project_edit_view import view_project_creation
from app.views.dashboard_utils.dashboard_router import render_general_view
from auth import logout  # Import local si no está global
from app.views.dashboard_utils.sidebar_messages import sidebar_messages
from app.views.messages.messages_view import render_messages_view

def show_dashboard():
    controller = DashboardController(st.session_state)
    #st.sidebar.markdown("---")  # Línea divisoria

    st.sidebar.title("📁 Proyectos")
    projects = controller.get_projects()
    selected_project = sidebar_project_management(controller, projects)
    sidebar_general_views(controller)
    sidebar_messages(controller)
    # Paso el estado de creación para controlar la navegación
    page = sidebar_project_navigation(selected_project, projects, controller.state.view_fake_project)

    # Si está creando un nuevo proyecto
    if controller.state.view_fake_project:
        view_project_creation(controller)
        return

    sync_project_selection(controller, selected_project)

    # Delegamos en router si hay una vista general activa
    if controller.state.vista_general and controller.state.vista_general != "Volver":
        render_general_view(controller)
        return

    if getattr(controller.state, "selected_chat_user", None):
        render_messages_view(controller, controller.state.selected_chat_user)
        return
    
    # Navegación de proyecto
    page_dispatch = {
        "Gestor de tareas": lambda: page_gestor_tareas(controller, selected_project),
        "Diagrama Gantt": lambda: page_diagrama_gantt(controller, selected_project),
        "Diagrama Gantt global de proyectos": lambda: page_diagrama_gantt_global(projects),
  
    }

    # Ejecuta la página elegida o muestra mensaje por defecto
    page_dispatch.get(
        page,
        lambda: st.info("No hay proyectos creados. Usá el formulario en la barra lateral."),
    )()

    logout()  # Se muestra siempre al final
    # 🔹 Botón de cerrar sesión al final del sidebar
