import streamlit as st
from app.forms.edit_project_form import render_edit_project_form
from app.forms.project_service import (
    get_project_data,
    save_project_changes,
    delete_existing_project
)

def editar_eliminar_proyectos(projects):
    with st.expander("### 🔧 Editar o eliminar proyectos", expanded=False):
        st.markdown("### ✏️ Editar o eliminar proyectos")

        if not projects:
            st.info("No hay proyectos disponibles.")
            return

        selected_project = st.selectbox("Seleccioná un proyecto para editar", projects)
        if not selected_project:
            return

        datos = get_project_data(selected_project)
        if not datos:
            return

        form_data, guardar, eliminar = render_edit_project_form(selected_project, datos)

        if guardar:
            save_project_changes(selected_project, form_data)

        if eliminar:
            delete_existing_project(selected_project)