import streamlit as st
from app.views.project_utils.extras.data_accessories import load_accessories

def render_accessories_table(project_name):
    """
    Muestra todos los accesorios de un proyecto en forma de tabla
    dentro de un expander para mantener la vista organizada.
    """
    accesorios = load_accessories(project_name)

    with st.expander("📊 Tabla de Accesorios", expanded=False):
        if not accesorios:
            st.info("No hay accesorios para este proyecto aún.")
        else:
            # Convertimos la lista de diccionarios en tabla
            st.table(accesorios)