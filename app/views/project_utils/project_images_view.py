import streamlit as st
from PIL import Image
import io

def render_project_images(imagenes):
    """Muestra las imágenes asociadas al proyecto."""
    with st.expander("📷 Imágenes del proyecto", expanded=False):
        if imagenes:
            for i, img_bytes in enumerate(imagenes):
                image = Image.open(io.BytesIO(img_bytes))
                st.image(image, caption=f"Imagen {i+1}", use_container_width=True)
        else:
            st.info("📭 No hay imágenes cargadas para este proyecto.")