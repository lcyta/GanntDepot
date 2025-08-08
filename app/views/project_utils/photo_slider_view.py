import streamlit as st
from PIL import Image
import io

def render_photo_slider():
    with st.expander("🖼️ Ver fotos cargadas (slider)", expanded=True):
        imagenes_bytes = st.session_state.imagenes_proyecto_bytes
        if imagenes_bytes:
            index = st.session_state.imagen_index
            total = len(imagenes_bytes)
            img = Image.open(io.BytesIO(imagenes_bytes[index]))
            st.image(img, caption=f"Imagen {index+1} de {total}", use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Anterior", disabled=index == 0):
                    st.session_state.imagen_index = index - 1
                    st.rerun()
            with col2:
                if st.button("➡️ Siguiente", disabled=index == total - 1):
                    st.session_state.imagen_index = index + 1
                    st.rerun()
        else:
            st.info("📭 Aún no se subieron imágenes.")