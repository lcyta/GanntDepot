import streamlit as st
from PIL import Image
import io


def render_photo_uploader():
    with st.expander(
        "📌 Objetivos del proyecto", expanded=True
    ):  # Podés moverlo arriba o abajo según lógica
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


def render_photo_slider():
    with st.expander("🖼️ Ver fotos cargadas (slider)", expanded=True):
        imagenes_bytes = st.session_state.imagenes_proyecto_bytes
        if imagenes_bytes:
            index = st.session_state.imagen_index
            total = len(imagenes_bytes)
            img = Image.open(io.BytesIO(imagenes_bytes[index]))
            st.image(
                img, caption=f"Imagen {index+1} de {total}", use_container_width=True
            )

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
