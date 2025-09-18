import streamlit as st
from app.views.dashboard_utils.const_views import GENERAL_VIEWS_KEYS

def sidebar_general_views(controller):
    if controller.state.view_fake_project:
        return  # Oculto completamente el sidebar de vistas generales

    # Filtramos solo la opción "Gestionar responsables" si no tiene permiso
    opciones = []
    for key in GENERAL_VIEWS_KEYS:
        if key == "👥 Gestionar responsables":
            if "gestionar_responsables" in controller.state.get("permissions", []):
                opciones.append(key)
        else:
            opciones.append(key)

    # Siempre agregamos "Volver" como primera opción
    opciones = ["Volver"] + opciones

    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=opciones,
            index=0,
        )