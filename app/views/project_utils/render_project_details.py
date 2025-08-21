import streamlit as st
from app.views.project_utils.project_info_view import render_project_info
from app.views.project_utils.project_images_view import render_project_images
from app.views.project_utils.extras.extras_view import render_extras_view

def render_project_extras(selected_project):
    """Muestra extras del proyecto."""
    with st.expander("📦 Accesorios y Extras", expanded=False):
        render_extras_view(selected_project)

def render_project_details(selected_project): 
    """Vista principal para mostrar detalles de un proyecto."""
    if "datos_proyectos" in st.session_state and selected_project in st.session_state.datos_proyectos:
        detalle = st.session_state.datos_proyectos[selected_project]

        with st.container():
            render_project_info(detalle)
            render_project_extras(selected_project)
            # Podés decidir si querés mostrar imágenes aquí también
            # render_project_images(detalle.get("imagenes", []))
    else:
        st.info("ℹ️ No se encontraron datos para este proyecto.")