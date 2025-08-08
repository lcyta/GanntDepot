import streamlit as st
from PIL import Image
import io

def render_photo_uploader():
    with st.expander("📌 Objetivos del proyecto", expanded=True):
        with st.columns(2)[1]:
            imagenes_subidas = st.file_uploader(
                "📷 Subí hasta 10 fotos del proyecto",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="uploader",
            )

            if imagenes_subidas:
                nuevos_bytes = [img.read() for img in imagenes_subidas[:10]]
                if nuevos_bytes != st.session_state.imagenes_proyecto_bytes:
                    st.session_state.imagenes_proyecto_bytes = nuevos_bytes
                    st.session_state.imagen_index = 0