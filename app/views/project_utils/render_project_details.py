import streamlit as st
from PIL import Image
import io

def render_project_details(selected_project):
    if "datos_proyectos" in st.session_state and selected_project in st.session_state.datos_proyectos:
        detalle = st.session_state.datos_proyectos[selected_project]
        
        with st.expander("📋 Detalles del proyecto seleccionado", expanded=False):
            with st.expander("📋 Detalles del proyecto seleccionado", expanded=False):
                st.markdown(f"👤 **Responsable:** {detalle['Responsable']}")
                st.markdown(f"👥 **Cliente:** {detalle['Cliente']}")
                st.markdown(f"🏙️ **Localidad:** {detalle['Localidad']}")
                st.markdown(f"📏 **Metros²:** {detalle['Metros²']} m²")
                st.markdown(f"📅 **Inicio:** {detalle['Inicio']}")
                st.markdown(f"⏱️ **Duración estimada:** {detalle['Duración estimada (días)']} días")
                st.markdown(f"📊 **Estado:** {detalle['Estado']}")

            # Mostrar imágenes asociadas
            with st.expander("📋 Mostrar imágenes asociadas", expanded=False):
                if "imagenes_proyectos" in st.session_state and selected_project in st.session_state.imagenes_proyectos:
                    imagenes = st.session_state.imagenes_proyectos[selected_project]
                    with st.expander("🖼️ Imágenes del proyecto", expanded=False):
                        for i, img_bytes in enumerate(imagenes):
                            image = Image.open(io.BytesIO(img_bytes))
                            st.image(image, caption=f"Imagen {i+1}", use_container_width=True)
                else:
                    st.info("📭 No hay imágenes cargadas para este proyecto.")
    else:
        st.info("ℹ️ No se encontraron datos para este proyecto.")