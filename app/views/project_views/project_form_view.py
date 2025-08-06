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

        if not _hay_proyectos(projects):
            return

        selected_project = _seleccionar_proyecto(projects)
        if not selected_project:
            return

        datos = _obtener_datos_proyecto(selected_project)
        if not datos:
            return

        _mostrar_formulario_y_acciones(selected_project, datos)

def _hay_proyectos(projects):
    if not projects:
        st.info("No hay proyectos disponibles.")
        return False
    return True

def _seleccionar_proyecto(projects):
    return st.selectbox("Seleccioná un proyecto para editar", projects)

def _obtener_datos_proyecto(project_name):
    datos = get_project_data(project_name)
    if not datos:
        st.error("No se encontraron datos para el proyecto seleccionado.")
        return None
    return datos

def _mostrar_formulario_y_acciones(project_name, datos):
    form_data, guardar, eliminar = render_edit_project_form(project_name, datos)

    if guardar:
        save_project_changes(project_name, form_data)
        st.success(f"Proyecto '{project_name}' guardado correctamente.")
        st.rerun()

    if eliminar:
        # Podés agregar confirmación aquí si querés
        delete_existing_project(project_name)
        st.success(f"Proyecto '{project_name}' eliminado correctamente.")
        st.rerun()