import streamlit as st
from app.views.project_utils.extras.data_shipment import load_shipment

def render_shipment_table(project_name):
    """
    Muestra todos los envíos de un proyecto en forma de tabla
    dentro de un expander para mantener la vista organizada.
    """
    shipments = load_shipment(project_name)

    with st.expander("📊 Tabla de Envíos", expanded=False):
        if not shipments:
            st.info("No hay envios para este proyecto aún.")
        else:
            # Convertimos la lista de diccionarios en tabla
            st.table(shipments)