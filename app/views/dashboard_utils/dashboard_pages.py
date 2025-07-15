import streamlit as st
from app.views.task_views_operations.task_view import view_tasks
from app.views.gantt_view import view_projects_gantt
from app.views.gantt_tasks_view import view_tasks_gantt


def page_gestor_tareas(controller, selected_project):
    col_title, col_edit, col_delete = st.columns([5, 1, 1])
    col_title.title(f"Proyecto: {selected_project}")

    if "datos_proyectos" in st.session_state and selected_project in st.session_state.datos_proyectos:
        detalle = st.session_state.datos_proyectos[selected_project]

        with st.expander("📋 Detalles del proyecto seleccionado", expanded=True):
            st.markdown(f"👤 **Responsable:** {detalle['Responsable']}")
            st.markdown(f"👥 **Cliente:** {detalle['Cliente']}")
            st.markdown(f"🏙️ **Localidad:** {detalle['Localidad']}")
            st.markdown(f"📏 **Metros²:** {detalle['Metros²']} m²")
            st.markdown(f"📅 **Inicio:** {detalle['Inicio']}")
            st.markdown(f"⏱️ **Duración estimada:** {detalle['Duración estimada (días)']} días")
            st.markdown(f"📊 **Estado:** {detalle['Estado']}")
    else:
        st.info("ℹ️ No se encontraron datos para este proyecto.")
        
    if controller.state.task_changed:
        controller.reload_tasks()
        controller.state.task_changed = False

    view_tasks(controller.state.tasks, selected_project)


def page_diagrama_gantt(controller, selected_project):
    view_tasks_gantt(controller.state.tasks, selected_project)


def page_diagrama_gantt_global(projects):
    view_projects_gantt(projects)
