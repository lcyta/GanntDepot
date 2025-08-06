import streamlit as st
from PIL import Image
import io
from app.views.project_utils.extras.extras_view import render_extras_view


def render_project_info(detalle):
    """Muestra la información textual del proyecto."""
    with st.expander("📑 Detalles del proyecto seleccionado", expanded=False):
        st.markdown(f"👤 **Responsable:** {detalle.get('Responsable', '')}")
        st.markdown(f"👥 **Cliente:** {detalle.get('Cliente', '')}")
        st.markdown(f"🌍 **Localidad:** {detalle.get('Localidad', '')}")
        st.markdown(f"📏 **Metros²:** {detalle.get('Metros²', '0')} m²")
        st.markdown(f"📅 **Inicio:** {detalle.get('Inicio', '')}")
        st.markdown(f"⏱️ **Duración estimada:** {detalle.get('Duración estimada (días)', 'Sin dato')}")
        st.markdown(f"📊 **Estado:** {detalle.get('Estado', '')}")


def render_project_images(imagenes):
    """Muestra las imágenes asociadas al proyecto."""
    with st.expander("📷 Imágenes del proyecto", expanded=False):
        if imagenes:
            for i, img_bytes in enumerate(imagenes):
                image = Image.open(io.BytesIO(img_bytes))
                st.image(image, caption=f"Imagen {i+1}", use_container_width=True)
        else:
            st.info("📭 No hay imágenes cargadas para este proyecto.")


def render_project_extras(selected_project):
    """Muestra extras del proyecto."""
    with st.expander("📦 Extras", expanded=False):
        render_extras_view(selected_project)


def render_project_details(selected_project): 
    """Vista principal para mostrar detalles de un proyecto."""
    if "datos_proyectos" in st.session_state and selected_project in st.session_state.datos_proyectos:
        detalle = st.session_state.datos_proyectos[selected_project]

        with st.container():
            render_project_info(detalle)
            render_project_extras(selected_project)

    else:
        st.info("ℹ️ No se encontraron datos para este proyecto.")