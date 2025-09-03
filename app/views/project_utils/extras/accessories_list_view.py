import streamlit as st
from app.views.project_utils.extras.accessories_editor import render_editor

def render_accessories_list(project_name, accesorios):
    """
    Renderiza la lista de accesorios con opciones de edición y eliminación.
    """
    with st.expander("🔧 Edición Accesorios del proyecto", expanded=False):
        if not accesorios:
            st.info("No hay accesorios para este proyecto aún.")
            return

        accesorio_seleccionado = _selector_accesorios(accesorios)
        if accesorio_seleccionado:
            render_editor(project_name, accesorio_seleccionado)


def _selector_accesorios(accesorios):
    """Muestra un selectbox para elegir un accesorio y devuelve el seleccionado."""
    nombres_accesorios = [a["Nombre"] for a in accesorios]
    nombre_seleccionado = st.selectbox("Seleccione un accesorio", nombres_accesorios)
    return next((a for a in accesorios if a["Nombre"] == nombre_seleccionado), None)