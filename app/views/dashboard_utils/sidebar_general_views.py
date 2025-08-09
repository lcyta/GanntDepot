import streamlit as st
from app.views.dashboard_utils.const_views import GENERAL_VIEWS_KEYS

def sidebar_general_views(controller):
    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        controller.state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=["Volver"] + GENERAL_VIEWS_KEYS,
            index=0,
        )