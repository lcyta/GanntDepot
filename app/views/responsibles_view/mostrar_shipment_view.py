import streamlit as st
from app.views.project_utils.extras.data_shipment import load_shipment
from app.core.init_data import cargar_lista_proyectos

def render_all_shipments():
    """
    Muestra los envíos de TODOS los proyectos en una tabla general.
    """
    proyectos = cargar_lista_proyectos()

    all_shipments = []
    for proyecto in proyectos:
        shipments = load_shipment(proyecto)
        for envio in shipments:
            envio["Proyecto"] = proyecto  # agregamos referencia al proyecto
            all_shipments.append(envio)

    with st.expander("📦 Envíos de todos los proyectos", expanded=False):
        if not all_shipments:
            st.info("No hay envíos registrados en ningún proyecto.")
        else:
            st.table(all_shipments)