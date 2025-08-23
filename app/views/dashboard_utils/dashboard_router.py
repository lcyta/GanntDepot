from app.views.general_responsibles_view import general_responsibles_view
from app.views.calendar.calendar_view import view_calendar
from app.views.project_views.project_view import view_project_list

# Diccionario con las vistas generales
GENERAL_VIEWS = {
    "👥 Gestionar responsables": general_responsibles_view,
    "📆 Calendario laboral": view_calendar,
   # "📅 Calendario por responsable": view_responsible_calendar,
    "📁 Gestión de proyectos": view_project_list,
}

def render_general_view(controller):
    vista = controller.state.vista_general
    view_func = GENERAL_VIEWS.get(vista)
    if view_func:
        view_func()
    else:
        import streamlit as st
        st.info("Seleccioná una vista válida")
