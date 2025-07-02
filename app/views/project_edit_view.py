import streamlit as st
from app.core.project_manager import save_project, load_projects
from PIL import Image
import io

def view_project_creation():
    st.title(f"🎨 Proyecto: {st.session_state.current_project}")
    st.markdown("Esta es una vista ficticia de gestión del proyecto recién creado.")

    if "imagenes_proyecto_bytes" not in st.session_state:
        st.session_state.imagenes_proyecto_bytes = []
    if "imagen_index" not in st.session_state:
        st.session_state.imagen_index = 0

    with st.expander("📌 Objetivos del proyecto", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("📅 Fecha estimada de terminación")
            duenio = st.text_input("👤 Dueño del proyecto")
            lugar = st.text_input("📍 Lugar")
            mt2 = st.number_input("📏 Metros cuadrados", min_value=0)
            localidad = st.text_input("🏘️ Localidad")

        with col2:
            imagenes_subidas = st.file_uploader(
                "📷 Subí hasta 10 fotos del proyecto",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="uploader"
            )

            # Actualizar solo si se subieron imágenes nuevas
            if imagenes_subidas and len(imagenes_subidas) > 0:
                nuevos_bytes = []
                for img in imagenes_subidas[:10]:
                    nuevos_bytes.append(img.read())

                # Guardar SOLO si son distintas o hay vacío
                if nuevos_bytes != st.session_state.imagenes_proyecto_bytes:
                    st.session_state.imagenes_proyecto_bytes = nuevos_bytes
                    st.session_state.imagen_index = 0

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

    with st.expander("🧑‍🤝‍🧑 Equipo asignado"):
        st.write("Esta sección mostraría los responsables asignados al proyecto.")

    if st.button("🔙 Volver al dashboard"):
        st.session_state.imagenes_proyecto_bytes = []
        st.session_state.imagen_index = 0
        st.session_state.view_fake_project = False
        st.rerun()

def create_project(new_project_name):
    save_project(new_project_name.strip())
    st.session_state.current_project = new_project_name.strip()
    st.session_state.view_fake_project = True
    st.session_state.imagenes_proyecto_bytes = []
    st.session_state.imagen_index = 0
    st.rerun()