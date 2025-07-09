import streamlit as st
from app.views.project_utils.project_objective import render_project_objectives
from app.views.project_utils.project_photos import (
    render_photo_uploader,
    render_photo_slider,
)
from app.views.project_utils.project_team import render_project_team


def view_project_creation():
    st.title(f"🎨 Proyecto: {st.session_state.current_project}")
    st.markdown("Esta es una vista ficticia de gestión del proyecto recién creado.")

    if "imagenes_proyecto_bytes" not in st.session_state:
        st.session_state.imagenes_proyecto_bytes = []
    if "imagen_index" not in st.session_state:
        st.session_state.imagen_index = 0

    # Mostrar cada sección modular
    render_project_objectives()
    render_photo_uploader()
    render_photo_slider()
    render_project_team()

    # Botón para volver
    if st.button("🔙 Volver al dashboard"):
        st.session_state.imagenes_proyecto_bytes = []
        st.session_state.imagen_index = 0
        st.session_state.view_fake_project = False
        st.rerun()
