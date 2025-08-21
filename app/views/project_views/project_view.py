import streamlit as st
from app.core.project_manager import load_projects
from app.views.project_views.project_table_view import mostrar_tabla_proyectos
from app.views.project_views.project_detail_view import mostrar_detalles_proyecto
from app.views.project_views.project_form_view import editar_eliminar_proyectos
from app.views.project_views.project_image_uploader import render_project_image_uploader
from app.views.responsibles_view.mostrar_tareas_view import mostrar_tareas_view
from app.views.responsibles_view.mostrar_shipment_view import render_all_shipments

def view_project_list():
    st.subheader("📝 Gestión de Proyectos")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    mostrar_tabla_proyectos(projects)
    selected_project = mostrar_detalles_proyecto(projects)
    editar_eliminar_proyectos(projects)
    mostrar_tareas_view()
    render_all_shipments()
    #if selected_project:
     #   render_project_image_uploader(selected_project)