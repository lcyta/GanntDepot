import streamlit as st
from app.core.project_manager import save_project


def handle_project_creation(new_project_name):
    save_project(new_project_name.strip())
    st.session_state.current_project = new_project_name.strip()
    st.session_state.view_fake_project = True
    st.session_state.imagenes_proyecto_bytes = []
    st.session_state.imagen_index = 0
    st.rerun()
