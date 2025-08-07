import streamlit as st
from app.forms.edit_project_form import render_edit_project_form
from app.views.project_views.project_edit_logic import guardar_cambios, eliminar_proyecto

def seleccionar_proyecto(projects):
    return st.selectbox("Seleccioná un proyecto para editar", projects)

def mostrar_formulario_y_acciones(project_name, datos):
    form_data, guardar, eliminar = render_edit_project_form(project_name, datos)

    if guardar:
        guardar_cambios(project_name, form_data)
        st.success(f"Proyecto '{project_name}' guardado correctamente.")
        st.rerun()

    if eliminar:
        eliminar_proyecto(project_name)
        st.success(f"Proyecto '{project_name}' eliminado correctamente.")
        st.rerun()