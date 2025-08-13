import streamlit as st
from app.views.project_views.project_edit_logic import (
    hay_proyectos,
    obtener_datos,
    guardar_cambios,
    eliminar_proyecto
)
from app.views.project_views.project_edit_helpers import (
    seleccionar_proyecto,
    mostrar_formulario_y_acciones
)

def editar_eliminar_proyectos(projects):
    with st.expander("### 🔧 Editar o eliminar proyectos", expanded=False):
        st.markdown("### 🔧 Editar o eliminar proyectos")

        if not hay_proyectos(projects):
            st.info("No hay proyectos disponibles.")
            return

        selected_project = seleccionar_proyecto(projects)
        if not selected_project:
            return

        datos = obtener_datos(selected_project)
        if not datos:
            st.error("No se encontraron datos para el proyecto seleccionado.")
            return

        mostrar_formulario_y_acciones(selected_project, datos)