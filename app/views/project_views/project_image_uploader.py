import streamlit as st

def render_project_image_uploader(selected_project):
    with st.expander("📷 Cargar fotos del proyecto seleccionado", expanded=False):
        st.markdown(f"Subí hasta 10 imágenes para **{selected_project}**")

        imagenes_subidas = st.file_uploader(
            "Seleccioná imágenes",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key=f"uploader_{selected_project}"  # clave única por proyecto
        )

        # Inicializar si no existe
        if "imagenes_proyectos" not in st.session_state:
            st.session_state.imagenes_proyectos = {}

        # Guardar imágenes nuevas
        if imagenes_subidas:
            imagenes_bytes = [img.read() for img in imagenes_subidas[:10]]
            st.session_state.imagenes_proyectos[selected_project] = imagenes_bytes
            st.success(f"✅ {len(imagenes_bytes)} imagen(es) guardada(s) para el proyecto **{selected_project}**.")

        # Mostrar imágenes ya guardadas
        elif selected_project in st.session_state.imagenes_proyectos:
            st.markdown("### 🖼️ Imágenes cargadas:")
            for idx, img_bytes in enumerate(st.session_state.imagenes_proyectos[selected_project]):
                st.image(img_bytes, caption=f"Imagen {idx + 1}", use_container_width=True)