import streamlit as st
from app.views.dashboard_utils.const_views import GENERAL_VIEWS_KEYS

def sidebar_general_views(controller):
    if controller.state.view_fake_project:
        return  # Oculto completamente el sidebar de vistas generales

    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=["Volver"] + GENERAL_VIEWS_KEYS,
            index=0,
        )